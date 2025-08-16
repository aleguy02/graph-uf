"""
Adjacency list representation of graph; FROM prereqs TO class
"""

from collections import deque
from typing import Iterable

class Graph:
    def __init__(self):
        self.adj_list: dict[
            str, dict[str, set[str]]
        ] = (
            {}
        )  # adj_list stores: {  COURSE_CODE: { UNLOCKED_COURSE: [ SEMESTERS... ] }  }

    def insertEdge(
        self, from_: str, to_: str, semester: str
    ):  # `from` keyword is reserved in python
        from_ = from_.upper()
        to_ = to_.upper()

        if from_ not in self.adj_list:
            self.adj_list[from_] = {}
        if to_ not in self.adj_list:
            self.adj_list[to_] = {}

        self.adj_list[from_].setdefault(to_, set()).add(semester)

    def getAdjList(self):
        return self.adj_list

    def postreqs(self, root: str, semesters: str | Iterable[str]) -> set[str]:
        """
        BFS traversal from root to all reachable nodes.
        Returns all classes that require root as in their prerequisite chain
        Only traverses along given semesters
        """
        root = root.upper()
        if root not in self.adj_list:
            raise ValueError("Node not in graph")

        sem_set = {semesters} if isinstance(semesters, str) else set(semesters)
        v = set()
        q = deque([root])

        while q:
            node = q.popleft()
            if node in v:
                continue

            v.add(node)

            for neighbor, sems_available in self.adj_list[node].items():
                if sems_available & sem_set and neighbor not in v:
                    q.append(neighbor)

        v.remove(root)
        return v

    def getDirectPostreqs(self, course: str, semesters: str | Iterable[str]) -> set[str]:
        sem_set = {semesters} if isinstance(semesters, str) else set(semesters)
        res = set()
        neighbors = self.adj_list[course]

        for neighbor, sems_available in neighbors.items():
            if sems_available & sem_set:
                res.add(neighbor)

        return res
