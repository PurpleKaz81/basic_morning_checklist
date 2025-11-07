from flask import Flask
from pathlib import Path


def create_app():
    # Use absolute paths so Jinja2 can find templates regardless of cwd
    root = Path(__file__).resolve().parent
    template_dir = str(root / "templates")
    static_dir = str(root / "static")

    app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)

    # Register routes
    from . import routes

    app.register_blueprint(routes.bp)

    return app
