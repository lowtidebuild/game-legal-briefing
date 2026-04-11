from __future__ import annotations

import logging
import re
from datetime import datetime, timedelta

from pipeline.sources.rss import RawArticle

logger = logging.getLogger(__name__)


def keyword_filter(articles: list[RawArticle], keywords: list[str]) -> list[RawArticle]:
    """
    Keep only articles matching at least one keyword as a whole word.

    Uses regex word boundaries for whole-word matching, case-insensitive.
    Returns the input list unchanged if keywords are empty.
    """
    if not keywords:
        return articles

    pattern = re.compile(
        "|".join(r"\b" + re.escape(keyword) + r"\b" for keyword in keywords),
        re.IGNORECASE,
    )
    filtered = [
        article
        for article in articles
        if pattern.search(f"{article.title} {article.description}")
    ]
    logger.info(
        "Keyword filter (%d keywords) reduced %d articles to %d",
        len(keywords),
        len(articles),
        len(filtered),
    )
    return filtered


def recency_filter(articles: list[RawArticle], max_age_days: int = 7) -> list[RawArticle]:
    """Drop articles older than max_age_days."""
    cutoff = (datetime.now() - timedelta(days=max_age_days)).strftime("%Y-%m-%d")
    filtered = [
        article for article in articles
        if article.pub_date >= cutoff or not article.pub_date
    ]
    logger.info("Recency filter (%d days) reduced %d articles to %d", max_age_days, len(articles), len(filtered))
    return filtered
