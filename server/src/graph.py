"""
Adjacency list representation of graph; FROM prereqs TO class
"""


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
