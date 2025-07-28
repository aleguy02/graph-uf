"""
Routes to serve main static pages. Not sure if this is how we'll do the frontend so we'll probably have to change it
"""

from flask import Blueprint, render_template, url_for
from app.config import get_config

main_bp: Blueprint = Blueprint("main", __name__)
config = get_config()


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
