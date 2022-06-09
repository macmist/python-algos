import pygame
import random

from pygame.locals import *
from a_star import *

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.width, self.height = 640, 400
        self.grid = Grid(self.width, self.height, 20, 20)
        self.astar = AStar(self.grid.start, self.grid.end, self.grid, self._display_surf)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.astar.surface = self._display_surf

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            end = self.astar.compute(True)
            while end != None:
                self.grid.set_color_at(end.position, PATH)
                end = end.previous
                self.grid.render(self._display_surf)

    def on_loop(self):
        pass

    def on_render(self):
        self.grid.render(self._display_surf)
        pass

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()

