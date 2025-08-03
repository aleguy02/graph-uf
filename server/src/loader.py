import json, re
from pathlib import Path
from .graph import Graph
from .tcm import TCM

semesters = [
    # 2018
    "f18",

    # 2019
    "sp19",
    "sm19",
    "f19",

    # 2020
    "sp20",
    "sm20",
    "f20",

    # 2021
    "sp21",
    "sm21",
    "f21",

    # 2022
    # "sp22",  # this file isn't being created atm so comment it out to avoid errors with build_graph()
    "sm22",
    "f22",

    # 2023
    "sp23",
    "sm23",
    "f23",

    # 2024
    "sp24",
    "sm24",
    "f24",

    # 2025
    "sp25",
    "sm25",
    "f25",
]

_JSON_PATHS = [Path(__file__).parent / "json" / f"soc_cleaned_{s}.json" for s in semesters]
_COURSE_RE = re.compile(r"\b[A-Z]{3,4}\s?\d{4}[A-Z]?\b")


def _extract_codes(s: str):
    s = s.split("Coreq")[0]  # we don't care about corequisites
    return (c.replace(" ", "") for c in _COURSE_RE.findall(s or ""))


def build_graph() -> Graph:
    g = Graph()

    for sem, fp in zip(semesters, _JSON_PATHS):
        if not fp.exists(): #for missing semesters
            continue

        data = json.loads(fp.read_text(encoding="utf-8"))
        for c in data["courses"]:
            tgt = c["code"].strip().upper()
            for p in _extract_codes(c.get("prerequisites", "")):
                g.insertEdge(p.upper(), tgt, sem)
    return g

def build_tcm() -> TCM:
    graph = build_graph()
    tcm = TCM.from_graph(graph, semesters)
    return tcm

