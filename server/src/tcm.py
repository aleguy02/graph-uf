from collections.abc import Mapping
from .graph import Graph

class TCM:
    def __init__(self, closure: Mapping[str, set[str]]):
        self._map: dict[str, set[str]] = dict(closure)

    @classmethod
    def from_graph(cls, g: Graph) -> "TCM":
        closure: dict[str, set[str]] = {}
        for course in g.getAdjList():
            downstream = g.postreqs(course)
            closure[course] = downstream

        return cls(closure)

    def postreqs(self, code: str) -> set[str]:
        return self._map.get(code.upper(), set())