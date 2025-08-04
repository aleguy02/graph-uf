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


def course_info() -> dict:
    course_info = {}
    debug_count = 0

    for sem, fp in zip(semesters, _JSON_PATHS):
        if not fp.exists():
            continue

        data = json.loads(fp.read_text(encoding="utf-8"))
        for c in data["courses"]:

            code = c.get("code", "").strip().upper()
            if not code:
                continue

            if debug_count < 3:
                print(f"DEBUG {code}: credits_min='{c.get('credits_min')}', credits_max='{c.get('credits_max')}'")
                print(f"DEBUG {code}: sample keys = {list(c.keys())[:10]}")  # First 10 keys
                debug_count += 1

            if code not in course_info:
                course_info[code] = {
                    "title": "No title",
                    "credits": "N/A",
                    "description": "No description",
                }

            title_fields = ["title", "name", "course_title", "courseName", "course_name"]
            for field in title_fields:
                title = c.get(field, "")
                if isinstance(title, str) and title.strip():
                    title = title.strip()
                    if title != "No title":
                        course_info[code]["title"] = title
                        break

            credits_min = c.get("credits_min")
            credits_max = c.get("credits_max")

            if code in ["PHI6905", "PHI6910", "PHI6934"]:
                print(f"DEBUG {code}: credits_min='{credits_min}', credits_max='{credits_max}'")
                print(f"DEBUG {code}: all keys = {list(c.keys())}")

            if credits_min is not None and credits_max is not None:
                try:
                    min_val = int(credits_min) if credits_min != "" and credits_min != "N/A" else None
                    max_val = int(credits_max) if credits_max != "" and credits_max != "N/A" else None

                    if min_val is not None and max_val is not None:
                        if min_val == max_val:
                            course_info[code]["credits"] = str(min_val)
                        else:
                            course_info[code]["credits"] = "VAR"
                    elif min_val is not None:
                        course_info[code]["credits"] = str(min_val)
                    elif max_val is not None:
                        course_info[code]["credits"] = str(max_val)
                except (ValueError, TypeError):
                    pass

            if course_info[code]["credits"] == "N/A":
                credit_fields = ["credits", "credit_hours", "credit", "hours", "creditHours", "units", "hrs", "ch"]
                for field in credit_fields:
                    credits = c.get(field, "")
                    if credits and str(credits).strip():
                        if isinstance(credits, str):
                            credits = re.sub(r'[\x00-\x1f\x7f-\x9f\[\]H;]', '', credits).strip()
                            if credits and credits.upper() not in ["N/A", "NO", "NONE", ""]:
                                course_info[code]["credits"] = credits
                                break
                        elif isinstance(credits, (int, float)):
                            course_info[code]["credits"] = str(credits)
                            break

            description = c.get("description", "")
            if isinstance(description, str) and description.strip():

                description = re.sub(r'[\x00-\x1f\x7f-\x9f]|□\[\d+;\d*[A-Za-z]', '', description).strip()
                if description and description != "No description":
                    course_info[code]["description"] = description

    return course_info


if __name__ == "__main__":
    from pprint import pprint
    pprint(course_info())
