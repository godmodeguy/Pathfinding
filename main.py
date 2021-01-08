import pygame
import sys
import numpy as np
from pathfinder import PathFinder, Node


ALL_NODES = []
class GridNode(Node):
    def __init__(self, pos):
        Node.__init__(self)

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
        self.grid = np.empty((self.height // self.bsize, self.width // self.bsize))
        self.grid.fill(self.INIT_WEIGHT)

        self.start = (0, 0)
        self.target = (0, 1)

        self.dragging_start = self.dragging_target = False

    def mainloop(self):
        while True:

            self.keyboard_handle()
            self.mouse_handle()
            self.render()   

            self.clock.tick(20)
    
    def create_graph(self):

        init_node = GridNode((0, 0))

        node_l1 = GridNode((0, 1))
        node_l1.add_neighbour(init_node, self.grid[1, 0])

        node_r1 = init_node
        node_r2 = GridNode((1, 0))
        node_r2.add_neighbour(node_r1, self.grid[0, 0])

        for x in range(1, self.grid.shape[0]-1):
            for y in range(1, self.grid.shape[1]-1):
                node_r1.add_neighbour(node_r2, self.grid[x, y+1])
                node_r2.add_neighbour(node_r1, self.grid[x, y])
                node_r1 = node_r2
                node_r2 = GridNode((x, y))

                node_l1.add_neighbour(node_r2, self.grid[x+1, y])
                node_l1 = GridNode((x+1, y))

            t = node_r1
            node_r1 = node_l1
            node_r2 = GridNode((x, y))

            node_l1 = GridNode((x, y))
            node_l1.add_neighbour(t, self.grid[x+1, 0])

        for node in ALL_NODES:
            print(node.pos, 'neighbours:', ', '.join(n.pos for n in node.neighbours))

        sys.exit()



    def find_path(self):
        start, end = self.create_graph()
        path = self.finder.find(start, end)
        self.path = self.path_to_grid(path)

    def path_to_grid(self, path):
        return 1


    def keyboard_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.grid.fill(self.INIT_WEIGHT)
                    self.start = (0, 0)
                    self.target = (0, 1)
                if event.key == pygame.K_SPACE:
                    self.find_path()

    def mouse_handle(self):
        if not pygame.mouse.get_focused():
            return

        left, center, right = pygame.mouse.get_pressed(3)
        x, y = pygame.mouse.get_pos()
        x, y = x // self.bsize, y // self.bsize

        if self.dragging_start or self.dragging_target:
            if self.dragging_start:
                self.start = y, x
                self.dragging_start = left
            else:
                self.target = y, x
                self.dragging_target = left
            return

        if left:
            # drag and drop start and target
            if (y, x) == self.start:
                self.dragging_start = True
            elif (y, x) == self.target:
                self.dragging_target = True

            elif self.grid[y, x] < 10:
                self.grid[y, x] += 1

        elif right:
            if self.grid[y, x] > 0:
                self.grid[y, x] -= 1

    def render(self):
        bs = self.bsize

        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                color = self.WEIGHT_COLOR - self.grid[x, y] * self.WEIGHT_FACTOR
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
