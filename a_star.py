import heapq
import time

import pygame

START = (100, 100, 100)
END = (200, 200, 200)
OBSTACLE = (0, 0, 0)
PATH = (0, 255, 0)
NEIGHBOR = (255, 0, 255)
CLOSED = (0, 0, 255)
CURRENT = (255, 0, 0)



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other: "Point"):
        dx = self.x - other.x
        dy = self.y - other.y
        return dx**2 + dy**2

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Tile:
    def __init__(self, x: int, y: int, obstacle: bool = False):
        self.color = (255, 255, 255) if not obstacle else OBSTACLE
        self.x = x
        self.y = y
        self.obstacle = obstacle


class Grid:
    def __init__(self, width, height, tile_width, tile_height):
        self.width = width
        self.height = height
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.columns = width // tile_width
        self.rows = height // tile_height
        self.tiles = []
        self.generate_tiles()
        self.start = Node(Point(10, 10), 0, 0, None)
        self.end = Node(Point(15, 15), 0, 0, None)

        self.set_color_at(self.start.position, START)
        self.set_color_at(self.end.position, END)

    def generate_tiles(self):
        for y in range(0, self.rows):
            row = []
            for x in range(0, self.columns):
                is_obstacle = y == 12 and 2 < x < 17
                row.append(Tile(x, y, is_obstacle))
            self.tiles.append(row)

    def tile_at(self, point: Point) -> Tile:
        return self.tiles[point.x][point.y]

    def set_color_at(self, point: Point, color):
        self.tiles[point.x][point.y].color = color

    def render(self, surface):
        for row in self.tiles:
            for tile in row:
                rect = pygame.Rect(tile.x * self.tile_width, tile.y * self.tile_height, self.tile_width, self.tile_height)
                pygame.draw.rect(surface, tile.color, rect)
                pygame.draw.rect(surface, (0,0,0), rect, 1)
        pygame.display.flip()



class Node:
    def __init__(self, point: Point, distance: int, heuristic: int, previous: "Node"):
        self.position = point
        self.distance = distance
        self.heuristic = heuristic
        self.total = distance + heuristic
        self.previous = previous

    def __lt__(self, other):
        return self.total < other.total


class AStar:
    def __init__(self, start: Node, end: Node, grid: Grid, surface):
        self.start = start
        self.open = [start]
        self.closed = []
        self.end = end
        self.grid = grid
        self.surface = surface

    def in_grid(self, point: Point):
        return 0 <= point.x < self.grid.columns and 0 <= point.y <= self.grid.rows

    def generate_successors(self,  node: Node):
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                point = Point(node.position.x + i, node.position.y + j)
                if self.in_grid(point) and not self.grid.tile_at(point).obstacle:
                    neighbours.append(Node(point, node.distance + 1, point.distance(self.end.position), node))
        return neighbours

    def compute(self, display):
        self.open = [self.start]
        self.closed = []
        while len(self.open) > 0:
            node = heapq.heappop(self.open)
            self.grid.set_color_at(node.position, CURRENT)

            if display:
                self.grid.render(self.surface)
            for successor in self.generate_successors(node):
                if display:
                    self.grid.render(self.surface)
                if successor.position == self.end.position:
                    return successor
                found_better_node = False
                for n in self.open:
                    if n.position == successor.position and n.total < successor.total:
                        found_better_node = True
                if found_better_node:
                    continue
                for n in self.closed:
                    if n.position == successor.position and n.total < successor.total:
                        found_better_node = True
                if found_better_node:
                    continue
                self.grid.set_color_at(successor.position, NEIGHBOR)

                heapq.heappush(self.open, successor)
            self.grid.set_color_at(node.position, CLOSED)
            self.closed.append(node)
            if display:
                self.grid.render(self.surface)
                time.sleep(.5)




