import pytest
from app import create_app
from src.graph import Graph


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
        }
    )

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def complex_g():
    g = Graph()

    # see docs/images/complex-chain-simplified.png for a visual of these courses
    courses = [
        {
            "code": "COP3530",
            "prerequisites": ["MAC2312", "COT3100", "COP3503", "COP3504"],
        },
        {
            "code": "MAC2312",
            "prerequisites": ["MAC2311", "MAC3472"],
        },
        {
            "code": "COT3100",
            "prerequisites": ["MAC2311", "MAC3472", "COP3502"],
        },
        {
            "code": "COP3503",
            "prerequisites": ["MAC2311", "COP3502"],
        },
        {
            "code": "COP3504",
            "prerequisites": [],
        },
        {
            "code": "MAC2311",
            "prerequisites": [],
        },
        {
            "code": "MAC3472",
            "prerequisites": [],
        },
        {
            "code": "COP3502",
            "prerequisites": [],
        },
    ]

    for crs in courses:
        for prereq in crs["prerequisites"]:
            g.insertEdge(prereq, crs["code"])

    return g
