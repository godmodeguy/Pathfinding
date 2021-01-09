from collections import deque


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


def bfs(start, end):
    frontier = deque()
    frontier.appendleft(start)
    came_from = {start: None}

    while len(frontier):
        current = frontier.pop()
        for next_ in current.get_neighbours():
            if next_ not in came_from:
                frontier.appendleft(next_)
                came_from[next_] = current

    path = []
    t = end
    while came_from[t] != start:
        t = came_from[t]
        path.append(t)

    return path

