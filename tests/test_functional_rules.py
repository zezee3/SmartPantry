import unittest
from datetime import date, timedelta
from types import SimpleNamespace

from app.services.functional_rules import (
    days_until_expiry,
    fallback_classification,
    filter_by_status,
    summarize_inventory,
)


class FunctionalRulesTests(unittest.TestCase):
    def test_days_until_expiry(self):
        today = date(2026, 11, 16)
        self.assertEqual(days_until_expiry(today + timedelta(days=2), today), 2)
        self.assertEqual(days_until_expiry(today - timedelta(days=1), today), -1)
        self.assertIsNone(days_until_expiry(None, today))

    def test_fallback_classification(self):
        self.assertEqual(fallback_classification(-1), ("expired", "review"))
        self.assertEqual(fallback_classification(3), ("expiring_soon", "high"))
        self.assertEqual(fallback_classification(8), ("fresh", "normal"))
        self.assertEqual(fallback_classification(None), ("no_expiry_date", "normal"))

    def test_summary_and_filter(self):
        views = [
            SimpleNamespace(expiry_status="expired", item=SimpleNamespace(quantity=1, category="Dairy")),
            SimpleNamespace(expiry_status="expiring_soon", item=SimpleNamespace(quantity=2, category="Fruits")),
            SimpleNamespace(expiry_status="fresh", item=SimpleNamespace(quantity=3, category="Dairy")),
        ]
        summary = summarize_inventory(views)
        self.assertEqual(summary["total_items"], 3)
        self.assertEqual(summary["expired"], 1)
        self.assertEqual(summary["expiring_soon"], 1)
        self.assertEqual(summary["category_count"], 2)
        self.assertEqual(summary["total_quantity"], 6)
        self.assertEqual(len(filter_by_status(views, "fresh")), 1)


if __name__ == "__main__":
    unittest.main()
