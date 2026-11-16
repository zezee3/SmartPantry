"""Immutable domain model for a pantry food item."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class FoodItem:
    id: int | None
    name: str
    category: str
    quantity: float
    unit: str
    purchase_date: date
    expiry_date: date | None
    notes: str = ""

    @classmethod
    def from_row(cls, row):
        expiry_value = row["expiry_date"]
        return cls(
            id=row["id"],
            name=row["name"],
            category=row["category"],
            quantity=float(row["quantity"]),
            unit=row["unit"],
            purchase_date=date.fromisoformat(row["purchase_date"]),
            expiry_date=date.fromisoformat(expiry_value) if expiry_value else None,
            notes=row["notes"] or "",
        )
