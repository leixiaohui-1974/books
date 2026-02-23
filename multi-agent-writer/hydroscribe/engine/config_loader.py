"""
TOML 配置加载器 — 统一管理 HydroScribe 所有配置

配置层级（后者覆盖前者）：
1. 内置默认值
2. config/config.toml 文件
3. 环境变量（HYDROSCRIBE_ 前缀）

配置文件结构参见 config/config.toml
"""

import logging
import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

logger = logging.getLogger("hydroscribe.config")


def _load_toml(path: str) -> Dict[str, Any]:
    """加载 TOML 文件，兼容 Python 3.10 (tomllib) 和 3.10 以下 (tomli)"""
    if not os.path.exists(path):
        return {}
    try:
        import tomllib
        with open(path, "rb") as f:
            return tomllib.load(f)
    except ImportError:
        pass
    try:
        import tomli
        with open(path, "rb") as f:
            return tomli.load(f)
    except ImportError:
        pass
    # 最后降级到简单解析
    logger.warning("tomllib/tomli 不可用，跳过 TOML 配置加载")
    return {}


@dataclass
class ServerConfig:
    """API 服务配置"""
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    cors_origins: list = field(default_factory=lambda: ["*"])
    log_level: str = "info"


@dataclass
class LLMRoleConfig:
    """单个角色的 LLM 配置"""
    provider: str = "openai"
    model: str = ""
    api_key: str = ""
    base_url: str = ""
    max_tokens: int = 4096
    temperature: float = 0.3
    top_p: float = 0.95
    timeout: int = 120
    max_retries: int = 3
    retry_delay: float = 2.0
    fallback_model: str = ""
    fallback_provider: str = ""


@dataclass
class OrchestratorConfig:
    """编排器配置"""
    gate_mode: str = "auto"  # auto | human | hybrid
    gate_timeout_seconds: int = 3600  # 人工门控超时(秒)，默认1小时
    gate_timeout_action: str = "reject"  # reject | approve — 超时后的默认动作
    review_weight: float = 0.80
    utility_weight: float = 0.20
    coordination_mode: str = "specialist"  # specialist | master_slave
    max_concurrent_writers: int = 3
    max_concurrent_reviewers: int = 8
    max_feedback_tokens: int = 4000  # 反馈截断上限(字符)
    dry_run: bool = False  # True = 跳过 LLM 调用，用占位内容验证管线


@dataclass
class DockerConfig:
    """容器化配置"""
    network_name: str = "hydroscribe_network"
    openclaw_port: int = 3000
    api_port: int = 8000


@dataclass
class HydroScribeConfig:
    """HydroScribe 主配置"""
    books_root: str = "/home/user/books"
    data_dir: str = "./data"
    log_level: str = "info"

    server: ServerConfig = field(default_factory=ServerConfig)
    orchestrator: OrchestratorConfig = field(default_factory=OrchestratorConfig)
    docker: DockerConfig = field(default_factory=DockerConfig)

    # LLM 配置：按角色分
    llm_default: LLMRoleConfig = field(default_factory=LLMRoleConfig)
    llm_writer: Optional[LLMRoleConfig] = None
    llm_reviewer: Optional[LLMRoleConfig] = None
    llm_utility: Optional[LLMRoleConfig] = None

    # OpenClaw 集成
    openclaw_enabled: bool = False
    openclaw_gateway_url: str = "http://openclaw_gateway:3000"

    def get_llm_config(self, role: str = "default") -> LLMRoleConfig:
        """获取指定角色的 LLM 配置，不存在则回退到 default"""
        role_map = {
            "writer": self.llm_writer,
            "reviewer": self.llm_reviewer,
            "utility": self.llm_utility,
        }
        config = role_map.get(role)
        if config and config.model:
            return config
        return self.llm_default


