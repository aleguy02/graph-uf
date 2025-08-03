import time
from pathlib import Path
import sys

#ensures project root is on sys.path when the script is run directly
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app

SEMESTER = "f25" #fall 2025 chosen for its large course list
GRAPH_REPS = 1
TCM_REPS = 100

def avg_time(func, *args, reps: int = 1) -> float:
    """average seconds per call"""
    t0 = time.perf_counter()
    for _ in range(reps):
        func(*args)
    return (time.perf_counter() - t0) / reps


def main() -> None:
    #starts the app to test in real environment
    app = create_app({"TESTING": True})
    graph = app.config["COURSE_GRAPH"]
    tcm = app.config["COURSE_TCM"]

    courses = sorted(graph.getAdjList().keys())
    print("Course     Postreqs |  BFS (µs) | TCM (µs)")
    print("-------------------------------------------")

    sum_bfs = 0.0
    sum_tcm = 0.0
    sum_count = 0
    for root in courses:
        bfs_us = avg_time(graph.postreqs, root, SEMESTER, reps=GRAPH_REPS) * 1e6
        tcm_us = avg_time(tcm.postreqs, root, SEMESTER, reps=TCM_REPS) * 1e6
        count = len(tcm.postreqs(root, SEMESTER))

        sum_bfs += bfs_us
        sum_tcm += tcm_us
        sum_count += count

    avg_count = sum_count / len(courses)
    avg_bfs = sum_bfs / len(courses)
    avg_tcm = sum_tcm / len(courses)

    print(f"{'AVERAGE':<10}{avg_count:9.2f} | {avg_bfs:9.2f} | {avg_tcm:8.2f}")


if __name__ == "__main__":
    main()