from collections.abc import Mapping
from .graph import Graph


class TCM:
    def __init__(self, closure: Mapping[str, Mapping[str, set[str]]]):
        copied = {}  # dict[str, dict[str, set[str]]]
        # deep copy
        for semester, course_map in closure.items():
            copied[semester] = {}
            for course, postreqs in course_map.items():
                copied[semester][course] = set(postreqs)

        self._map = copied

    @classmethod
    def from_graph(cls, g: Graph, semesters: list[str]) -> "TCM":
        closure: dict[str, dict[str, set[str]]] = {}
        for sem in semesters:
            sem_closure: dict[str, set[str]] = {}
            for course in g.getAdjList():
                sem_closure[course] = g.postreqs(course, sem)
            closure[sem] = sem_closure
        return cls(closure)

    def postreqs(self, code: str, semester: str) -> set[str]:
        semester_map = self._map.get(semester, {})
        if code.upper() not in semester_map:
            raise ValueError(f"Course code '{code}' not found")

        return semester_map[code.upper()]
