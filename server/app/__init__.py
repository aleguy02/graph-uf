from flask import Flask, render_template
from app.routes.main import main_bp
from app.routes.api import api_bp
from pathlib import Path
import sys

SRC = Path(__file__).resolve().parent.parent
sys.path.append(str(SRC))

from src.loader import build_graph


def create_app(test_config=None):
    app = Flask(__name__)

    try:
        app.config["COURSE_GRAPH"] = build_graph()
    except Exception as e:
        app.logger.error(f"Failed to build course graph: {e}")
        raise RuntimeError("App init failed due to course graph error") from e

    if test_config and test_config.get("TESTING"):
        app.config.from_mapping(test_config)

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", title="Not Found"), 404

    return app


app = create_app()
