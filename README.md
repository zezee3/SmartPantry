 SmartPantry

 Project Demonstration Video

Watch our SmartPantry application demonstration:

[Click here to watch the SmartPantry Demo] https://drive.google.com/file/d/1ZZvVRbshj8U133SOJ_idSKG5Yr9HyNIJ/view?usp=sharing

A Food Inventory and Expiration Tracking System**

SmartPantry is a small web application for recording household food items, checking their recorded expiration dates, and helping users prioritize items that may need attention. It was planned as a two-week CS121 Programming Languages project and demonstrates imperative, functional, logic, and object-oriented programming.

> Important: SmartPantry provides date-based reminders only. It does not determine whether food is safe to eat. Always follow product labels, storage instructions, and local food-safety guidance.

 1. Main features

- Add, edit, view, and delete pantry items.
- Store category, quantity, unit, purchase date, optional expiration date, and notes.
- Search items and filter by category.
- Show dashboard totals for all items, expired items, items expiring soon, and categories.
- Display date-based status labels: Expired, Expiring soon, Fresh, and No expiry date.
- Highlight items that may need attention first and show a rule-based priority label.
- Use SWI-Prolog rules for expiration status and consumption-priority classification when SWI-Prolog is installed.
- Fall back to equivalent Python rules if SWI-Prolog is unavailable, so the basic application remains usable.

The default "Expiring soon" window is 0 to 3 days, inclusive. This is a configurable project rule, not a food-safety recommendation.

 2. Technology stack

| Layer | Technology | Purpose |
|---|---|---|
| Front-end | HTML, CSS, Bootstrap 5 | Pages, forms, tables, and responsive layout |
| Back-end | Python 3 and Flask | Routes, validation, and application services |
| Database | SQLite | Persistent pantry records |
| Logic engine | SWI-Prolog | Facts, rules, and logical classification |
| Version control | Git and GitHub | Source history and collaboration |

 3. Requirements

- Python 3.10 or newer
- pip
- A modern web browser
- SWI-Prolog for the live Prolog demonstration (recommended and required to show the Prolog engine running)

The app can run without SWI-Prolog by using its documented Python fallback. For the CS121 logic-programming demonstration, install SWI-Prolog and confirm that the `swipl` command is available in your terminal.

 4. Setup

 Windows PowerShell

`powershell
cd SmartPantry
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed_demo.py
python run.py
```

If PowerShell blocks virtual-environment activation, use Command Prompt instead:

```bat
.venv\Scripts\activate.bat
```

macOS or Linux

```bash
cd SmartPantry
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed_demo.py
python run.py
```

Open <http://127.0.0.1:5000> in your browser.

Optional: copy `.env.example` to `.env` and set a private `SECRET_KEY` before sharing or deploying the app. The included default key is only for local development.

The SQLite database is stored at `instance/smartpantry.db`. A sample database is included in the project. Running `python seed_demo.py` adds sample records only when the database is empty. To replace the current records with fresh sample data, run:

```bash
python seed_demo.py --reset
```

5. Installing SWI-Prolog

Install SWI-Prolog using the official instructions for your operating system:

<https://www.swi-prolog.org/download/stable>

After installation, open a new terminal and check:

```bash
swipl --version
```

Restart the Flask application after installing SWI-Prolog. The dashboard displays whether the Prolog engine or the Python fallback is being used.

The Prolog source is `app/logic/pantry_rules.pl`. The Python adapter is `app/logic/prolog_engine.py`.

 6. Project structure

```text
SmartPantry/
|-- app/
|   |-- __init__.py
|   |-- routes.py
|   |-- data/
|   |   |-- database.py
|   |   `-- pantry_repository.py
|   |-- logic/
|   |   |-- pantry_rules.pl
|   |   `-- prolog_engine.py
|   |-- models/
|   |   `-- food_item.py
|   |-- services/
|   |   |-- functional_rules.py
|   |   `-- pantry_service.py
|   |-- static/css/style.css
|   `-- templates/
|       |-- base.html
|       |-- dashboard.html
|       |-- inventory.html
|       `-- item_form.html
|-- database/schema.sql
|-- docs/
|   |-- ARCHITECTURE.md
|   |-- DEMO_CHECKLIST.md
|   |-- DEVELOPMENT_PLAN.md
|   |-- PARADIGM_GUIDE.md
|   `-- PROJECT_OVERVIEW.md
|-- instance/smartpantry.db
|-- tests/
|   |-- test_functional_rules.py
|   |-- test_repository.py
|   `-- test_service_validation.py
|-- .gitignore
|-- requirements.txt
|-- run.py
`-- seed_demo.py
```

 7. Database

The database has one main table, `food_items`:

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Food item name |
| category | TEXT | Food category |
| quantity | REAL | Quantity on hand |
| unit | TEXT | Unit such as pcs, packs, kg, or L |
| purchase_date | TEXT | Purchase date in YYYY-MM-DD format |
| expiry_date | TEXT, nullable | Recorded expiration date |
| notes | TEXT | Optional notes |
| created_at | TEXT | Record creation timestamp |
| updated_at | TEXT | Last update timestamp |

The schema is in `database/schema.sql`. The repository uses parameterized SQL queries.

 8. Where the four paradigms are demonstrated

| Paradigm | Main files | How it appears |
|---|---|---|
| Imperative | `app/routes.py`, `app/services/pantry_service.py` | Ordered steps, validation, conditionals, loops, and database operations |
| Functional | `app/services/functional_rules.py` | Pure functions, immutable result objects, and `map`/`filter`/`reduce` for data summaries |
| Logic | `app/logic/pantry_rules.pl`, `app/logic/prolog_engine.py` | Prolog facts/rules and queries classify expiration status and priority |
| Object-oriented | `app/models/food_item.py`, `app/data/pantry_repository.py`, `app/services/pantry_service.py` | Classes encapsulate food records, database access, and pantry operations |

See `docs/PROJECT_OVERVIEW.md` for the problem, objectives, scope, and SDG alignment; `docs/DEVELOPMENT_PLAN.md` for the two-week schedule; and `docs/PARADIGM_GUIDE.md` for code examples and defense notes. Do not claim that ordinary Python `if` statements are Logic Programming; the Prolog rules are the logic-programming component.

 9. Run tests

```bash
python -m unittest discover -s tests -v
```

The tests cover date functions, summary calculations, SQLite repository operations, and form validation. The Prolog integration can also be checked manually by installing SWI-Prolog and adding or viewing pantry records.

 10. Suggested GitHub workflow

Create an empty repository on GitHub, then run these commands from the project folder:

```bash
git init
git add .
git commit -m "Add SmartPantry application"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your own repository URL. Commit regularly and use clear messages, for example `Add pantry item form` or `Connect Prolog classification`.

11. Scope and limitations

- This is a local household pantry prototype, not a commercial food-safety system.
- There is no user account or multi-household access control in this first version.
- Expiration reminders use the date entered by the user; the app does not verify labels or storage conditions.
- The app does not send email, SMS, or push notifications.
- The Prolog component requires SWI-Prolog to be installed and available as `swipl`. Without it, the app uses a clearly identified Python fallback.

Before presenting, review the code, change the sample records to suit your demonstration, and make sure every group member can explain the features and paradigm mapping.
