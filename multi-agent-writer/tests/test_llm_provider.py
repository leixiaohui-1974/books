"""
Tests for LLM Provider Abstraction Layer and Config Loader
"""

import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from hydroscribe.engine.llm_provider import (
    LLMConfig, LLMManager, LLMProvider, LLMResponse, LLMUsage,
    AlibabaBailianClient, OpenAIClient, AnthropicClient, LocalLLMClient,
    create_llm_client, create_llm_from_dict,
)
from hydroscribe.engine.config_loader import (
    HydroScribeConfig, LLMRoleConfig, OrchestratorConfig, ServerConfig,
    load_config, _apply_env_overrides, _dict_to_llm_role_config,
)


# ── LLMConfig Tests ────────────────────────────────────────────

class TestLLMConfig:
    def test_default_values(self):
        config = LLMConfig(provider=LLMProvider.OPENAI, model="gpt-4o")
        assert config.max_tokens == 4096
        assert config.temperature == 0.3
        assert config.max_retries == 3
        assert config.retry_delay == 2.0

    def test_alibaba_config(self):
        config = LLMConfig(
            provider=LLMProvider.ALIBABA_BAILIAN,
            model="qwen-plus",
            api_key="sk-test",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        assert config.provider == LLMProvider.ALIBABA_BAILIAN
        assert config.model == "qwen-plus"

    def test_fallback_config(self):
        config = LLMConfig(
            provider=LLMProvider.ALIBABA_BAILIAN,
            model="qwen-max",
            fallback_model="qwen-turbo",
            fallback_provider="alibaba_bailian",
        )
        assert config.fallback_model == "qwen-turbo"


# ── Factory Tests ──────────────────────────────────────────────

class TestCreateLLMClient:
    def test_create_alibaba(self):
        config = LLMConfig(
            provider=LLMProvider.ALIBABA_BAILIAN,
            model="qwen-plus",
            api_key="test-key",
        )
        client = create_llm_client(config)
        assert isinstance(client, AlibabaBailianClient)

    def test_create_openai(self):
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4o",
            api_key="test-key",
        )
        client = create_llm_client(config)
        assert isinstance(client, OpenAIClient)

    def test_create_anthropic(self):
        config = LLMConfig(
            provider=LLMProvider.ANTHROPIC,
            model="claude-sonnet-4-20250514",
            api_key="test-key",
        )
        client = create_llm_client(config)
        assert isinstance(client, AnthropicClient)

    def test_create_local(self):
        config = LLMConfig(
            provider=LLMProvider.LOCAL,
            model="qwen2.5:14b",
        )
        client = create_llm_client(config)
        assert isinstance(client, LocalLLMClient)

    def test_create_from_dict(self):
        d = {
            "provider": "alibaba_bailian",
            "model": "qwen-plus",
            "api_key": "test",
            "max_tokens": 8192,
        }
        client = create_llm_from_dict(d)
        assert isinstance(client, AlibabaBailianClient)
        assert client.config.max_tokens == 8192

    def test_invalid_provider(self):
        with pytest.raises(ValueError, match="不支持"):
            create_llm_from_dict({"provider": "invalid_provider", "model": "test"})


# ── LLMManager Tests ──────────────────────────────────────────

class TestLLMManager:
    def test_register_and_get(self):
        manager = LLMManager()
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4o",
            api_key="test",
        )
        manager.register("writer", config)
        client = manager.get_client("writer")
        assert isinstance(client, OpenAIClient)

    def test_fallback_to_default(self):
        manager = LLMManager()
        config = LLMConfig(
            provider=LLMProvider.OPENAI,
            model="gpt-4o",
            api_key="test",
        )
        manager.register("default", config)
        client = manager.get_client("nonexistent_role")
        assert isinstance(client, OpenAIClient)

    def test_no_default_raises(self):
        manager = LLMManager()
        with pytest.raises(RuntimeError, match="未找到"):
            manager.get_client("nonexistent")

    def test_multi_role_registration(self):
        manager = LLMManager()
        manager.register("writer", LLMConfig(
            provider=LLMProvider.ALIBABA_BAILIAN, model="qwen-max", api_key="k1"
        ))
        manager.register("reviewer", LLMConfig(
            provider=LLMProvider.ANTHROPIC, model="claude-sonnet-4-20250514", api_key="k2"
        ))
        assert isinstance(manager.get_client("writer"), AlibabaBailianClient)
        assert isinstance(manager.get_client("reviewer"), AnthropicClient)

    def test_total_tokens(self):
        manager = LLMManager()
        config = LLMConfig(
            provider=LLMProvider.LOCAL, model="test", api_key="k"
        )
        manager.register("default", config)
        assert manager.get_total_tokens() == 0


