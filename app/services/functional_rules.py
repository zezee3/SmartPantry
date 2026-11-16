"""Pure functions used to summarize pantry records."""

from dataclasses import dataclass
from datetime import date
from functools import reduce

from app.models.food_item import FoodItem


@dataclass(frozen=True)
class ItemStatus:
    """A read-only view that combines an item with calculated status details."""

    item: FoodItem
    days_remaining: int | None
    expiry_status: str
    priority: str
    logic_engine: str


def days_until_expiry(expiry_date, today=None):
    """Return the number of days until expiry without changing the input item."""
    if expiry_date is None:
        return None
    reference_date = today or date.today()
    return (expiry_date - reference_date).days


def fallback_classification(days_remaining):
    """Simple Python fallback used when SWI-Prolog is not installed."""
    if days_remaining is None:
        return "no_expiry_date", "normal"
    if days_remaining < 0:
        return "expired", "review"
    if days_remaining <= 3:
        return "expiring_soon", "high"
    return "fresh", "normal"


def filter_by_status(item_views, status):
    """Return a new list containing only views with the requested status."""
    return list(filter(lambda view: view.expiry_status == status, item_views))


def summarize_inventory(item_views):
    """Build dashboard totals using map, filter, and reduce."""
    statuses = list(map(lambda view: view.expiry_status, item_views))
    quantities = map(lambda view: view.item.quantity, item_views)
    total_quantity = reduce(lambda total, value: total + value, quantities, 0.0)
    categories = set(map(lambda view: view.item.category, item_views))

    return {
        "total_items": len(item_views),
        "expired": len(list(filter(lambda status: status == "expired", statuses))),
        "expiring_soon": len(
            list(filter(lambda status: status == "expiring_soon", statuses))
        ),
        "category_count": len(categories),
        "total_quantity": total_quantity,
    }
