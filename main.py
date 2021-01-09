import pygame
import sys
import numpy as np
from pathfinder import PathFinder, Node


ALL_NODES = []
class GridNode(Node):
    def __init__(self, pos, weight):
        Node.__init__(self)
        self.weight = weight

        self.pos = f'({pos[0]}:{pos[1]})'
        ALL_NODES.append(self)


class PathfindingGUI:
    START_COLOR = (0, 200, 0)
    TARGET_COLOR = (200, 0, 0)
    WEIGHT_COLOR = np.array((250, 250, 250))
    PATH_COLOR = (0, 0, 200)
    WEIGHT_FACTOR = 25
    INIT_WEIGHT = 3

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.finder = PathFinder()

        self.width, self.height = (1600, 800)
        self.bsize = 25
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.path = [(5, i) for i in range(10, 20)]
        self.grid = None
        self.create_grid()

        self.start = (0, 0)
        self.target = (0, 1)

        self.dragging_start = self.dragging_target = False

    def mainloop(self):
        while True:

            self.keyboard_handle()
            self.mouse_handle()
            self.render()   

            self.clock.tick(20)

    def create_grid(self):
        self.grid = np.empty((self.height // self.bsize, self.width // self.bsize), dtype=object)

        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                self.grid[x, y] = GridNode((x, y), self.INIT_WEIGHT)

        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if x > 0:
                    self.grid[x, y].add_neighbour(self.grid[x-1, y], self.grid[x-1, y])
                if x < self.height//self.bsize - 1:
                    self.grid[x, y].add_neighbour(self.grid[x+1, y], self.grid[x+1, y])
                if y > 0:
                    self.grid[x, y].add_neighbour(self.grid[x, y-1], self.grid[x, y-1])
                if y < self.width//self.bsize - 1:
                    self.grid[x, y].add_neighbour(self.grid[x, y+1], self.grid[x, y+1])

        for node in ALL_NODES:
            print(node.pos, 'neighbours:', ', '.join(k.pos for (k, v) in node.neighbours.items()))


    def find_path(self):
        pass

    def path_to_grid(self, path):
        return 1

    def keyboard_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.fill_grid()
                    self.start = (0, 0)
                    self.target = (0, 1)
                if event.key == pygame.K_SPACE:
                    self.find_path()

    def mouse_handle(self):
        if not pygame.mouse.get_focused():
            return

        left, center, right = pygame.mouse.get_pressed(3)
        y, x = pygame.mouse.get_pos()
        y, x = y // self.bsize, x // self.bsize

        if self.dragging_start or self.dragging_target:
            if self.dragging_start:
                self.start = x, y
                self.dragging_start = left
            else:
                self.target = x, y
                self.dragging_target = left
            return

        if left:
            # drag and drop start and target
            if (x, y) == self.start:
                self.dragging_start = True
            elif (x, y) == self.target:
                self.dragging_target = True

            elif self.grid[x, y].weight < 10:
                self.grid[x, y].weight += 1

        elif right:
            if self.grid[x, y].weight > 0:
                self.grid[x, y].weight -= 1

    def render(self):
        bs = self.bsize

        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                color = self.WEIGHT_COLOR - self.grid[x, y].weight * self.WEIGHT_FACTOR
                pygame.draw.rect(self.screen, list(map(int, color)),
                                 (y*bs, x*bs, bs-1, bs-1))

        for (x, y) in self.path:
            pygame.draw.rect(self.screen, self.PATH_COLOR,
                             (y * bs, x * bs, bs - 1, bs - 1))

        pygame.draw.rect(self.screen, self.START_COLOR,
                         (self.start[1] * bs, self.start[0] * bs, bs - 1, bs - 1))

        pygame.draw.rect(self.screen, self.TARGET_COLOR,
                         (self.target[1] * bs, self.target[0] * bs, bs - 1, bs - 1))

        pygame.display.flip()


if __name__ == '__main__':
    PathfindingGUI().mainloop()
