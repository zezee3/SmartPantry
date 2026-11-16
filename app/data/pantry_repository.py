"""Database operations for pantry records."""

from contextlib import contextmanager

from app.data.database import connect_db
from app.models.food_item import FoodItem


class PantryRepository:
    """Keeps SQL operations in one place so routes do not query SQLite directly."""

    def __init__(self, database_path):
        self.database_path = database_path

    @contextmanager
    def _connection(self):
        connection = connect_db(self.database_path)
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def list_items(self, search="", category=""):
        query = "SELECT * FROM food_items WHERE 1 = 1"
        values = []

        if search:
            query += " AND name LIKE ?"
            values.append(f"%{search}%")

        if category:
            query += " AND category = ?"
            values.append(category)

        query += " ORDER BY expiry_date IS NULL, expiry_date ASC, name COLLATE NOCASE"

        with self._connection() as connection:
            rows = connection.execute(query, values).fetchall()
        return [FoodItem.from_row(row) for row in rows]

    def get_item(self, item_id):
        with self._connection() as connection:
            row = connection.execute(
                "SELECT * FROM food_items WHERE id = ?", (item_id,)
            ).fetchone()
        return FoodItem.from_row(row) if row else None

    def create_item(self, item_data):
        sql = """\
            INSERT INTO food_items
                (name, category, quantity, unit, purchase_date, expiry_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        values = (
            item_data["name"],
            item_data["category"],
            item_data["quantity"],
            item_data["unit"],
            item_data["purchase_date"],
            item_data["expiry_date"],
            item_data["notes"],
        )
        with self._connection() as connection:
            cursor = connection.execute(sql, values)
            return cursor.lastrowid

    def update_item(self, item_id, item_data):
        sql = """\
            UPDATE food_items
            SET name = ?, category = ?, quantity = ?, unit = ?,
                purchase_date = ?, expiry_date = ?, notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        values = (
            item_data["name"],
            item_data["category"],
            item_data["quantity"],
            item_data["unit"],
            item_data["purchase_date"],
            item_data["expiry_date"],
            item_data["notes"],
            item_id,
        )
        with self._connection() as connection:
            cursor = connection.execute(sql, values)
            return cursor.rowcount > 0

    def delete_item(self, item_id):
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM food_items WHERE id = ?", (item_id,)
            )
            return cursor.rowcount > 0

    def count_items(self):
        with self._connection() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS item_count FROM food_items"
            ).fetchone()
        return row["item_count"]
