"""Page routes for the SmartPantry web application."""

import hmac
import secrets
from datetime import date
from pathlib import Path

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app.data.pantry_repository import PantryRepository
from app.logic.prolog_engine import PrologEngine
from app.services.pantry_service import CATEGORIES, UNITS, PantryService

main_bp = Blueprint("main", __name__)

STATUS_LABELS = {
    "expired": "Expired",
    "expiring_soon": "Expiring soon",
    "fresh": "Fresh",
    "no_expiry_date": "No expiry date",
}

PRIORITY_LABELS = {
    "review": "Review item",
    "high": "Use soon",
    "normal": "Normal",
}

PRIORITY_CLASSES = {
    "review": "priority-review",
    "high": "priority-high",
    "normal": "priority-normal",
}

STATUS_CLASSES = {
    "expired": "status-expired",
    "expiring_soon": "status-soon",
    "fresh": "status-fresh",
    "no_expiry_date": "status-neutral",
}


def get_service():
    repository = PantryRepository(current_app.config["DATABASE_PATH"])
    rules_path = Path(__file__).resolve().parent / "logic" / "pantry_rules.pl"
    logic_engine = PrologEngine(rules_path=rules_path)
    return PantryService(repository, logic_engine)


@main_bp.app_context_processor
def inject_template_helpers():
    def csrf_token():
        token = session.get("_csrf_token")
        if token is None:
            token = secrets.token_urlsafe(32)
            session["_csrf_token"] = token
        return token

    return {
        "csrf_token": csrf_token,
        "status_labels": STATUS_LABELS,
        "status_classes": STATUS_CLASSES,
        "priority_labels": PRIORITY_LABELS,
        "priority_classes": PRIORITY_CLASSES,
        "today_date": date.today().isoformat(),
    }


@main_bp.before_app_request
def protect_post_requests():
    if request.method == "POST":
        submitted = request.form.get("_csrf_token", "")
        expected = session.get("_csrf_token", "")
        if not submitted or not expected or not hmac.compare_digest(submitted, expected):
            abort(400, description="The form token is missing or invalid. Refresh the page and try again.")


@main_bp.route("/")
def dashboard():
    service = get_service()
    summary, attention_items, item_views, engine_name = service.get_dashboard_data()
    return render_template(
        "dashboard.html",
        summary=summary,
        attention_items=attention_items,
        recent_items=item_views[:6],
        engine_name=engine_name,
    )


@main_bp.route("/inventory")
def inventory():
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    item_views = get_service().get_item_views(search=search, category=category)
    return render_template(
        "inventory.html",
        item_views=item_views,
        categories=CATEGORIES,
        search=search,
        selected_category=category,
    )


@main_bp.route("/items/new", methods=["GET", "POST"])
def create_item():
    if request.method == "POST":
        try:
            get_service().create_item(request.form)
        except ValueError as error:
            flash(str(error), "danger")
            return render_template(
                "item_form.html",
                page_title="Add food item",
                item=None,
                form_data=request.form,
                categories=CATEGORIES,
                units=UNITS,
            ), 400
        flash("Food item added to your pantry.", "success")
        return redirect(url_for("main.inventory"))

    return render_template(
        "item_form.html",
        page_title="Add food item",
        item=None,
        form_data={},
        categories=CATEGORIES,
        units=UNITS,
    )


@main_bp.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
def edit_item(item_id):
    service = get_service()
    item = service.get_item(item_id)
    if item is None:
        abort(404)

    if request.method == "POST":
        try:
            updated = service.update_item(item_id, request.form)
        except ValueError as error:
            flash(str(error), "danger")
            return render_template(
                "item_form.html",
                page_title="Edit food item",
                item=item,
                form_data=request.form,
                categories=CATEGORIES,
                units=UNITS,
            ), 400
        if not updated:
            abort(404)
        flash("Food item updated.", "success")
        return redirect(url_for("main.inventory"))

    return render_template(
        "item_form.html",
        page_title="Edit food item",
        item=item,
        form_data={},
        categories=CATEGORIES,
        units=UNITS,
    )


@main_bp.route("/items/<int:item_id>/delete", methods=["POST"])
def delete_item(item_id):
    deleted = get_service().delete_item(item_id)
    if deleted:
        flash("Food item deleted.", "success")
    else:
        flash("That food item could not be found.", "warning")
    return redirect(url_for("main.inventory"))
