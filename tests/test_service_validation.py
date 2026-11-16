import unittest
from datetime import date

from app.services.pantry_service import PantryService


class PantryServiceValidationTests(unittest.TestCase):
    def valid_form(self):
        return {
            "name": "Oats",
            "category": "Grains",
            "quantity": "1.5",
            "unit": "kg",
            "purchase_date": date.today().isoformat(),
            "expiry_date": "",
            "notes": "Breakfast pantry item",
        }

    def test_valid_form_is_normalized(self):
        result = PantryService._validate_item_data(self.valid_form())
        self.assertEqual(result["name"], "Oats")
        self.assertEqual(result["quantity"], 1.5)
        self.assertIsNone(result["expiry_date"])

    def test_rejects_unknown_category(self):
        form = self.valid_form()
        form["category"] = "Unknown"
        with self.assertRaises(ValueError):
            PantryService._validate_item_data(form)

    def test_rejects_non_finite_quantity(self):
        form = self.valid_form()
        form["quantity"] = "nan"
        with self.assertRaises(ValueError):
            PantryService._validate_item_data(form)


if __name__ == "__main__":
    unittest.main()
