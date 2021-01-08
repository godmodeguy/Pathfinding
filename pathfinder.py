
class PathFinder:
    def __init__(self):
        pass

    def find(self, start, end):
        pass


class Node:
    def __init__(self):
        self.neighbours = []
        self.weights = []

    def add_neighbour(self, node, weight):
        self.neighbours.append(node)
        self.weights.append(weight)
