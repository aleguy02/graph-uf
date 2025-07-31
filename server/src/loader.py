import json, re
from pathlib import Path
from .graph import Graph

_JSON_PATH = Path(__file__).parent / "json" / "soc_cleaned.json"
_COURSE_RE = re.compile(r"\b[A-Z]{3,4}\s?\d{4}[A-Z]?\b")


def _extract_codes(s: str):
    s = s.split("Coreq")[0]  # we don't care about prerequisites
    return (c.replace(" ", "") for c in _COURSE_RE.findall(s or ""))


def build_graph() -> Graph:
    data = json.loads(_JSON_PATH.read_text(encoding="utf-8"))
    g = Graph()
    for c in data["courses"]:
        tgt = c["code"].strip().upper()
        for p in _extract_codes(c.get("prerequisites", "")):
            g.insertEdge(p.upper(), tgt)
    return g
