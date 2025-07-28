"""
API routes
"""

from flask import Blueprint, request

api_bp: Blueprint = Blueprint("api", __name__)


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
