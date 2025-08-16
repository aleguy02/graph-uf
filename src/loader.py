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

_JSON_PATHS = [
    Path(__file__).parent / "json" / f"soc_cleaned_{s}.json" for s in semesters
]
_COURSE_RE = re.compile(r"\b[A-Z]{3,4}\s?\d{4}[A-Z]?\b")


def _extract_codes(s: str):
    s = s.split("Coreq")[0]  # we don't care about corequisites
    return (c.replace(" ", "") for c in _COURSE_RE.findall(s or ""))


def build_graph() -> Graph:
    g = Graph()

    for sem, fp in zip(semesters, _JSON_PATHS):
        if not fp.exists():  # for missing semesters
            continue

        data = json.loads(fp.read_text(encoding="utf-8"))
        for c in data["courses"]:
            tgt = c["code"].strip().upper()
            for p in _extract_codes(c.get("prerequisites", "")):
                g.insertEdge(p.upper(), tgt, sem)
    return g

import re

_SEM_RE = re.compile(r'^(f|sp|sm)(\d{2})$')
def _parse_sem(sem: str) -> tuple[str, int]:
    m = _SEM_RE.match(sem)
    if not m:
        raise ValueError(f"Bad semester code: {sem}")
    term, yy = m.groups()
    return term, 2000 + int(yy)

def _same_season_fallback(target_sem: str, available: dict[str, bool], all_sems: list[str]) -> str | None:
    """
    Find the latest available same-season term <= target year.
    Return None if none exists (e.g., 'sm18' when there's no earlier Summer).
    """
    term, year = _parse_sem(target_sem)
    for s in reversed(all_sems):
        t, y = _parse_sem(s)
        if t == term and y <= year and available.get(s, False):
            return s
    return None


def _build_academic_year_bundles(all_sems: list[str], json_paths: list[Path]) -> dict[str, list[str]]:
    # availability map based on existing JSON files
    available = {s: fp.exists() for s, fp in zip(all_sems, json_paths)}

    # get candidate years from list
    years = sorted({_parse_sem(s)[1] for s in all_sems})
    bundles: dict[str, list[str]] = {}

    for y in years:
        sm = f"sm{str(y)[-2:]}"
        fa = f"f{str(y)[-2:]}"
        sp = f"sp{str(y + 1)[-2:]}"

        # only build if at least one of the three is in the configured semester list
        present_any = any(s in all_sems for s in (sm, fa, sp))
        if not present_any:
            continue

        terms = []
        for target in (sm, fa, sp):
            effective = target if available.get(target, False) else _same_season_fallback(target, available, all_sems)
            terms.append(effective)

        bundle_key = f"AY{y}-{y+1}"
        bundles[bundle_key] = terms

    return bundles

def build_tcm() -> TCM:
    graph = build_graph()
    tcm = TCM.from_graph(graph, semesters)
    # build bundles, compute into tcm
    bundles = _build_academic_year_bundles(semesters, _JSON_PATHS)
    tcm.add_bundles(graph, bundles)
    return tcm


def build_tooltip():
    tooltip = {}

    for sem, fp in zip(semesters, _JSON_PATHS):
        if not fp.exists():
            continue

        data = json.loads(fp.read_text(encoding="utf-8"))

        tooltip[sem] = {}
        for c in data["courses"]:

            code = c.get("code", "").strip().upper()
            name = c.get("name", "")

            description = c.get("description", "").replace("\n", " ")
            if not description:
                description = "No description given"

            prerequisites = c.get("prerequisites", "")

            sections = c.get("sections", [])
            credits = sections[0].get("credits", "") if sections else ""

            tooltip[sem][code] = {
                "name": name,
                "description": description,
                "prerequisites": prerequisites,
                "credits": credits,
            }

    return tooltip
