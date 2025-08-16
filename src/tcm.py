from collections.abc import Mapping
from .graph import Graph
from collections import deque
from typing import Iterable

class TCM:
    def __init__(self, closure: Mapping[str, Mapping[str, set[str]]]):
        copied = {}  # dict[str, dict[str, set[str]]]
        # deep copy
        for semester, course_map in closure.items():
            copied[semester] = {}
            for course, postreqs in course_map.items():
                copied[semester][course] = set(postreqs)

        self._map = copied
        self._bundle_terms: dict[str, list[str]] = {}
        self._bundle_alias: dict[frozenset[str], str] = {}

    def add_bundles(self, graph, bundles: dict[str, list[str]]) -> None:
        """
        Precompute closures for each bundle key -> list of effective semester codes.
        Stores results in self._map[<bundle_key>] so postreqs() is O(1).
        """
        self._bundle_terms = dict(bundles)

        for k, terms in bundles.items():
            self._bundle_alias[frozenset(terms)] = k

        # collect course codes
        adj = graph.getAdjList()
        codes: set[str] = set(adj.keys())
        for nbrs in adj.values():
            codes.update(nbrs.keys())

        # precompute closure per bundle by traversing the union of edges
        def _postreqs_union(root: str, sems: set[str]) -> set[str]:
            root = root.upper()
            if root not in adj:
                return set()
            seen: set[str] = set()
            q = deque([root])
            while q:
                node = q.popleft()
                if node in seen:
                    continue
                seen.add(node)
                for neighbor, edge_terms in adj[node].items():
                    if edge_terms & sems and neighbor not in seen:
                        q.append(neighbor)
            seen.discard(root)
            return seen

        for bundle_key, term_list in bundles.items():
            sem_set = set(term_list)
            bucket: dict[str, set[str]] = {}
            for c in codes:
                bucket[c] = _postreqs_union(c, sem_set)
            self._map[bundle_key] = bucket

    @classmethod
    def from_graph(cls, g: Graph, semesters: list[str]) -> "TCM":
        closure: dict[str, dict[str, set[str]]] = {}
        for sem in semesters:
            sem_closure: dict[str, set[str]] = {}
            for course in g.getAdjList():
                sem_closure[course] = g.postreqs(course, sem)
            closure[sem] = sem_closure
        return cls(closure)

    def postreqs(self, code: str, semesters: str | Iterable[str]) -> set[str]:
        code = code.upper()

        # single term
        if isinstance(semesters, str):
            semester_map = self._map.get(semesters, {})
            if code not in semester_map:
                raise ValueError(f"Course code '{code}' not found")
            return semester_map[code]

        # multi term
        sem_key = self._bundle_alias.get(frozenset(semesters))
        if sem_key is None:
            raise ValueError(
                "Semester combination has not been precomputed")

        semester_map = self._map.get(sem_key, {})
        if code not in semester_map:
            raise ValueError(f"Course code '{code}' not found")
        return semester_map[code]

