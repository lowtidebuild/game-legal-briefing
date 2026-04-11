import os
import tempfile

import yaml

from pipeline.config import load_config


def test_load_config_from_file():
    data = {
        "llm": {"provider": "gemini", "model": "gemini-3.1-flash-lite", "max_retries": 2},
        "sources": {
            "tier_a": [{"name": "Test", "url": "https://example.com/feed"}],
            "tier_b": [],
            "tier_c": [{"name": "Tier C", "url": "https://example.com/html"}],
        },
        "pipeline": {"top_n": 10, "categories": ["IP", "ETC"]},
        "dedup": {"retention_days": 30},
        "site": {"base_url": "/game-legal-briefing"},
        "email": {
            "subject_prefix": "[Test]",
            "web_url": "https://example.com/briefing",
        },
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as handle:
        yaml.safe_dump(data, handle)
        path = handle.name
    try:
        cfg = load_config(path)
        assert cfg.llm.provider == "gemini"
        assert cfg.pipeline.top_n == 10
        assert cfg.sources.tier_a[0].name == "Test"
        assert cfg.sources.tier_c[0].name == "Tier C"
        assert cfg.site.base_url == "/game-legal-briefing"
        assert cfg.email.web_url == "https://example.com/briefing"
    finally:
        os.unlink(path)


def test_config_exposes_env_vars(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "test-key-123")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as handle:
        yaml.safe_dump({"sources": {"tier_a": [], "tier_b": []}}, handle)
        path = handle.name
    try:
        cfg = load_config(path)
        assert cfg.google_api_key == "test-key-123"
    finally:
        os.unlink(path)
