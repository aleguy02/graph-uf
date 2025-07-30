"""
Tests for graph implementation with UF data
Run this test with `python -m pytest tests/test_graph.py`
"""

from src.graph import Graph


def test_basic_chain():
    g = Graph()

    ## Course 1
    crs1 = {
        "code": "EEL3111C",
        "prerequisites": ["MAC2312", "PHY2049"],
    }

    for prereq in crs1["prerequisites"]:
        g.insertEdge(prereq, crs1["code"])

    # expected_graph = {
    #     "MAC2312": {"EEL3111C"},
    #     "PHY2049": {"EEL3111C"},
    #     "EEL3111C": set(),
    # }

    expected_edges = [
        # this is a python equivalent to pair<string, unordered_set<string>>
        ("MAC2312", {"EEL3111C"}),
        ("PHY2049", {"EEL3111C"}),
        ("EEL3111C", set()),
    ]

    adj_list = g.getAdjList()

    for e in expected_edges:
        assert adj_list[e[0]] == e[1]

    ## Course 2
    crs2 = {
        "code": "EEX3097",
        "prerequisites": ["EEX2000", "EEX3093"],
    }

    for prereq in crs2["prerequisites"]:
        g.insertEdge(prereq, crs2["code"])

    expected_edges = [
        ("EEX2000", {"EEX3097"}),
        ("EEX3093", {"EEX3097"}),
        ("EEX3097", set()),
    ]

    adj_list = g.getAdjList()
    for e in expected_edges:
        assert adj_list[e[0]] == e[1]


def test_complex_chain():
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

    expected_edges = [
        ("MAC2311", {"MAC2312", "COT3100", "COP3503"}),
        ("MAC3472", {"MAC2312", "COT3100"}),
        ("COP3502", {"COT3100", "COP3503"}),
        ("MAC2312", {"COP3530"}),
        ("COT3100", {"COP3530"}),
        ("COP3503", {"COP3530"}),
        ("COP3504", {"COP3530"}),
        ("COP3530", set()),
    ]

    adj_list = g.getAdjList()
    for e in expected_edges:
        assert adj_list[e[0]] == e[1]
