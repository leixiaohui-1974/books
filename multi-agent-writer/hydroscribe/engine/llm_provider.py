"""
LLM Provider Abstraction Layer — 多LLM后端统一接口

支持的提供商：
- alibaba_bailian (阿里云百炼): qwen-plus, qwen-max, qwen-turbo 等
- openai: gpt-4o, gpt-4-turbo 等
- anthropic: claude-3.5-sonnet, claude-3-opus 等
- local: Ollama/vLLM 等本地部署

设计原则：
- 工厂模式：根据 config.toml 配置自动创建对应客户端
- 重试机制：指数退避，最多 3 次重试
- 降级策略：主模型失败后自动切换到备选模型
- Token 用量追踪：统一的 usage 统计接口
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger("hydroscribe.llm_provider")


class CircuitState(str, Enum):
    """熔断器状态"""
    CLOSED = "closed"        # 正常 — 请求通过
    OPEN = "open"            # 熔断 — 快速失败
    HALF_OPEN = "half_open"  # 试探 — 允许少量请求通过


class CircuitBreaker:
    """
    LLM 熔断器 — 防止 API 级联失败

    状态机:
    CLOSED → (连续 failure_threshold 次失败) → OPEN
    OPEN → (等待 recovery_timeout 秒) → HALF_OPEN
    HALF_OPEN → (success_threshold 次连续成功) → CLOSED
    HALF_OPEN → (任意一次失败) → OPEN
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        success_threshold: int = 2,
        name: str = "default",
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold
        self.name = name

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._success_count = 0
        self._last_failure_time = 0.0
        self._total_trips = 0  # 累计熔断次数

    @property
    def state(self) -> CircuitState:
        if self._state == CircuitState.OPEN:
            if time.monotonic() - self._last_failure_time >= self.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._success_count = 0
                logger.info(f"熔断器 [{self.name}] OPEN → HALF_OPEN (尝试恢复)")
        return self._state

    def record_success(self):
        if self._state == CircuitState.HALF_OPEN:
            self._success_count += 1
            if self._success_count >= self.success_threshold:
                self._state = CircuitState.CLOSED
                self._failure_count = 0
                logger.info(f"熔断器 [{self.name}] HALF_OPEN → CLOSED (已恢复)")
        else:
            self._failure_count = 0

    def record_failure(self):
        self._failure_count += 1
        self._last_failure_time = time.monotonic()

        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
            self._total_trips += 1
            logger.warning(f"熔断器 [{self.name}] HALF_OPEN → OPEN (恢复失败)")
        elif self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN
            self._total_trips += 1
            logger.warning(
                f"熔断器 [{self.name}] CLOSED → OPEN "
                f"(连续 {self._failure_count} 次失败, 累计熔断 {self._total_trips} 次)"
            )

    def allow_request(self) -> bool:
        return self.state != CircuitState.OPEN

    def get_stats(self) -> dict:
        return {
            "state": self.state.value,
            "failure_count": self._failure_count,
            "total_trips": self._total_trips,
            "recovery_timeout": self.recovery_timeout,
        }


class LLMProvider(str, Enum):
    """支持的 LLM 提供商"""
    ALIBABA_BAILIAN = "alibaba_bailian"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"


@dataclass
class LLMConfig:
    """LLM 配置数据类"""
    provider: LLMProvider
    model: str
    api_key: str = ""
    base_url: str = ""
    max_tokens: int = 4096
    temperature: float = 0.3
    top_p: float = 0.95
    timeout: int = 120
    max_retries: int = 3
    retry_delay: float = 2.0  # 初始重试延迟（秒）
    extra: Dict[str, Any] = field(default_factory=dict)

    # 降级配置
    fallback_model: str = ""
    fallback_provider: str = ""


