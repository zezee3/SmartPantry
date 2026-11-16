"""Flask application factory."""

import os
from pathlib import Path

from flask import Flask

from app.data.database import initialize_database
from app.routes import main_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "local-development-key-change-me"),
        DATABASE_PATH=os.environ.get(
            "DATABASE_PATH", str(Path(app.instance_path) / "smartpantry.db")
        ),
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    initialize_database(app.config["DATABASE_PATH"])
    app.register_blueprint(main_bp)
    return app
