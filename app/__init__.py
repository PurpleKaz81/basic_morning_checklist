from flask import Flask


def create_app():
    app = Flask(__name__, static_folder="app/static", template_folder="app/templates")

    # Register routes
    from . import routes

    app.register_blueprint(routes.bp)

    return app