def _apply_env_overrides(config: HydroScribeConfig) -> HydroScribeConfig:
    """从环境变量覆盖配置（HYDROSCRIBE_ 前缀）"""
    env_map = {
        "HYDROSCRIBE_BOOKS_ROOT": ("books_root", str),
        "HYDROSCRIBE_LOG_LEVEL": ("log_level", str),
        "HYDROSCRIBE_SERVER_HOST": None,
        "HYDROSCRIBE_SERVER_PORT": None,
        "HYDROSCRIBE_GATE_MODE": None,
        # LLM 配置
        "HYDROSCRIBE_LLM_PROVIDER": None,
        "HYDROSCRIBE_LLM_MODEL": None,
        "HYDROSCRIBE_LLM_API_KEY": None,
        "HYDROSCRIBE_LLM_BASE_URL": None,
        # 阿里云百炼快捷配置
        "DASHSCOPE_API_KEY": None,
        # OpenClaw
        "HYDROSCRIBE_OPENCLAW_ENABLED": None,
        "HYDROSCRIBE_OPENCLAW_URL": None,
    }

    # 直接映射
    for env_key, attr_info in env_map.items():
        val = os.environ.get(env_key)
        if val and attr_info:
            attr_name, attr_type = attr_info
            setattr(config, attr_name, attr_type(val))

    # Server 配置
    if os.environ.get("HYDROSCRIBE_SERVER_HOST"):
        config.server.host = os.environ["HYDROSCRIBE_SERVER_HOST"]
    if os.environ.get("HYDROSCRIBE_SERVER_PORT"):
        config.server.port = int(os.environ["HYDROSCRIBE_SERVER_PORT"])

    # Gate mode
    if os.environ.get("HYDROSCRIBE_GATE_MODE"):
        config.orchestrator.gate_mode = os.environ["HYDROSCRIBE_GATE_MODE"]

    # LLM default 配置
    if os.environ.get("HYDROSCRIBE_LLM_PROVIDER"):
        config.llm_default.provider = os.environ["HYDROSCRIBE_LLM_PROVIDER"]
    if os.environ.get("HYDROSCRIBE_LLM_MODEL"):
        config.llm_default.model = os.environ["HYDROSCRIBE_LLM_MODEL"]
    if os.environ.get("HYDROSCRIBE_LLM_API_KEY"):
        config.llm_default.api_key = os.environ["HYDROSCRIBE_LLM_API_KEY"]
    if os.environ.get("HYDROSCRIBE_LLM_BASE_URL"):
        config.llm_default.base_url = os.environ["HYDROSCRIBE_LLM_BASE_URL"]

    # 百炼快捷方式
    dashscope_key = os.environ.get("DASHSCOPE_API_KEY")
    if dashscope_key and not config.llm_default.api_key:
        config.llm_default.provider = "alibaba_bailian"
        config.llm_default.api_key = dashscope_key
        if not config.llm_default.model:
            config.llm_default.model = "qwen-plus"
        if not config.llm_default.base_url:
            config.llm_default.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    # OpenClaw
    if os.environ.get("HYDROSCRIBE_OPENCLAW_ENABLED"):
        config.openclaw_enabled = os.environ["HYDROSCRIBE_OPENCLAW_ENABLED"].lower() in ("true", "1", "yes")
    if os.environ.get("HYDROSCRIBE_OPENCLAW_URL"):
        config.openclaw_gateway_url = os.environ["HYDROSCRIBE_OPENCLAW_URL"]

    # Dry-run 模式
    if os.environ.get("HYDROSCRIBE_DRY_RUN"):
        config.orchestrator.dry_run = os.environ["HYDROSCRIBE_DRY_RUN"].lower() in ("true", "1", "yes")

    return config


def _dict_to_llm_role_config(d: Dict[str, Any]) -> LLMRoleConfig:
    """将字典转换为 LLMRoleConfig"""
    return LLMRoleConfig(
        provider=d.get("provider", "openai"),
        model=d.get("model", ""),
        api_key=d.get("api_key", ""),
        base_url=d.get("base_url", ""),
        max_tokens=d.get("max_tokens", 4096),
        temperature=d.get("temperature", 0.3),
        top_p=d.get("top_p", 0.95),
        timeout=d.get("timeout", 120),
        max_retries=d.get("max_retries", 3),
        retry_delay=d.get("retry_delay", 2.0),
        fallback_model=d.get("fallback_model", ""),
        fallback_provider=d.get("fallback_provider", ""),
    )


