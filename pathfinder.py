from collections import deque


class Node:
    MAX_PASSABLE_WEIGHT = float('inf')

    def __init__(self, weight):
        self.neighbours = {}
        self.weight = weight

    def add_neighbour(self, node):
        self.neighbours[node] = node.weight

    def get_neighbours(self):
        return [n for n in self.neighbours.keys() if n.weight <= self.MAX_PASSABLE_WEIGHT]


def breadth_first_search_c(start, end):
    frontier = deque()
    frontier.appendleft(start)
    came_from = {start: None}

    while len(frontier):
        current = frontier.pop()
        for neighbour in current.get_neighbours():
            if neighbour not in came_from:
                frontier.appendleft(neighbour)
                came_from[neighbour] = current

    path = []
    t = end
    while came_from[t] != start:
        t = came_from[t]
        path.append(t)

    return path

