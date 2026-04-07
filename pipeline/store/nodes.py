from __future__ import annotations

from pipeline.intelligence.classifier import ClassificationResult
from pipeline.intelligence.dedup import compute_event_key
from pipeline.intelligence.summarizer import SummaryResult
from pipeline.models import BriefingNode
from pipeline.sources.rss import RawArticle


def assemble_node(
    article: RawArticle,
    classification: ClassificationResult,
    summary: SummaryResult,
) -> BriefingNode:
    """Assemble a full briefing node from the article and enrichment output."""
    event = classification.event
    # Prefer LLM-generated human-readable event_key, fall back to hash
    event_key = classification.event_key or compute_event_key(
        jurisdiction=event.jurisdiction.value,
        actors=event.actors,
        object_=event.object,
        action=event.action,
    )
    return BriefingNode(
        title=article.title,
        url=article.url,
        source=article.source,
        pub_date=article.pub_date,
        category=classification.category,
        summary_ko=summary.summary_ko,
        event=event,
        event_key=event_key,
        is_primary=True,
        title_ko=summary.title_ko,
    )

