"""
Recommendation service for PocketSmartAI.
"""

from typing import Any

from app.services.catalog import get_catalog


def _safe_float(value: Any) -> float | None:
    """
    Convert a value to float when possible.
    """

    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _calculate_score(
    item: dict[str, Any],
    query: str,
    budget: float | None,
    category: str | None,
) -> int:
    """
    Calculate a simple recommendation score.
    """

    score = 0

    query_text = query.strip().lower()

    category_text = (
        category.strip().lower()
        if category
        else ""
    )

    item_category = str(
        item.get("category", "")
    ).lower()

    item_name = str(
        item.get("name", "")
    ).lower()

    item_description = str(
        item.get("description", "")
    ).lower()

    item_tags = [
        str(tag).lower()
        for tag in item.get("tags", [])
    ]

    # Category match
    if category_text:
        if item_category == category_text:
            score += 40

    # Keyword matching
    if query_text:
        query_words = set(
            query_text.replace(",", " ").split()
        )

        searchable_text = " ".join(
            [
                item_name,
                item_description,
                " ".join(item_tags),
            ]
        )

        for word in query_words:
            if len(word) >= 2 and word in searchable_text:
                score += 10

    # Budget matching
    price = _safe_float(item.get("price"))

    if budget is not None and price is not None:
        if price <= budget:
            score += 30

            # Prefer items that use the budget reasonably.
            if budget > 0:
                ratio = price / budget

                if ratio >= 0.5:
                    score += 5

        else:
            # Do not completely discard an item,
            # but reduce its score if it exceeds budget.
            score -= 20

    return score


def get_recommendations(
    query: str = "",
    category: str | None = None,
    budget: float | None = None,
    limit: int = 5,
) -> list[dict[str, Any]]:
    """
    Return catalog recommendations based on user preferences.
    """

    if limit < 1:
        limit = 1

    if limit > 20:
        limit = 20

    catalog = get_catalog()

    scored_items: list[dict[str, Any]] = []

    for item in catalog:
        score = _calculate_score(
            item=item,
            query=query,
            budget=budget,
            category=category,
        )

        result = item.copy()
        result["score"] = score

        scored_items.append(result)

    scored_items.sort(
        key=lambda item: (
            item["score"],
            -float(item.get("price", 0)),
        ),
        reverse=True,
    )

    return scored_items[:limit]