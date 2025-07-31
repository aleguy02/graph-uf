# server/app/routes/api.py

from flask import Blueprint, current_app, jsonify, abort

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.get("/unlocks/<code>")
def unlocks(code: str):
    """
    Returns courses that <code> is a prerequesite for
    """
    graph = current_app.config["COURSE_GRAPH"]
    unlocked = sorted(graph.getAdjList().get(code.upper(), []))
    if not unlocked:
        abort(404, f"{code} not a prerequesite")
    return jsonify(unlocked)

@api_bp.get("/unlocks/<code>")
def unlocks(code: str):
    """
    Return every course that (transitively) lists <code> as a prerequisite.
    """
    graph = current_app.config["COURSE_GRAPH"]
    key = code.upper().strip()
    try:
        unlocked = sorted(graph.postreqs(key))
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

    # build the reverse lookup: any course X where adj_list[X] contains key
    try:
        adj = graph.getAdjList()
    except AttributeError:
        abort(500, "Graph is mis‑configured")

    if key not in adj and all(key not in targets for targets in adj.values()):
        abort(404, f"{key} not found in catalog")

    direct = sorted(
        src for src, targets in adj.items()
        if key in targets
    )
    return jsonify(direct)


@api_bp.post("/schedule")
def schedule_post():
    # your schedule‑generation stub
    return {"hello": "world"}


@api_bp.get("/schedule")
def schedule_get():
    return {"hello": "world"}
