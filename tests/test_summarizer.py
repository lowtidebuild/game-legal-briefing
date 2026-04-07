from unittest.mock import MagicMock

from pipeline.intelligence.summarizer import SummaryResult, summarize_article
from pipeline.llm.base import LLMProvider
from pipeline.sources.rss import RawArticle


def _article() -> RawArticle:
    return RawArticle(
        title="EU Enacts Loot Box Regulation",
        url="https://example.com/eu-lootbox",
        source="GamesIndustry.biz",
        description="The European Union has enacted new regulations.",
        pub_date="2026-03-23",
    )


def test_summarize_returns_summary_result():
    mock_llm = MagicMock(spec=LLMProvider)
    mock_llm.generate_json.return_value = {
        "title_ko": "EU, 루트박스 규제 확정",
        "summary_ko": ["EU가 루트박스 규제를 확정했다.", "2026년 3분기부터 시행 예정.", "게임사 공시 의무화."]
    }
    result = summarize_article(_article(), mock_llm)
    assert isinstance(result, SummaryResult)
    assert result.title_ko == "EU, 루트박스 규제 확정"
    assert len(result.summary_ko) == 3


def test_summarize_fallback_on_failure():
    mock_llm = MagicMock(spec=LLMProvider)
    mock_llm.generate_json.side_effect = Exception("LLM failed")
    result = summarize_article(_article(), mock_llm)
    assert isinstance(result, SummaryResult)
    assert result.title_ko == ""
    assert result.summary_ko == ["EU Enacts Loot Box Regulation"]
