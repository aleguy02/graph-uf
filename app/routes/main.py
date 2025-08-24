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
import json

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
        max_courses_taken=config.MAX_COURSES_TAKEN,
    )


@main_bp.route("/unlocks", methods=["POST"])
def unlocks_redirect():
    code = request.form.get("tentative-code", "")

    completed = request.form.get(f"completed-courses", "[]")
    try:
        completed = json.loads(completed)
    except json.JSONDecodeError as e:
        current_app.logger.exception(f"Error decoding JSON: {e}")
        completed = []

    sem = request.form.get("semester", current_app.config["DEFAULT_SEMESTER"])

    view = request.form.get("view_type", "")
    if view not in ("tcm", "graph"):
        abort(400, "Bad view type")

    return redirect(
        url_for(
            "main.unlocks_page",
            code=code,
            completed=_to_CSV(
                completed
            ),  # optimizaton, pass more efficiently, maybe in a cookie
            semester=sem,
            view_type=view,
        )
    )


@main_bp.route("/unlocks/<code>")
def unlocks_page(code: str):
    base = normalise(code)
    if not base:
        abort(400, f"Bad course code: {code}")

    completed_raw = request.args.get("completed", "")
    completed = set(completed_raw.split(",")) if completed_raw else set()

    sem = request.args.get("semester", current_app.config["DEFAULT_SEMESTER"])
    view = request.args.get("view_type", "")
    if view != "tcm" and view != "graph":
        abort(400, "Bad view type")

    struct = (
        current_app.config["COURSE_TCM"]
        if view == "tcm"
        else current_app.config["COURSE_GRAPH"]
    )

    try:
        unlocked = struct.postreqs(base, sem)  # all downstream courses
    except ValueError:
        abort(400, f"Course not found in catalog: {base}")

    # all courses in unlocks for which you would meet all or some prerequisites or where the only prerequisite is the tentative course
    meet_prereqs = set()

    # all courses in unlocks for which you do not meet any other prereqs, excluding tentative course
    not_meet_prereqs = set()

    """
    this readibility sucsk
    """
    for c in unlocked:
        """
        Get prerequisites for course c using the same logic as the url_for(api_bp.prereqs()) API route
        please review this code carefully in code review. It may be wise to opt for an internal API call if we want
        to use the prereqs API elsewhere in the app. For now, it is more efficient to just duplicate the logic
        """
        graph = current_app.config["COURSE_GRAPH"]
        try:
            adj = graph.getAdjList()
            c_prereqs = set(
                src
                for src, targets in adj.items()
                if c in targets and sem in targets[c]
            )
            if not c_prereqs.isdisjoint(completed) or c_prereqs == {base}:
                meet_prereqs.add(c)
            else:
                not_meet_prereqs.add(c)
        except (AttributeError, KeyError):
            abort(400, f"Course not found in catalog: {c}")

    return render_template(
        "unlocks.html",
        title=f"{base} unlocks",
        code=base,
        not_meet_prereqs=sorted(not_meet_prereqs),
        meet_prereqs=sorted(meet_prereqs),
        semesters=current_app.config["SEMESTERS"],
        selected_semester=sem,
        tooltip_info=current_app.config["TOOLTIP_INFO"].get(sem, {}),
    )
