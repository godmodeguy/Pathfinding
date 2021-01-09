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


class PriorityQueue:
    def __init__(self):
        self.queue = dict()  # (item, priority)

    def put(self, item, priority):
        self.queue[item] = priority

    def get(self):
        if self.empty():
            return None

        max_priority = float('inf')
        max_priority_item = None
        for item, priority in self.queue.items():
            if priority < max_priority:
                max_priority = priority
                max_priority_item = item

        del self.queue[max_priority_item]
        return max_priority_item

    def empty(self):
        return len(self.queue) == 0


def breadth_first_search(start, end):
    frontier = deque()  # queue to check node
    frontier.appendleft(start)
    came_from = {start: None}  # from what node (value) we come to this (key)

    while len(frontier):
        current = frontier.pop()

        # greedy stop, we find what we want
        if current == end:
            break

        for neighbour in current.get_neighbours():
            if neighbour not in came_from:
                frontier.appendleft(neighbour)
                came_from[neighbour] = current

    if end not in came_from.keys():
        # there's no way to end
        return []
    return restore_path(came_from, start, end)


def dijkstra_search(start, end):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {start: None}
    cost = {start: 0}

    while not frontier.empty():
        current = frontier.get()

        # greedy stop, we find what we want
        if current == end:
            break

        for neighbour in current.get_neighbours():
            new_cost = cost[current] + neighbour.weight
            if neighbour not in cost or new_cost < cost[neighbour]:
                cost[neighbour] = new_cost
                frontier.put(neighbour, new_cost)
                came_from[neighbour] = current

    if end not in came_from.keys():
        # there's no way to end
        return []
    return restore_path(came_from, start, end)


def restore_path(came_from, start, end):
    path = []
    t = end
    while came_from[t] != start:
        t = came_from[t]
        path.append(t)

    return path
