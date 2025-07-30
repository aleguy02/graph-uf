"""
Adjacency list representation of graph; FROM prereqs TO class
"""

from collections import deque


class Graph:
    def __init__(self):
        self.adj_list: dict[str, set[str]] = {}

    def insertEdge(self, from_: str, to_: str):  # `from` keyword is reserved in python
        if from_ not in self.adj_list:
            self.adj_list[from_] = {to_}
        else:
            self.adj_list[from_].add(to_)

        if to_ not in self.adj_list:
            self.adj_list[to_] = set()

    def getAdjList(self):
        return self.adj_list

    def postreqs(self, root: str):
        """
        Returns all classes that require root as in their prerequisite chain
        """
        if root not in self.adj_list:
            raise ValueError("Node not in graph")

        v = set()
        q = deque()
        q.append(root)

        while q:
            node = q[0]
            q.popleft()
            if node in v:
                continue

            v.add(node)

            for neighbor in self.adj_list[node]:
                if neighbor not in v:
                    q.append(neighbor)

        v.remove(root)
        return v
