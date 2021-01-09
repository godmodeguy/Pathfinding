
class PathFinder:
    def __init__(self):
        pass

    def find(self, start, end):
        return [start, end]


class Node:
    def __init__(self):
        self.neighbours = {}

    def add_neighbour(self, node, weight):
        self.neighbours[node] = weight

    def get_neighbours(self):
        return self.neighbours.keys()
