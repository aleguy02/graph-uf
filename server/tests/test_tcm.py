from src.tcm import TCM
from src.graph import Graph
import pytest

SEM = "sm25"

def test_tcm_matches_graph(complex_g: Graph):
    tcm = TCM.from_graph(complex_g, [SEM])
    for course in complex_g.getAdjList():
        assert tcm.postreqs(course, SEM) == complex_g.postreqs(course, SEM)

def test_tcm_missing_course():
    tcm = TCM({})
    with pytest.raises(ValueError):
        tcm.postreqs("ABC", SEM)
