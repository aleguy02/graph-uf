from src.tcm import TCM, Graph

def test_tcm_matches_graph(complex_g: Graph):
    tcm = TCM.from_graph(complex_g)
    for course in complex_g.getAdjList():
        assert tcm.postreqs(course) == complex_g.postreqs(course)

def test_tcm_missing_course():
    tcm = TCM({})
    assert tcm.postreqs("ABC") == set()
