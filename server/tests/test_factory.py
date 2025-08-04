"""
Test for Flask app factory pattern
"""

from app import create_app


def test_config():
    assert not create_app().testing
    testing_app = create_app({"TESTING": True})
    assert testing_app.testing
    assert testing_app.config["COURSE_GRAPH"] and type(testing_app.config["COURSE_GRAPH"]).__name__ == "Graph"
    assert testing_app.config["COURSE_TCM"] and type(testing_app.config["COURSE_TCM"]).__name__ == "TCM"
    assert testing_app.config["TOOLTIP_INFO"]
