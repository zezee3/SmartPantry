"""Application service for pantry workflows and validation."""

from datetime import date
import math

from app.services.functional_rules import (
    ItemStatus,
    days_until_expiry,
    fallback_classification,
    summarize_inventory,
)

CATEGORIES = [
    "Bakery",
    "Beverages",
    "Canned goods",
    "Dairy",
    "Fruits",
    "Grains",
    "Meat",
    "Seafood",
    "Vegetables",
    "Other",
]

UNITS = ["pcs", "packs", "bottles", "cans", "kg", "g", "L", "ml", "boxes", "bags"]


class PantryService:
    """Coordinates validation, repository operations, and status calculation."""

    def __init__(self, repository, logic_engine):
        self.repository = repository
        self.logic_engine = logic_engine

    def get_item(self, item_id):
        return self.repository.get_item(item_id)

    def get_item_views(self, search="", category="", today=None):
        reference_date = today or date.today()
        items = self.repository.list_items(search=search, category=category)
        day_values = [days_until_expiry(item.expiry_date, reference_date) for item in items]
        logic_results = self.logic_engine.classify_many(day_values)

        views = []
        for item, days, result in zip(items, day_values, logic_results):
            if result is None:
                status, priority = fallback_classification(days)
                engine_name = "Python fallback"
            else:
                status = result.status
                priority = result.priority
                engine_name = result.engine
            views.append(
                ItemStatus(
                    item=item,
                    days_remaining=days,
                    expiry_status=status,
                    priority=priority,
                    logic_engine=engine_name,
                )
            )
        return views

    def get_dashboard_data(self, today=None):
        item_views = self.get_item_views(today=today)
        summary = summarize_inventory(item_views)
        attention_items = [
            view
            for view in item_views
            if view.expiry_status in ("expired", "expiring_soon")
        ]
        attention_items.sort(
            key=lambda view: (
                view.days_remaining is None,
                view.days_remaining if view.days_remaining is not None else 99999,
            )
        )
        engine_name = (
            item_views[0].logic_engine
            if item_views
            else self.logic_engine.engine_name
        )
        return summary, attention_items[:6], item_views, engine_name

    def create_item(self, form_data):
        item_data = self._validate_item_data(form_data)
        return self.repository.create_item(item_data)

    def update_item(self, item_id, form_data):
        item_data = self._validate_item_data(form_data)
        return self.repository.update_item(item_id, item_data)

    def delete_item(self, item_id):
        return self.repository.delete_item(item_id)

    @staticmethod
    def _validate_item_data(form_data):
        name = form_data.get("name", "").strip()
        category = form_data.get("category", "").strip()
        unit = form_data.get("unit", "pcs").strip()
        notes = form_data.get("notes", "").strip()

        if not name or len(name) > 80:
            raise ValueError("Enter a food name between 1 and 80 characters.")
        if category not in CATEGORIES:
            raise ValueError("Choose a valid food category.")
        if unit not in UNITS:
            raise ValueError("Choose a valid unit.")
        if len(notes) > 300:
            raise ValueError("Notes must be 300 characters or fewer.")

        try:
            quantity = float(form_data.get("quantity", ""))
        except (TypeError, ValueError):
            raise ValueError("Enter a valid quantity.") from None
        if not math.isfinite(quantity) or quantity <= 0 or quantity > 100000:
            raise ValueError("Quantity must be greater than 0 and no more than 100,000.")

        purchase_value = form_data.get("purchase_date", "").strip()
        expiry_value = form_data.get("expiry_date", "").strip()
        try:
            purchase_date = date.fromisoformat(purchase_value)
        except ValueError:
            raise ValueError("Enter a valid purchase date.") from None

        if expiry_value:
            try:
                date.fromisoformat(expiry_value)
            except ValueError:
                raise ValueError("Enter a valid expiration date.") from None
        else:
            expiry_value = None

        return {
            "name": name,
            "category": category,
            "quantity": quantity,
            "unit": unit,
            "purchase_date": purchase_date.isoformat(),
            "expiry_date": expiry_value,
            "notes": notes,
        }
