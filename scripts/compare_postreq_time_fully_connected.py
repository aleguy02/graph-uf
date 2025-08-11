"""
benchmark worst case performance using a fully connected graph
"""

import time
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.graph import Graph
from src.tcm import TCM

TEST_SEM = "test"
N_VERTICES = 512
REPS = 100
LOOKUPS = 10_000

# generates class codes
VERTS = [f"CRS{i:04}" for i in range(N_VERTICES)]
ROOT = VERTS[0]  # first vertex is root


def time_block(fn, *args, reps=1):
    start = time.perf_counter()
    for _ in range(reps):
        fn(*args)
    return time.perf_counter() - start


def avg_time(fn, *args, reps=1):
    """
    average seconds per call
    """
    total = time_block(fn, *args, reps=reps)
    return total / reps


def main():
    print(f"Creating fully connected graph with {N_VERTICES} vertices…")
    t0 = time.perf_counter()
    g = Graph()
    for u in VERTS:
        for v in VERTS:
            if u != v:
                g.insertEdge(u, v, TEST_SEM)
    t_graph = time.perf_counter() - t0
    print(f"Graph construction: {t_graph*1e3:.0f} ms")
    t0 = time.perf_counter()
    tcm = TCM.from_graph(g, [TEST_SEM])
    t_tcm = time.perf_counter() - t0
    print(f"TCM construction: {t_tcm*1e3:.0f} ms")

    # accounts for first call taking longer
    _ = g.postreqs(ROOT, TEST_SEM)
    _ = tcm.postreqs(ROOT, TEST_SEM)

    bfs_avg = avg_time(g.postreqs, ROOT, TEST_SEM, reps=REPS)
    tcm_avg = avg_time(tcm.postreqs, ROOT, TEST_SEM, reps=LOOKUPS)
    print(f"BFS average: {bfs_avg*1e3:.5f} ms")
    print(f"TCM average: {tcm_avg*1e3:.5f} ms")


if __name__ == "__main__":
    main()
