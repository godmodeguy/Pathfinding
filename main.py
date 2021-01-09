import pygame
import sys
import numpy as np
from pathfinder import Node, breadth_first_search, dijkstra_search


class GridNode(Node):
    MAX_PASSABLE_WEIGHT = 9

    def __init__(self, position, weight):
        Node.__init__(self, weight)
        self.position = position

    def __repr__(self):
        return f'GridNode({self.position[0]}:{self.position[1]})'


class PathfindingGUI:
    START_COLOR = (0, 200, 0)
    TARGET_COLOR = (200, 0, 0)
    WEIGHT_COLOR = np.array((250, 250, 250))
    PATH_COLOR = (0, 0, 250, 40)  # fourth value for transparency
    WEIGHT_FACTOR = 25  # step for changing cell color by weight
    INIT_WEIGHT = 3

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.width, self.height = (1600, 800)
        self.bsize = 25
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.path = []
        self.grid = None
        self.create_grid()

        self.start = self.grid[0, 0]
        self.target = self.grid[0, 1]

        self.dragging_start = self.dragging_target = False

    def mainloop(self):
        while True:
            # clear path every frame, hold Space to instantly update
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.path = dijkstra_search(self.start, self.target)

            else:
                self.path = []

            self.keyboard_handle()
            self.mouse_handle()
            self.render()

            self.clock.tick(20)

    def create_grid(self):
        self.grid = np.empty((self.height // self.bsize, self.width // self.bsize), dtype=object)

        # fill grid with nodes
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                self.grid[x, y] = GridNode((x, y), self.INIT_WEIGHT)

        # creating links between grid nodes
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if x > 0:
                    self.grid[x, y].add_neighbour(self.grid[x-1, y])
                if x < self.height//self.bsize - 1:
                    self.grid[x, y].add_neighbour(self.grid[x+1, y])
                if y > 0:
                    self.grid[x, y].add_neighbour(self.grid[x, y-1])
                if y < self.width//self.bsize - 1:
                    self.grid[x, y].add_neighbour(self.grid[x, y+1])

    def keyboard_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Ctrl+C - return to start state
                    self.create_grid()
                    self.start = self.grid[0, 0]
                    self.target = self.grid[0, 1]

    def mouse_handle(self):
        if not pygame.mouse.get_focused():
            return

        left, center, right = pygame.mouse.get_pressed(3)
        y, x = pygame.mouse.get_pos()
        y, x = y // self.bsize, x // self.bsize

        # drag and drop start and target
        if self.dragging_start or self.dragging_target:
            if self.dragging_start:
                self.start = self.grid[x, y]
                self.dragging_start = left
            else:
                self.target = self.grid[x, y]
                self.dragging_target = left
            return

        if left:
            # start dragging
            if (x, y) == self.start.position:
                self.dragging_start = True
            elif (x, y) == self.target.position:
                self.dragging_target = True

            # increase weight when holding left button on cell
            elif self.grid[x, y].weight < 10:
                self.grid[x, y].weight += 1

        elif right:
            # decrease weight when holding right button on cell
            if self.grid[x, y].weight > 0:
                self.grid[x, y].weight -= 1

    def render(self):
        bs = self.bsize

        # draw grid
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                color = self.WEIGHT_COLOR - self.grid[x, y].weight * self.WEIGHT_FACTOR
                pygame.draw.rect(self.screen, list(map(int, color)),
                                 (y*bs, x*bs, bs-1, bs-1))

        # draw path in a special way for transparency
        for node in self.path:
            s = pygame.Surface((bs - 1, bs - 1), pygame.SRCALPHA)
            s.fill(self.PATH_COLOR)
            self.screen.blit(s, (node.position[1] * bs, node.position[0] * bs))

        # draw start cell
        pygame.draw.rect(self.screen, self.START_COLOR,
                         (self.start.position[1] * bs, self.start.position[0] * bs, bs - 1, bs - 1))

        # draw target cell
        pygame.draw.rect(self.screen, self.TARGET_COLOR,
                         (self.target.position[1] * bs, self.target.position[0] * bs, bs - 1, bs - 1))

        pygame.display.flip()


if __name__ == '__main__':
    PathfindingGUI().mainloop()
