import tempfile
import unittest
from datetime import date
from pathlib import Path

from app.data.database import initialize_database
from app.data.pantry_repository import PantryRepository


class PantryRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = str(Path(self.temp_dir.name) / "test.db")
        initialize_database(self.database_path)
        self.repository = PantryRepository(self.database_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def sample_item(self):
        return {
            "name": "Oats",
            "category": "Grains",
            "quantity": 1.5,
            "unit": "kg",
            "purchase_date": date.today().isoformat(),
            "expiry_date": None,
            "notes": "Test record",
        }

    def test_create_get_update_and_delete(self):
        item_id = self.repository.create_item(self.sample_item())
        item = self.repository.get_item(item_id)
        self.assertEqual(item.name, "Oats")
        self.assertEqual(item.quantity, 1.5)

        updated = self.sample_item()
        updated["quantity"] = 2
        updated["notes"] = "Updated record"
        self.assertTrue(self.repository.update_item(item_id, updated))
        self.assertEqual(self.repository.get_item(item_id).quantity, 2)
        self.assertTrue(self.repository.delete_item(item_id))
        self.assertIsNone(self.repository.get_item(item_id))

    def test_search_and_category_filter(self):
        self.repository.create_item(self.sample_item())
        self.assertEqual(len(self.repository.list_items(search=" oat ".strip())), 1)
        self.assertEqual(len(self.repository.list_items(category="Fruits")), 0)


if __name__ == "__main__":
    unittest.main()
