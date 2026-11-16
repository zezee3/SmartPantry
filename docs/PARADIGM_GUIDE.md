# Programming Paradigms in SmartPantry

The application is designed to show four distinct approaches in working code. The examples below identify the relevant files and explain the role of each approach.

## 1. Imperative Programming

**Main location:** `app/routes.py` and `app/services/pantry_service.py`

The create-item route follows an ordered workflow: receive the form, validate the values, write the record through the repository, show a message, and redirect the browser.

```python
try:
    get_service().create_item(request.form)
except ValueError as error:
    flash(str(error), "danger")
    return render_template("item_form.html", ...), 400

flash("Food item added to your pantry.", "success")
return redirect(url_for("main.inventory"))
```

This is imperative because the program explicitly performs operations in a defined order and uses control flow to handle success or validation errors.

## 2. Functional Programming

**Main location:** `app/services/functional_rules.py`

The functions `days_until_expiry`, `filter_by_status`, and `summarize_inventory` calculate results without changing the original food records. The `ItemStatus` result is a frozen dataclass. The summary uses `map`, `filter`, and `reduce` to transform and aggregate data.

```python
statuses = list(map(lambda view: view.expiry_status, item_views))
quantities = map(lambda view: view.item.quantity, item_views)
total_quantity = reduce(lambda total, value: total + value, quantities, 0.0)
```

These functions are reusable and produce new results instead of mutating the source records.

## 3. Logic Programming

**Main location:** `app/logic/pantry_rules.pl`

The Prolog file defines facts for the reminder window and priority mapping, plus rules for expiration status. The Python adapter passes the number of days remaining to SWI-Prolog and reads the result.

```prolog
expiry_status(Days, expired) :-
    Days < 0,
    !.
expiry_status(Days, expiring_soon) :-
    Days >= 0,
    Days =< 3,
    !.
expiry_status(_, fresh).
```

The rules express relationships and conditions declaratively. Prolog determines which rule matches the supplied value. The 0-to-3 day threshold is a project-defined reminder setting.

To demonstrate this paradigm, install SWI-Prolog and confirm that the dashboard reports `SWI-Prolog` as the classification engine. If it reports `Python fallback`, the app is still usable, but the Prolog engine is not active.

## 4. Object-Oriented Programming

**Main locations:** `app/models/food_item.py`, `app/data/pantry_repository.py`, and `app/services/pantry_service.py`

- `FoodItem` represents a pantry record as an immutable domain object.
- `PantryRepository` encapsulates database operations.
- `PantryService` encapsulates validation and pantry workflows.
- `PrologEngine` encapsulates communication with the external logic engine.

Each class has a defined responsibility. Routes use these objects instead of placing all data and behavior in one file.

## Suggested defense explanation

"SmartPantry uses more than one programming paradigm because each approach solves a different part of the problem. Imperative code handles the sequence of web operations, functional code calculates summaries without changing the original records, Prolog applies explicit rules to classify expiration status, and object-oriented classes organize food records and database services. The paradigms work together in one application rather than being four separate programs."
