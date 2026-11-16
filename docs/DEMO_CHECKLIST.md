# SmartPantry Live Demonstration Checklist

## Before the presentation

- [ ] Install the Python requirements.
- [ ] Install SWI-Prolog and confirm `swipl --version` works.
- [ ] Run `python seed_demo.py --reset` to load sample pantry records.
- [ ] Start the app with `python run.py`.
- [ ] Confirm the dashboard says `SWI-Prolog` rather than `Python fallback`.
- [ ] Open the project repository and make sure the README and source folders are visible.

## Suggested live demonstration

1. Open the dashboard and explain the total records, expiring-soon count, and past-date count.
2. Open Inventory and search for an item such as `milk`.
3. Add a new item with a name, category, quantity, purchase date, and expiration date.
4. Edit the new item and change its quantity or expiration date.
5. Delete a sample item to show the delete workflow.
6. Return to the dashboard and show how the totals and attention list change.
7. Open `app/services/functional_rules.py` and explain the pure functions and use of `map`, `filter`, and `reduce`.
8. Open `app/logic/pantry_rules.pl` and explain the Prolog facts/rules and how the application calls them.
9. Open `app/models/food_item.py` and `app/data/pantry_repository.py` to explain classes and encapsulation.
10. Explain the ordered request flow in `app/routes.py` as the imperative example.

## Questions to prepare for

- Why did the group choose Flask and SQLite?
- Which file demonstrates each programming paradigm?
- What happens if SWI-Prolog is not installed?
- How are user inputs validated?
- How are SQL statements protected against direct input injection?
- What are the limitations of date-only expiration reminders?
- What would the group improve with more development time?
