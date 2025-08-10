"""
Adjacency list representation of graph; FROM prereqs TO class
"""

from collections import deque


class Graph:
    def __init__(self):
        self.adj_list: dict[str, dict[str, set[str]]] = (
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

    def postreqs(self, root: str, semester: str) -> set[str]:
        """
        BFS traversal from root to all reachable nodes.
        Returns all classes that require root as in their prerequisite chain
        Only traverses along given semester
        """
        root = root.upper()
        if root not in self.adj_list:
            raise ValueError("Node not in graph")

        v = set()
        q = deque([root])

        while q:
            node = q.popleft()
            if node in v:
                continue

            v.add(node)

            for neighbor, sems in self.adj_list[node].items():
                if semester in sems and neighbor not in v:
                    q.append(neighbor)

        v.remove(root)
        return v

    def getDirectPostreqs(self, course: str, semester: str) -> set[str]:
        res = set()
        neighbors = self.adj_list[course]

        for neighbor, sems_available in neighbors.items():
            if semester in sems_available:
                res.add(neighbor)

        return res
