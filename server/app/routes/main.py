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

def _to_CSV(vals: list[str]) -> str | None:
    if not vals:
        return None
    return ",".join(vals)


@main_bp.route("/")
def index():
    """
    Returns home page
    """
    return render_template(
        "index.html",
        title="GraphUF",
        semesters=current_app.config["SEMESTERS"],
        default_semester=current_app.config["DEFAULT_SEMESTER"],
        url=config.URL,
        max_courses_taken=config.MAX_COURSES_TAKEN,
    )


@main_bp.route("/unlocks", methods=["POST"])
def unlocks_redirect():
    raw = request.form.get("tentative-code", "")
    code = normalise(raw)
    if not code:
        return redirect(url_for("main.index"))

    # extract completed courses
    completed = []
    for i in range(1, config.MAX_COURSES_TAKEN + 1):
        raw = request.form.get(f"code{i}", "")
        if not raw:
            continue

        base = normalise(raw)
        if not base:
            return redirect(url_for("main.index"))

        completed.append(base)

    sem = request.form.get("semester", current_app.config["DEFAULT_SEMESTER"])
    
    view = request.form.get("view_type", "")
    if view != "tcm" and view != "graph":
        abort(404, "Bad view type")
        
    return redirect(url_for("main.unlocks_page", code=code, completed=_to_CSV(completed), semester=sem, view_type=view))


@main_bp.route("/unlocks/<code>")
def unlocks_page(code: str):
    base = normalise(code)
    if not base:
        abort(404, "Bad course code")

    completed_raw = request.args.get("completed", "")
    completed = completed_raw.split(",") if completed_raw else []

    sem = request.args.get("semester", current_app.config["DEFAULT_SEMESTER"])
    view = request.args.get("view_type", "")
    if view != "tcm" and view != "graph":
        abort(404, "Bad view type")

    struct = current_app.config["COURSE_TCM"] if view == "tcm" else current_app.config["COURSE_GRAPH"]
    
    try:
        unlocked = struct.postreqs(base, sem)  #all downstream courses
    except ValueError:
        abort(404, f"{base} not found in catalog")
    
    graph = current_app.config["COURSE_GRAPH"]
    prev_unlocked = set()
    for c in completed:  # this section is a good candidate for future optimization/refactoring but it works
        try:
            direct_postreqs = graph.getDirectPostreqs(c, sem)
            prev_unlocked.update(direct_postreqs)
        except KeyError:
            abort(404, f"{c} not found in catalog")
    

    # Courses unlocked by 'base' that are not already unlocked by completed courses
    new_unlocked = sorted(unlocked.difference(prev_unlocked))
    
    # Courses unlocked by 'base' that are also unlocked by completed courses
    already_unlocked = sorted(unlocked.intersection(prev_unlocked))

    

    return render_template("unlocks.html",
                           title=f"{base} unlocks…",
                           code=base,
                           new_unlocked=new_unlocked,
                           already_unlocked=already_unlocked,
                           semesters=current_app.config["SEMESTERS"],
                           selected_semester=sem
                           )