@dataclass
class LLMUsage:
    """Token 用量统计"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = ""
    provider: str = ""
    latency_ms: int = 0


@dataclass
class LLMResponse:
    """统一的 LLM 响应格式"""
    content: str = ""
    usage: Optional[LLMUsage] = None
    model: str = ""
    provider: str = ""
    finish_reason: str = ""
    raw_response: Optional[Any] = None


class BaseLLMClient(ABC):
    """LLM 客户端基类"""

    def __init__(self, config: LLMConfig):
        self.config = config
        self._total_usage = LLMUsage()
        self._circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60.0,
            success_threshold=2,
            name=f"{config.provider.value}/{config.model}",
        )

    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> LLMResponse:
        """生成文本 — 子类必须实现"""
        ...

    async def generate_with_retry(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> LLMResponse:
        """带重试 + 熔断器的生成"""
        # 熔断器检查
        if not self._circuit_breaker.allow_request():
            raise RuntimeError(
                f"熔断器已打开 [{self._circuit_breaker.name}]，"
                f"将在 {self._circuit_breaker.recovery_timeout}s 后尝试恢复"
            )

        last_error = None
        delay = self.config.retry_delay

        for attempt in range(1, self.config.max_retries + 1):
            try:
                response = await self.generate(
                    messages=messages,
                    system_prompt=system_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
                if response.usage:
                    self._total_usage.prompt_tokens += response.usage.prompt_tokens
                    self._total_usage.completion_tokens += response.usage.completion_tokens
                    self._total_usage.total_tokens += response.usage.total_tokens
                self._circuit_breaker.record_success()
                return response
            except Exception as e:
                last_error = e
                self._circuit_breaker.record_failure()
                if attempt < self.config.max_retries:
                    # 如果熔断器已打开，不再重试
                    if not self._circuit_breaker.allow_request():
                        logger.warning(f"熔断器打开，跳过剩余重试")
                        break
                    logger.warning(
                        f"LLM 调用失败 (尝试 {attempt}/{self.config.max_retries}): {e}. "
                        f"{delay:.1f}s 后重试..."
                    )
                    await asyncio.sleep(delay)
                    delay *= 2  # 指数退避

        raise RuntimeError(
            f"LLM 调用在 {self.config.max_retries} 次重试后仍然失败: {last_error}"
        )

    @property
    def circuit_breaker_stats(self) -> dict:
        return self._circuit_breaker.get_stats()

    def get_total_usage(self) -> LLMUsage:
        return self._total_usage

    def reset_usage(self):
        self._total_usage = LLMUsage()


class AlibabaBailianClient(BaseLLMClient):
    """
    阿里云百炼大模型客户端

    支持 OpenAI 兼容模式 (dashscope compatible-mode)，
    也支持原生 DashScope SDK。
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from openai import AsyncOpenAI
            except ImportError:
                raise ImportError("需要安装 openai 库: pip install openai")

            base_url = self.config.base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
            self._client = AsyncOpenAI(
                api_key=self.config.api_key,
                base_url=base_url,
                timeout=self.config.timeout,
            )
        return self._client

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> LLMResponse:
        client = self._get_client()
        start_time = time.monotonic()

        api_messages = []
        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})
        api_messages.extend(messages)

        response = await client.chat.completions.create(
            model=self.config.model,
            messages=api_messages,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=temperature if temperature is not None else self.config.temperature,
            top_p=self.config.top_p,
        )

        latency = int((time.monotonic() - start_time) * 1000)

        usage = None
        if response.usage:
            usage = LLMUsage(
                prompt_tokens=response.usage.prompt_tokens or 0,
                completion_tokens=response.usage.completion_tokens or 0,
                total_tokens=response.usage.total_tokens or 0,
                model=self.config.model,
                provider="alibaba_bailian",
                latency_ms=latency,
            )

        content = ""
        finish_reason = ""
        if response.choices:
            content = response.choices[0].message.content or ""
            finish_reason = response.choices[0].finish_reason or ""

        return LLMResponse(
            content=content,
            usage=usage,
            model=self.config.model,
            provider="alibaba_bailian",
            finish_reason=finish_reason,
            raw_response=response,
        )


