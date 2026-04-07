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
    return BriefingNode(
        title=article.title,
        url=article.url,
        source=article.source,
        pub_date=article.pub_date,
        category=classification.category,
        summary_ko=summary.summary_ko,
        event=event,
        event_key=compute_event_key(
            jurisdiction=event.jurisdiction.value,
            actors=event.actors,
            object_=event.object,
            action=event.action,
        ),
        is_primary=True,
        title_ko=summary.title_ko,
    )

