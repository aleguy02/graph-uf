from flask import Flask, render_template
from app.routes.main import main_bp
from app.routes.api import api_bp
from pathlib import Path
from src.loader import build_graph, build_tcm, build_tooltip, semesters
import re

def semester_label(code: str) -> str:
    m = re.fullmatch(r'(f|sp|sm)(\d{2})', code)
    if not m:
        return code #fallback for if not pattern match
    term, yy = m.groups()
    term_map = {'f': 'Fall', 'sp': 'Spring', 'sm': 'Summer'}
    year = 2000 + int(yy)
    return f"{term_map[term]} {year}"

def create_app(test_config=None):
    app = Flask(__name__)

    try:
        app.config["COURSE_GRAPH"] = build_graph()
        app.config["COURSE_TCM"] = build_tcm()
        app.config["TOOLTIP_INFO"] = build_tooltip()
        app.config["SEMESTERS"] = semesters
        app.config["DEFAULT_SEMESTER"] = semesters[-1]
    except Exception as e:
        app.logger.error(f"Failed to build course graph: {e}")
        raise RuntimeError("App init failed due to course graph error") from e

    if test_config and test_config.get("TESTING"):
        app.config.from_mapping(test_config)

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    app.jinja_env.filters["semester_label"] = semester_label
    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", title="GraphUF"), 404

    return app


app = create_app()
