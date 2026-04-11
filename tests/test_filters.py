from pipeline.sources.filters import keyword_filter
from pipeline.sources.rss import RawArticle


def _article(title: str, description: str = "") -> RawArticle:
    return RawArticle(
        title=title,
        url="https://example.com",
        source="Test",
        description=description,
        pub_date="2026-03-23",
    )


def test_keyword_filter_matches_title_and_description():
    articles = [
        _article("EU Loot Box Regulation"),
        _article("New Policy", description="FTC announces gaming probe"),
        _article("Cooking Recipes for Spring"),
    ]
    result = keyword_filter(articles, ["loot box", "FTC"])
    assert [article.title for article in result] == ["EU Loot Box Regulation", "New Policy"]


def test_keyword_filter_returns_all_without_keywords():
    articles = [_article("Anything")]
    assert keyword_filter(articles, []) == articles


def test_keyword_filter_enforces_word_boundaries():
    articles = [
        _article("This email was sent yesterday"),
        _article("The CEO said", description="again and again"),
        _article("New AI regulation proposed"),
    ]
    result = keyword_filter(articles, ["AI"])
    assert len(result) == 1
    assert result[0].title == "New AI regulation proposed"


def test_keyword_filter_case_insensitive():
    articles = [
        _article("Gaming LAWSUIT filed today"),
        _article("A lawsuit is pending"),
    ]
    result = keyword_filter(articles, ["lawsuit"])
    assert len(result) == 2


def test_keyword_filter_multi_word_keywords():
    articles = [
        _article("LOOT BOX regulations tightened"),
        _article("Loot box proposal"),
        _article("Loot and box separate"),
    ]
    result = keyword_filter(articles, ["loot box"])
    assert [article.title for article in result] == [
        "LOOT BOX regulations tightened",
        "Loot box proposal",
    ]
