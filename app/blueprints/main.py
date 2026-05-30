# The "main" blueprint — public, content-only pages that don't need a database.
#
# A blueprint is just a Flask object you attach routes to, then plug into the
# app via `app.register_blueprint(...)`. Think of it as a sub-app you can
# develop in isolation and mount under a URL prefix.

import json
from pathlib import Path

from flask import Blueprint, render_template

# Arguments worth knowing:
#   "main"     — the blueprint's internal name. `url_for("main.home")` uses it.
#   __name__   — tells Flask where the blueprint lives, so it can find
#                template/static folders relative to this file if we ever
#                give the blueprint its own.
main_bp = Blueprint("main", __name__)


# --- Projects data ---------------------------------------------------------
#
# Loaded ONCE at import time, not per-request. Python imports each module
# exactly once per process, so this open()+json.load() runs once when the
# app starts and the resulting list is reused for every request.
#
# Why this matters: reading + parsing a file on every request is wasteful.
# For tiny JSON it doesn't matter much, but the habit of "load static data
# once at startup" scales — to YAML configs, ML models, anything expensive.
#
# Trade-off: editing projects.json requires a server restart (or, in dev,
# saving any .py file triggers the auto-reloader). Acceptable for a CV.
#
# Path note: `__file__` is the absolute path to this main.py file. We walk
# up to the `app/` package directory, then down into `data/projects.json`.
# Using a path relative to __file__ keeps the lookup robust regardless of
# where you launch `flask run` from.
_PROJECTS_PATH = Path(__file__).resolve().parent.parent / "data" / "projects.json"

with _PROJECTS_PATH.open(encoding="utf-8") as f:
    PROJECTS = json.load(f)


@main_bp.route("/")
def home():
    # `render_template` looks in app/templates/ (set up by create_app's
    # Flask(__name__)). The second argument is the template context: any
    # variables you pass become available inside the template as {{ name }}.
    return render_template("home.html")


@main_bp.route("/work-history")
def work_history():
    # The list of jobs is hard-coded here for now. In a bigger app this
    # might come from a JSON file (like projects in phase 3) or a database.
    # Keeping it inline is fine for two or three entries.
    jobs = [
        {
            "role": "AI Engineer",
            "company": "umage.ai",
            "period": "April 2026 — present",
            "summary": (
                "Exploring and developing tools and extensions, utilizing the power of artificial intelligence. "
                "Developing and maintaining full-stack solution, using AI Agents and AI tools."
            ),
            "image": 'company-logo.png',  # e.g. "company-logo.png" once you add one in app/static/img/
        },
    ]
    return render_template("work_history.html", jobs=jobs)


@main_bp.route("/projects")
def projects():
    # PROJECTS is the list we loaded at module-import time above. We pass
    # it straight into the template — Jinja's auto-escaping will handle
    # every string safely on render.
    return render_template("projects.html", projects=PROJECTS)
