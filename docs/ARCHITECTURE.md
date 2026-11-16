# SmartPantry System Architecture

## Overview

SmartPantry uses a simple three-layer web architecture with a separate Prolog logic component.

```text
Browser
  |
  | HTTP request / HTML response
  v
Flask routes (app/routes.py)
  |
  v
PantryService (validation and application workflow)
  |                         \
  |                          \ subprocess call
  v                           v
PantryRepository           SWI-Prolog rules
  |                       (app/logic/pantry_rules.pl)
  v
SQLite database
```

## Front-end

- Jinja templates render the dashboard, inventory table, and add/edit form.
- Bootstrap provides responsive layout components.
- `app/static/css/style.css` contains the project-specific visual styles.
- Forms submit to Flask routes using standard HTTP requests.

## Back-end

- Flask routes receive requests and choose the correct workflow.
- `PantryService` validates form data and coordinates repository and logic operations.
- `PantryRepository` contains parameterized SQLite queries.
- `PrologEngine` sends calculated days-remaining values to SWI-Prolog and reads the returned status and priority.

## Database

The first version uses one `food_items` table. It stores the food name, category, quantity, unit, purchase date, optional expiration date, notes, and timestamps. The schema is maintained in `database/schema.sql`.

## Main request flow

1. A user opens the inventory page or submits a food-item form.
2. Flask receives the request in `app/routes.py`.
3. `PantryService` validates submitted values or requests the current records.
4. `PantryRepository` reads or writes data in SQLite.
5. For inventory status, the service calculates days remaining and asks `PrologEngine` to classify each value.
6. The route passes the resulting view data to a Jinja template.
7. The browser displays the updated page.

## Design decisions

- SQLite keeps installation simple for a small classroom project.
- The repository pattern keeps SQL separate from route handling.
- Immutable dataclasses make domain and calculated view objects easier to reason about.
- Prolog handles rule-based classification, while Python handles date arithmetic and web requests.
- A clearly labelled Python fallback keeps the app usable when SWI-Prolog is not installed. The Prolog component should be active during the programming-paradigm demonstration.
