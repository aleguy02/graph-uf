import time
from pathlib import Path
import sys

#ensures project root is on sys.path when the script is run directly
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app

SEMESTER = "f25" #fall 2025 chosen for its large course list
ROOTS = ["MAC2311", "CHM2045", "COP3502C", "CAP4410"] #different amounts of postreqs, for comparison
REPS = 10_000


def avg_time(func, *args, reps=REPS) -> float:
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

    print("Course     Postreqs |  BFS (µs) | TCM (µs)")
    print("-------------------------------------------")

    for root in ROOTS:
        bfs_us  = avg_time(graph.postreqs, root, SEMESTER) * 1e6
        tcm_us  = avg_time(tcm.postreqs,   root, SEMESTER) * 1e6
        count   = len(tcm.postreqs(root, SEMESTER))

        print(
            f"{root:<10}{count:9d} | "
            f"{bfs_us:8.2f} | {tcm_us:8.2f}"
        )


if __name__ == "__main__":
    main()