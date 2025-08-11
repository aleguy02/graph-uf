"""
Test for Flask app factory pattern
"""

from app import create_app
from src.graph import Graph
from src.tcm import TCM


def test_config():
    assert not create_app().testing
    testing_app = create_app({"TESTING": True})
    assert testing_app.testing
    assert isinstance(testing_app.config["COURSE_GRAPH"], Graph)
    assert isinstance(testing_app.config["COURSE_TCM"], TCM)
    assert isinstance(testing_app.config["TOOLTIP_INFO"], dict)
