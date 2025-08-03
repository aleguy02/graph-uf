"""
Tests for graph implementation with UF data
Run this test with `python -m pytest tests/test_graph.py`
"""

from src.graph import Graph
import pdb

SEM = "sm25"

def test_basic_chain():
    g = Graph()

    ## Course 1
    crs1 = {
        "code": "EEL3111C",
        "prerequisites": ["MAC2312", "PHY2049"],
    }

    for prereq in crs1["prerequisites"]:
        g.insertEdge(prereq, crs1["code"], SEM)

    # expected_graph = {
    #     "MAC2312": {"EEL3111C"},
    #     "PHY2049": {"EEL3111C"},
    #     "EEL3111C": set(),
    # }

    expected_edges = [
        # this is a python equivalent to pair<string, unordered_set<string>>
        ("MAC2312", {"EEL3111C": {SEM}}),
        ("PHY2049", {"EEL3111C": {SEM}}),
        ("EEL3111C", {}),
    ]

    adj_list = g.getAdjList()

    for key, inner in expected_edges:
        assert adj_list[key] == inner

    ## Course 2
    crs2 = {
        "code": "EEX3097",
        "prerequisites": ["EEX2000", "EEX3093"],
    }

    for prereq in crs2["prerequisites"]:
        g.insertEdge(prereq, crs2["code"], SEM)

    expected_edges = [
        ("EEX2000", {"EEX3097": {SEM}}),
        ("EEX3093", {"EEX3097": {SEM}}),
        ("EEX3097", {}),
    ]

    adj_list = g.getAdjList()
    for key, inner in expected_edges:
        assert adj_list[key] == inner


def test_complex_chain(complex_g):
    expected_edges = [
        ("MAC2311", {"MAC2312": {SEM}, "COT3100": {SEM}, "COP3503": {SEM}}),
        ("MAC3472", {"MAC2312": {SEM}, "COT3100": {SEM}}),
        ("COP3502", {"COT3100": {SEM}, "COP3503": {SEM}}),
        ("MAC2312", {"COP3530": {SEM}}),
        ("COT3100", {"COP3530": {SEM}}),
        ("COP3503", {"COP3530": {SEM}}),
        ("COP3504", {"COP3530": {SEM}}),
        ("COP3530", {}),
    ]

    adj_list = complex_g.getAdjList()
    for key, inner in expected_edges:
        assert adj_list[key] == inner


def test_postreqs(complex_g):
    root = "MAC2311"

    expected_postreqs = {"MAC2312", "COT3100", "COP3503", "COP3530"}
    postreqs = complex_g.postreqs(root, SEM)
    assert postreqs == expected_postreqs