def load_config(config_path: Optional[str] = None) -> HydroScribeConfig:
    """
    加载配置 — 主入口

    优先级：环境变量 > config.toml > 内置默认值
    """
    config = HydroScribeConfig()

    # 寻找配置文件
    if not config_path:
        candidates = [
            os.path.join(os.getcwd(), "config", "config.toml"),
            os.path.join(os.getcwd(), "config.toml"),
            os.path.expanduser("~/.hydroscribe/config.toml"),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                config_path = candidate
                break

    if config_path and os.path.exists(config_path):
        logger.info(f"加载配置文件: {config_path}")
        toml_data = _load_toml(config_path)

        # 基础配置
        config.books_root = toml_data.get("books_root", config.books_root)
        config.data_dir = toml_data.get("data_dir", config.data_dir)
        config.log_level = toml_data.get("log_level", config.log_level)

        # Server
        if "server" in toml_data:
            s = toml_data["server"]
            config.server.host = s.get("host", config.server.host)
            config.server.port = s.get("port", config.server.port)
            config.server.workers = s.get("workers", config.server.workers)
            config.server.log_level = s.get("log_level", config.server.log_level)

        # Orchestrator
        if "orchestrator" in toml_data:
            o = toml_data["orchestrator"]
            config.orchestrator.gate_mode = o.get("gate_mode", config.orchestrator.gate_mode)
            config.orchestrator.review_weight = o.get("review_weight", config.orchestrator.review_weight)
            config.orchestrator.utility_weight = o.get("utility_weight", config.orchestrator.utility_weight)
            config.orchestrator.coordination_mode = o.get("coordination_mode", config.orchestrator.coordination_mode)
            config.orchestrator.max_concurrent_writers = o.get("max_concurrent_writers", config.orchestrator.max_concurrent_writers)
            config.orchestrator.max_concurrent_reviewers = o.get("max_concurrent_reviewers", config.orchestrator.max_concurrent_reviewers)

        # LLM 配置
        if "llm" in toml_data:
            config.llm_default = _dict_to_llm_role_config(toml_data["llm"])
        if "llm.writer" in toml_data:
            config.llm_writer = _dict_to_llm_role_config(toml_data["llm.writer"])
        elif "llm_writer" in toml_data:
            config.llm_writer = _dict_to_llm_role_config(toml_data["llm_writer"])
        if "llm.reviewer" in toml_data:
            config.llm_reviewer = _dict_to_llm_role_config(toml_data["llm.reviewer"])
        elif "llm_reviewer" in toml_data:
            config.llm_reviewer = _dict_to_llm_role_config(toml_data["llm_reviewer"])
        if "llm.utility" in toml_data:
            config.llm_utility = _dict_to_llm_role_config(toml_data["llm.utility"])
        elif "llm_utility" in toml_data:
            config.llm_utility = _dict_to_llm_role_config(toml_data["llm_utility"])

        # OpenClaw
        if "openclaw" in toml_data:
            oc = toml_data["openclaw"]
            config.openclaw_enabled = oc.get("enabled", False)
            config.openclaw_gateway_url = oc.get("gateway_url", config.openclaw_gateway_url)

        # Docker
        if "docker" in toml_data:
            dk = toml_data["docker"]
            config.docker.network_name = dk.get("network_name", config.docker.network_name)
            config.docker.openclaw_port = dk.get("openclaw_port", config.docker.openclaw_port)
            config.docker.api_port = dk.get("api_port", config.docker.api_port)

    # 环境变量覆盖
    config = _apply_env_overrides(config)

    return config


# 全局单例
_global_config: Optional[HydroScribeConfig] = None


def get_config() -> HydroScribeConfig:
    """获取全局配置单例"""
    global _global_config
    if _global_config is None:
        _global_config = load_config()
    return _global_config


def set_config(config: HydroScribeConfig):
    """设置全局配置"""
    global _global_config
    _global_config = config