# ── LLMUsage Tests ────────────────────────────────────────────

class TestLLMUsage:
    def test_default(self):
        usage = LLMUsage()
        assert usage.prompt_tokens == 0
        assert usage.total_tokens == 0

    def test_tracking(self):
        usage = LLMUsage(prompt_tokens=100, completion_tokens=200, total_tokens=300)
        assert usage.total_tokens == 300


# ── Config Loader Tests ──────────────────────────────────────

class TestConfigLoader:
    def test_default_config(self):
        config = HydroScribeConfig()
        assert config.books_root == "/home/user/books"
        assert config.server.port == 8000
        assert config.orchestrator.gate_mode == "auto"
        assert config.orchestrator.coordination_mode == "specialist"

    def test_get_llm_config_default(self):
        config = HydroScribeConfig()
        config.llm_default = LLMRoleConfig(
            provider="alibaba_bailian", model="qwen-plus"
        )
        result = config.get_llm_config("writer")
        assert result.model == "qwen-plus"  # falls back to default

    def test_get_llm_config_role_specific(self):
        config = HydroScribeConfig()
        config.llm_default = LLMRoleConfig(model="default-model")
        config.llm_writer = LLMRoleConfig(model="writer-model")
        assert config.get_llm_config("writer").model == "writer-model"
        assert config.get_llm_config("reviewer").model == "default-model"

    def test_dict_to_role_config(self):
        d = {
            "provider": "anthropic",
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 8192,
            "temperature": 0.2,
        }
        rc = _dict_to_llm_role_config(d)
        assert rc.provider == "anthropic"
        assert rc.max_tokens == 8192
        assert rc.temperature == 0.2

    def test_env_overrides(self):
        config = HydroScribeConfig()
        with patch.dict(os.environ, {
            "HYDROSCRIBE_BOOKS_ROOT": "/test/books",
            "HYDROSCRIBE_GATE_MODE": "human",
            "HYDROSCRIBE_LLM_PROVIDER": "openai",
            "HYDROSCRIBE_LLM_MODEL": "gpt-4o",
        }):
            config = _apply_env_overrides(config)
        assert config.books_root == "/test/books"
        assert config.orchestrator.gate_mode == "human"
        assert config.llm_default.provider == "openai"
        assert config.llm_default.model == "gpt-4o"

    def test_dashscope_shortcut(self):
        config = HydroScribeConfig()
        with patch.dict(os.environ, {
            "DASHSCOPE_API_KEY": "sk-test-bailian",
        }, clear=False):
            config = _apply_env_overrides(config)
        assert config.llm_default.provider == "alibaba_bailian"
        assert config.llm_default.api_key == "sk-test-bailian"
        assert config.llm_default.model == "qwen-plus"

    def test_orchestrator_config(self):
        oc = OrchestratorConfig()
        assert oc.review_weight == 0.80
        assert oc.utility_weight == 0.20
        assert oc.max_concurrent_writers == 3
        assert oc.max_concurrent_reviewers == 8


# ── LLMProvider Enum Tests ────────────────────────────────────

class TestLLMProviderEnum:
    def test_all_providers(self):
        assert LLMProvider.ALIBABA_BAILIAN.value == "alibaba_bailian"
        assert LLMProvider.OPENAI.value == "openai"
        assert LLMProvider.ANTHROPIC.value == "anthropic"
        assert LLMProvider.LOCAL.value == "local"
        assert len(LLMProvider) == 4
