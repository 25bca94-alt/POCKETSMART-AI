"""
PocketSmartAI product catalog.

This module contains the built-in catalog used by the
recommendation service.
"""

from typing import Any


CATALOG: list[dict[str, Any]] = [
    {
        "id": 1,
        "name": "Minimalist Gold Necklace",
        "category": "jewelry",
        "subcategory": "necklace",
        "price": 2499,
        "description": "Simple gold-finish necklace suitable for everyday wear.",
        "tags": ["minimal", "gold", "casual", "daily"],
    },
    {
        "id": 2,
        "name": "Pearl Pendant Set",
        "category": "jewelry",
        "subcategory": "necklace",
        "price": 3499,
        "description": "Elegant pearl pendant set for special occasions.",
        "tags": ["pearl", "elegant", "party", "traditional"],
    },
    {
        "id": 3,
        "name": "Traditional Jhumka Earrings",
        "category": "jewelry",
        "subcategory": "earrings",
        "price": 1899,
        "description": "Traditional jhumka-style earrings with a classic design.",
        "tags": ["jhumka", "traditional", "ethnic", "wedding"],
    },
    {
        "id": 4,
        "name": "Modern Stud Earrings",
        "category": "jewelry",
        "subcategory": "earrings",
        "price": 999,
        "description": "Small modern stud earrings for everyday use.",
        "tags": ["stud", "modern", "minimal", "daily"],
    },
    {
        "id": 5,
        "name": "Compact Living Room Setup",
        "category": "home",
        "subcategory": "living-room",
        "price": 25000,
        "description": "Space-efficient living room arrangement for small homes.",
        "tags": ["compact", "modern", "small-space", "living"],
    },
    {
        "id": 6,
        "name": "Cozy Bedroom Setup",
        "category": "home",
        "subcategory": "bedroom",
        "price": 30000,
        "description": "Comfortable bedroom arrangement with practical storage.",
        "tags": ["cozy", "bedroom", "storage", "modern"],
    },
    {
        "id": 7,
        "name": "Budget Birthday Party",
        "category": "party",
        "subcategory": "birthday",
        "price": 10000,
        "description": "Simple birthday party plan for a small group.",
        "tags": ["birthday", "budget", "small", "family"],
    },
    {
        "id": 8,
        "name": "Elegant Dinner Party",
        "category": "party",
        "subcategory": "dinner",
        "price": 25000,
        "description": "Elegant dinner party setup with decoration and menu ideas.",
        "tags": ["dinner", "elegant", "friends", "decoration"],
    },
]


def get_catalog() -> list[dict[str, Any]]:
    """
    Return a copy of the complete catalog.
    """
    return [item.copy() for item in CATALOG]


def get_catalog_by_category(
    category: str,
) -> list[dict[str, Any]]:
    """
    Return catalog items belonging to a category.
    """

    category_normalized = category.strip().lower()

    return [
        item.copy()
        for item in CATALOG
        if item["category"].lower() == category_normalized
    ]


def get_catalog_item(
    item_id: int,
) -> dict[str, Any] | None:
    """
    Return one catalog item by ID.
    """

    for item in CATALOG:
        if item["id"] == item_id:
            return item.copy()

    return None