"""Add realistic demo records to the supplied SQLite database."""

import argparse
from datetime import date, timedelta

from dotenv import load_dotenv

from app import create_app
from app.data.pantry_repository import PantryRepository


def build_demo_items(today):
    return [
        {
            "name": "Fresh milk",
            "category": "Dairy",
            "quantity": 1,
            "unit": "L",
            "purchase_date": today.isoformat(),
            "expiry_date": (today + timedelta(days=2)).isoformat(),
            "notes": "Keep refrigerated.",
        },
        {
            "name": "Whole wheat bread",
            "category": "Bakery",
            "quantity": 1,
            "unit": "packs",
            "purchase_date": today.isoformat(),
            "expiry_date": (today + timedelta(days=1)).isoformat(),
            "notes": "Stored in the bread box.",
        },
        {
            "name": "Eggs",
            "category": "Dairy",
            "quantity": 12,
            "unit": "pcs",
            "purchase_date": (today - timedelta(days=4)).isoformat(),
            "expiry_date": (today + timedelta(days=12)).isoformat(),
            "notes": "One dozen.",
        },
        {
            "name": "Spinach",
            "category": "Vegetables",
            "quantity": 1,
            "unit": "bags",
            "purchase_date": (today - timedelta(days=5)).isoformat(),
            "expiry_date": (today - timedelta(days=1)).isoformat(),
            "notes": "Check condition and storage guidance.",
        },
        {
            "name": "Bananas",
            "category": "Fruits",
            "quantity": 6,
            "unit": "pcs",
            "purchase_date": (today - timedelta(days=1)).isoformat(),
            "expiry_date": (today + timedelta(days=3)).isoformat(),
            "notes": "Keep at room temperature until ripe.",
        },
        {
            "name": "Brown rice",
            "category": "Grains",
            "quantity": 2,
            "unit": "kg",
            "purchase_date": (today - timedelta(days=20)).isoformat(),
            "expiry_date": None,
            "notes": "Dry pantry storage.",
        },
        {
            "name": "Canned beans",
            "category": "Canned goods",
            "quantity": 3,
            "unit": "cans",
            "purchase_date": (today - timedelta(days=30)).isoformat(),
            "expiry_date": (today + timedelta(days=180)).isoformat(),
            "notes": "Store in a cool, dry place.",
        },
        {
            "name": "Chicken breast",
            "category": "Meat",
            "quantity": 500,
            "unit": "g",
            "purchase_date": today.isoformat(),
            "expiry_date": today.isoformat(),
            "notes": "Follow package storage instructions.",
        },
    ]


def main():
    parser = argparse.ArgumentParser(description="Seed the SmartPantry demo database.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete current pantry records before adding demo records.",
    )
    args = parser.parse_args()

    load_dotenv()
    app = create_app()
    with app.app_context():
        repository = PantryRepository(app.config["DATABASE_PATH"])
        if args.reset:
            for item in repository.list_items():
                repository.delete_item(item.id)
        elif repository.count_items() > 0:
            print("The database already contains records. Use --reset to replace them.")
            return

        for item in build_demo_items(date.today()):
            repository.create_item(item)

        print("Added 8 sample pantry records.")
        print(f"Database: {app.config['DATABASE_PATH']}")


if __name__ == "__main__":
    main()
