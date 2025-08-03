# tests/conftest.py
import pytest
from app import create_app

@pytest.fixture(scope="session")
def app():
    """start the flask app so testing on real environment"""
    return create_app({"TESTING": True})

@pytest.fixture(scope="session")
def course_graph(app):
    """fully built graph"""
    return app.config["COURSE_GRAPH"]

@pytest.fixture
def client(app):
    return app.test_client()

import time
from src.tcm import TCM

SEM   = "f25"
ROOT  = "MAC2311"
#ROOT = "COP3502C"
#ROOT = "CHM2046"
REPS  = 10_000

def avg_time(func, *args, reps=REPS):
    t0 = time.perf_counter()
    for _ in range(reps):
        func(*args)
    return (time.perf_counter() - t0) / reps

def test_average_latency(course_graph):
    tcm = TCM.from_graph(course_graph, [SEM])
    bfs = avg_time(course_graph.postreqs, ROOT, SEM)
    fast = avg_time(tcm.postreqs,            ROOT, SEM)
    print(f"BFS: {bfs*1e6:.2f} µs  |  TCM: {fast*1e6:.2f} µs")
    assert fast < bfs * 0.5
