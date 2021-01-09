
class PathFinder:
    def __init__(self):
        pass

    def find(self, start, end):
        pass


class Node:
    def __init__(self):
        self.neighbours = {}

    def add_neighbour(self, node, weight):
        self.neighbours[node] = weight
