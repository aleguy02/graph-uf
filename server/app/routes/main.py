"""
Routes to serve main static pages. Not sure if this is how we'll do the frontend so we'll probably have to change it
"""

from flask import (
    Blueprint,
    render_template,
    url_for,
    redirect,
    current_app,
    request,
    abort,
)
from app.config import get_config

main_bp: Blueprint = Blueprint("main", __name__)
config = get_config()

import re

CODE_RE = re.compile(r"^[A-Z]{3,4}\d{4}[A-Z]?")


def normalise(code: str) -> str | None:
    m = CODE_RE.match(code.upper().replace(" ", ""))
    return m.group(0) if m else None


@main_bp.route("/")
def index():
    """
    Returns home page
    """
    return render_template(
        "index.html",
        title="UF Scheduler",
        url=config.URL,
    )


@main_bp.route("/unlocks", methods=["POST"])
def unlocks_redirect():
    raw = request.form.get("code", "")
    base = normalise(raw)
    if not base:
        return redirect(url_for("main.index"))
    return redirect(url_for("main.unlocks_page", code=base))


@main_bp.route("/unlocks/<code>")
def unlocks_page(code: str):
    base = normalise(code)
    if not base:
        abort(404, "Bad course code")

    graph = current_app.config["COURSE_GRAPH"]
    try:
        unlocked = sorted(graph.postreqs(base))  #all downstream courses
    except ValueError:
        abort(404, f"{base} not found in catalog")
    #shows empty list
    return render_template("unlocks.html",
                           title=f"{base} unlocks…",
                           code=base,
                           unlocked=unlocked)
