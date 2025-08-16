# server/app/routes/api.py

from flask import Blueprint, current_app, jsonify, abort, request
import re
api_bp = Blueprint("api", __name__, url_prefix="/api")

AY_RE = re.compile(r"^AY(\d{4})-(\d{4})$")

def _resolve_selected_semesters(selected: str) -> tuple[str, list[str]]:
    """
    resolver
    """
    ay_terms = current_app.config.get("AY_TERMS", {})
    if selected in ay_terms:
        return selected, ay_terms[selected]

    m = AY_RE.match(selected)
    if m:
        y1, y2 = m.groups()
        sm = f"sm{y1[-2:]}"
        fa = f"f{y1[-2:]}"
        sp = f"sp{y2[-2:]}"
        return selected, [sm, fa, sp]

    if "," in selected:
        parts = [p.strip() for p in selected.split(",") if p.strip()]
        return selected, parts

    return selected, [selected]

@api_bp.get("/unlocks/<code>")
def unlocks(code: str):
    """
    Return every course that (transitively) lists <code> as a prerequisite.
    """
    graph = current_app.config["COURSE_GRAPH"]
    key = code.upper().strip()
    selected = request.args.get(
        "semester",
        current_app.config.get("DEFAULT_AY", current_app.config["DEFAULT_SEMESTER"])
    )
    _, terms = _resolve_selected_semesters(selected)
    try:
        unlocked = sorted(graph.postreqs(key, terms))

    except ValueError:
        abort(404, f"{key} not found in catalog")
    return jsonify(unlocked)


@api_bp.get("/prereqs/<code>")
def prereqs(code: str):
    """
    Return the *direct* prerequisites for <code>.
    """
    graph = current_app.config["COURSE_GRAPH"]
    key = code.upper().strip()
    selected = request.args.get(
        "semester",
        current_app.config.get("DEFAULT_AY", current_app.config["DEFAULT_SEMESTER"])
    )
    _, terms = _resolve_selected_semesters(selected)
    sem_set = set(terms)

    # build the reverse lookup: any course X where adj_list[X] contains key
    try:
        adj = graph.getAdjList()
    except AttributeError:
        abort(500, "Graph is mis-configured")

    if key not in adj and all(key not in targets for targets in adj.values()):
        abort(404, f"{key} not found in catalog")

    direct = sorted(
        src for src, targets in adj.items()
        if key in targets and (targets[key] & sem_set)  # ANY selected term
    )
    return jsonify(direct)


@api_bp.post("/schedule")
def schedule_post():
    # your schedule‑generation stub
    return {"hello": "world"}


@api_bp.get("/schedule")
def schedule_get():
    return {"hello": "world"}
