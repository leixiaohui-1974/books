"""
测试 API 端点 — FastAPI 路由覆盖

注意：需要 OpenManus 完整依赖。如缺少依赖则自动跳过。
"""

import pytest

try:
    from fastapi.testclient import TestClient
    from hydroscribe.api.app import app
    HAS_DEPS = True
except (ImportError, Exception):
    HAS_DEPS = False

pytestmark = pytest.mark.skipif(not HAS_DEPS, reason="OpenManus 依赖不完整")


@pytest.fixture
def client():
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "uptime_seconds" in data


class TestStatusEndpoint:
    def test_status_returns_200(self, client):
        resp = client.get("/api/status")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "running"
        assert "orchestrator" in data
        assert "skill_types" in data

    def test_status_has_skill_types(self, client):
        resp = client.get("/api/status")
        skills = resp.json()["skill_types"]
        assert "BK" in skills
        assert "SCI" in skills
        assert len(skills) == 9


class TestBooksEndpoint:
    def test_list_books(self, client):
        resp = client.get("/api/books")
        assert resp.status_code == 200
        assert "books" in resp.json()


class TestSkillsEndpoint:
    def test_list_skills(self, client):
        resp = client.get("/api/skills")
        assert resp.status_code == 200
        skills = resp.json()["skills"]
        assert "BK" in skills
        assert skills["BK"]["reviewer_count"] == 4

    def test_all_skills_have_thresholds(self, client):
        resp = client.get("/api/skills")
        for skill_id, skill_data in resp.json()["skills"].items():
            assert "threshold" in skill_data


class TestAgentsEndpoint:
    def test_list_agents(self, client):
        resp = client.get("/api/agents")
        assert resp.status_code == 200
        data = resp.json()
        assert "writers" in data
        assert "reviewers" in data


class TestMetricsEndpoint:
    def test_metrics_returns_200(self, client):
        resp = client.get("/api/metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert "uptime_seconds" in data
        assert "agents" in data
        assert "llm" in data
        assert "events" in data

    def test_metrics_agent_counts(self, client):
        resp = client.get("/api/metrics")
        agents = resp.json()["agents"]
        assert "writers_active" in agents
        assert "tasks_active" in agents


class TestConfigEndpoint:
    def test_config_returns_200(self, client):
        resp = client.get("/api/config")
        assert resp.status_code == 200
        data = resp.json()
        assert "llm" in data
        assert "orchestrator" in data
        # API Key 应该被脱敏
        assert "api_key_set" in data["llm"]
        assert "api_key" not in data["llm"]


class TestLLMUsageEndpoint:
    def test_llm_usage_returns_200(self, client):
        resp = client.get("/api/llm/usage")
        assert resp.status_code == 200
        data = resp.json()
        assert "usage" in data
        assert "total_tokens" in data


class TestGatesEndpoint:
    def test_pending_gates(self, client):
        resp = client.get("/api/gates/pending")
        assert resp.status_code == 200
        assert "pending_gates" in resp.json()


class TestStartTask:
    def test_start_task_returns_200(self, client):
        resp = client.post("/api/tasks/start", json={
            "book_id": "T1-CN",
            "skill_type": "BK",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "started"
        assert data["book_id"] == "T1-CN"


class TestDashboard:
    def test_dashboard_returns_html(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "HydroScribe" in resp.text
