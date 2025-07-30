"""
API routes
"""

from flask import Blueprint, request, current_app, jsonify, abort

api_bp: Blueprint = Blueprint("api", __name__)

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

@api_bp.route("/api/schedule", methods=["POST"])
def schedule_post():
    """
    Create schedule
    """
    return {"hello": "world"}


@api_bp.route("/api/schedule", methods=["GET"])
def schedule_get():
    """
    Get schedule
    """
    return {"hello": "world"}
