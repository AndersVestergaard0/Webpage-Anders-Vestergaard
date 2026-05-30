# The Flask application package.
#
# This file makes `app/` a Python package, AND it exposes `create_app()` —
# the "application factory" Flask will call to build an app instance.
#
# Why a factory instead of a module-level `app = Flask(__name__)`?
#
#   1. Testing. Each test can build its own app with a test-only config
#      (in-memory DB, CSRF disabled, etc.) without polluting any global.
#   2. Multiple configs. Dev / prod / test can each get their own settings
#      without `if FLASK_ENV == "production"` sprinkled through the code.
#   3. Extension lifecycle. Extensions (SQLAlchemy, Migrate, Login, ...) are
#      instantiated once in `extensions.py`, then bound to whichever app the
#      factory builds. This is the pattern that avoids the dreaded
#      circular-import problem in larger Flask apps.
#
# Flask auto-discovers a function named `create_app` in the package set by
# FLASK_APP, so once .env has `FLASK_APP=app`, `flask run` calls this.

from flask import Flask


def create_app() -> Flask:
    # `Flask(__name__)` again, but this time __name__ == "app" (the package),
    # so Flask looks for templates in app/templates/ and static files in
    # app/static/ by default. That's the whole reason we put them there.
    app = Flask(__name__)

    # Register blueprints. A blueprint is a self-contained collection of
    # routes that we plug into the app. Right now we only have one, but
    # in later phases we'll add: blog, admin, auth, contact.
    #
    # The import is *inside* the factory deliberately. If it were at the
    # top of the file, importing `app.blueprints.main` would import this
    # module, which would import the blueprint, which would import this
    # module... a circular import. Late imports break that cycle.
    from app.blueprints.main import main_bp
    app.register_blueprint(main_bp)

    return app