class OpenAIClient(BaseLLMClient):
    """OpenAI / OpenAI-compatible 客户端"""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from openai import AsyncOpenAI
            except ImportError:
                raise ImportError("需要安装 openai 库: pip install openai")

            kwargs = {
                "api_key": self.config.api_key,
                "timeout": self.config.timeout,
            }
            if self.config.base_url:
                kwargs["base_url"] = self.config.base_url

            self._client = AsyncOpenAI(**kwargs)
        return self._client

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> LLMResponse:
        client = self._get_client()
        start_time = time.monotonic()

        api_messages = []
        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})
        api_messages.extend(messages)

        response = await client.chat.completions.create(
            model=self.config.model,
            messages=api_messages,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=temperature if temperature is not None else self.config.temperature,
        )

        latency = int((time.monotonic() - start_time) * 1000)

        usage = None
        if response.usage:
            usage = LLMUsage(
                prompt_tokens=response.usage.prompt_tokens or 0,
                completion_tokens=response.usage.completion_tokens or 0,
                total_tokens=response.usage.total_tokens or 0,
                model=self.config.model,
                provider="openai",
                latency_ms=latency,
            )

        content = ""
        finish_reason = ""
        if response.choices:
            content = response.choices[0].message.content or ""
            finish_reason = response.choices[0].finish_reason or ""

        return LLMResponse(
            content=content,
            usage=usage,
            model=self.config.model,
            provider="openai",
            finish_reason=finish_reason,
            raw_response=response,
        )


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude 客户端"""

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from anthropic import AsyncAnthropic
            except ImportError:
                raise ImportError("需要安装 anthropic 库: pip install anthropic")

            kwargs = {"api_key": self.config.api_key}
            if self.config.base_url:
                kwargs["base_url"] = self.config.base_url

            self._client = AsyncAnthropic(**kwargs)
        return self._client

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> LLMResponse:
        client = self._get_client()
        start_time = time.monotonic()

        # Anthropic 的 system 放在 create 参数中，不放在 messages 中
        kwargs = {
            "model": self.config.model,
            "messages": messages,
            "max_tokens": max_tokens or self.config.max_tokens,
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        if temperature is not None:
            kwargs["temperature"] = temperature
        elif self.config.temperature > 0:
            kwargs["temperature"] = self.config.temperature

        response = await client.messages.create(**kwargs)

        latency = int((time.monotonic() - start_time) * 1000)

        usage = LLMUsage(
            prompt_tokens=response.usage.input_tokens if response.usage else 0,
            completion_tokens=response.usage.output_tokens if response.usage else 0,
            total_tokens=(
                (response.usage.input_tokens + response.usage.output_tokens)
                if response.usage else 0
            ),
            model=self.config.model,
            provider="anthropic",
            latency_ms=latency,
        )

        content = ""
        if response.content:
            content = response.content[0].text if response.content else ""

        return LLMResponse(
            content=content,
            usage=usage,
            model=self.config.model,
            provider="anthropic",
            finish_reason=response.stop_reason or "",
            raw_response=response,
        )


class LocalLLMClient(BaseLLMClient):
    """
    本地 LLM 客户端 (Ollama / vLLM / LM Studio 等)
    使用 OpenAI 兼容 API
    """

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                from openai import AsyncOpenAI
            except ImportError:
                raise ImportError("需要安装 openai 库: pip install openai")

            base_url = self.config.base_url or "http://localhost:11434/v1"
            self._client = AsyncOpenAI(
                api_key=self.config.api_key or "local",
                base_url=base_url,
                timeout=self.config.timeout,
            )
        return self._client

    async def generate(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> LLMResponse:
        client = self._get_client()
        start_time = time.monotonic()

        api_messages = []
        if system_prompt:
            api_messages.append({"role": "system", "content": system_prompt})
        api_messages.extend(messages)

        response = await client.chat.completions.create(
            model=self.config.model,
            messages=api_messages,
            max_tokens=max_tokens or self.config.max_tokens,
            temperature=temperature if temperature is not None else self.config.temperature,
        )

        latency = int((time.monotonic() - start_time) * 1000)

        usage = None
        if response.usage:
            usage = LLMUsage(
                prompt_tokens=response.usage.prompt_tokens or 0,
                completion_tokens=response.usage.completion_tokens or 0,
                total_tokens=response.usage.total_tokens or 0,
                model=self.config.model,
                provider="local",
                latency_ms=latency,
            )

        content = ""
        finish_reason = ""
        if response.choices:
            content = response.choices[0].message.content or ""
            finish_reason = response.choices[0].finish_reason or ""

        return LLMResponse(
            content=content,
            usage=usage,
            model=self.config.model,
            provider="local",
            finish_reason=finish_reason,
            raw_response=response,
        )


# ── 提供商注册表 ─────────────────────────────────────────────────

_PROVIDER_REGISTRY: Dict[LLMProvider, type] = {
    LLMProvider.ALIBABA_BAILIAN: AlibabaBailianClient,
    LLMProvider.OPENAI: OpenAIClient,
    LLMProvider.ANTHROPIC: AnthropicClient,
    LLMProvider.LOCAL: LocalLLMClient,
}


def create_llm_client(config: LLMConfig) -> BaseLLMClient:
    """工厂函数 — 根据配置创建 LLM 客户端"""
    client_cls = _PROVIDER_REGISTRY.get(config.provider)
    if not client_cls:
        raise ValueError(f"不支持的 LLM 提供商: {config.provider}")
    return client_cls(config)


def create_llm_from_dict(config_dict: Dict[str, Any]) -> BaseLLMClient:
    """从字典创建 LLM 客户端"""
    provider = config_dict.get("provider", "openai")
    try:
        provider_enum = LLMProvider(provider)
    except ValueError:
        raise ValueError(f"不支持的 LLM 提供商: {provider}")

    config = LLMConfig(
        provider=provider_enum,
        model=config_dict.get("model", ""),
        api_key=config_dict.get("api_key", ""),
        base_url=config_dict.get("base_url", ""),
        max_tokens=config_dict.get("max_tokens", 4096),
        temperature=config_dict.get("temperature", 0.3),
        top_p=config_dict.get("top_p", 0.95),
        timeout=config_dict.get("timeout", 120),
        max_retries=config_dict.get("max_retries", 3),
        retry_delay=config_dict.get("retry_delay", 2.0),
        fallback_model=config_dict.get("fallback_model", ""),
        fallback_provider=config_dict.get("fallback_provider", ""),
        extra=config_dict.get("extra", {}),
    )

    return create_llm_client(config)


class LLMManager:
    """
    LLM 管理器 — 多提供商管理 + 降级策略

    支持：
    - 为不同角色（writer/reviewer）配置不同的模型
    - 主模型故障自动降级到备选模型
    - 统一 token 用量统计
    """

    def __init__(self):
        self._clients: Dict[str, BaseLLMClient] = {}
        self._configs: Dict[str, LLMConfig] = {}
        self._default_role = "default"

    def register(self, role: str, config: LLMConfig):
        """注册一个角色的 LLM 配置"""
        self._configs[role] = config
        self._clients[role] = create_llm_client(config)

    def get_client(self, role: str = "default") -> BaseLLMClient:
        """获取指定角色的 LLM 客户端"""
        if role in self._clients:
            return self._clients[role]
        if self._default_role in self._clients:
            return self._clients[self._default_role]
        raise RuntimeError(f"未找到角色 '{role}' 的 LLM 客户端，且无默认配置")

    async def generate(
        self,
        role: str,
        messages: List[Dict[str, str]],
        system_prompt: str = "",
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> LLMResponse:
        """通过角色调用 LLM，支持降级"""
        client = self.get_client(role)
        try:
            return await client.generate_with_retry(
                messages=messages,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except Exception as primary_error:
            # 尝试降级
            config = self._configs.get(role)
            if config and config.fallback_model:
                logger.warning(
                    f"角色 '{role}' 主模型失败: {primary_error}. "
                    f"降级到 {config.fallback_provider or config.provider.value}:{config.fallback_model}"
                )
                fallback_config = LLMConfig(
                    provider=LLMProvider(config.fallback_provider) if config.fallback_provider else config.provider,
                    model=config.fallback_model,
                    api_key=config.api_key,
                    base_url=config.base_url,
                    max_tokens=config.max_tokens,
                    temperature=config.temperature,
                    timeout=config.timeout,
                    max_retries=2,
                )
                fallback_client = create_llm_client(fallback_config)
                return await fallback_client.generate_with_retry(
                    messages=messages,
                    system_prompt=system_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )
            raise

    def get_all_usage(self) -> Dict[str, LLMUsage]:
        """获取所有角色的 token 用量"""
        return {role: client.get_total_usage() for role, client in self._clients.items()}

    def get_total_tokens(self) -> int:
        """获取总 token 用量"""
        return sum(c.get_total_usage().total_tokens for c in self._clients.values())
