from flask import Flask, render_template
from app.routes.main import main_bp
from app.routes.api import api_bp
from pathlib import Path
from src.loader import build_graph, build_tcm, build_tooltip, semesters

def _build_ay_terms(sems: list[str]) -> dict[str, list[str]]:
    """
    Build AY keys from years that appear as summer or fall starters
    """
    years = sorted({2000 + int(s[-2:]) for s in sems if s.startswith(("sm", "f"))})
    ay = {}
    for y in years:
        yy = str(y)[-2:]
        yyp1 = str(y + 1)[-2:]
        ay[f"AY{y}-{y+1}"] = [f"sm{yy}", f"f{yy}", f"sp{yyp1}"]
    return ay

def create_app(test_config=None):
    app = Flask(__name__)

    try:
        app.config["COURSE_GRAPH"] = build_graph()
        app.config["COURSE_TCM"] = build_tcm()
        app.config["TOOLTIP_INFO"] = build_tooltip()
        app.config["SEMESTERS"] = semesters
        app.config["DEFAULT_SEMESTER"] = semesters[-1]
        app.config["AY_TERMS"] = _build_ay_terms(semesters)
        # pick last AY as default, otherwise fall back to DEFAULT_SEMESTER
        app.config["DEFAULT_AY"] = (
            sorted(app.config["AY_TERMS"].keys())[-1]
            if app.config["AY_TERMS"] else app.config["DEFAULT_SEMESTER"]
        )

    except Exception as e:
        app.logger.error(f"Failed to build course graph: {e}")
        raise RuntimeError("App init failed due to course graph error") from e

    if test_config and test_config.get("TESTING"):
        app.config.from_mapping(test_config)

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", title="GraphUF"), 404

    return app


app = create_app()
