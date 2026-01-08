import pygame
import random
import sys
from agent import Agent
from assets import images_init
from popup import draw_popup

N = 12
CELL = 50
HUD_WIDTH = 60
WIDTH = HUD_WIDTH + N * CELL
HEIGHT = N * CELL
MAP_OFFSET_X = HUD_WIDTH
FPS = 2

WALL_COUNT = 22
MOVES_LIMIT = 300
MIN_DISTANCE = 8

VISION = 2
SENSE_RANGE = 3


BG = (20, 20, 40)
GRID = (180, 180, 220)
HERO = (50, 150, 255)
DEMON = (220, 50, 50)
SWORD = (50, 220, 80)
WALL = (100, 100, 140)
FOG = (30, 30, 50)
TEXT = (255, 255, 255)
POPUP_BG = (200, 180, 120)
POPUP_BORDER = (100, 50, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Demon World")
font = pygame.font.SysFont("arial", 18, bold=True)
clock = pygame.time.Clock()
images = images_init(CELL, pygame)

def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def random_pos(exclude):
    while True:
        p = (random.randint(0, N-1), random.randint(0, N-1))
        if p not in exclude:
            return p

def random_pos_with_min_dist(exclude, origin, min_dist):
    while True:
        p = (random.randint(0, N-1), random.randint(0, N-1))
        if p not in exclude and manhattan(p, origin) >= min_dist:
            return p
        

class World:
    def __init__(self):
        self.N = N
        self.hero = random_pos([])
        
        self.sword = random_pos_with_min_dist(
            exclude=[self.hero],
            origin=self.hero,
            min_dist=MIN_DISTANCE
        )

        self.demon = random_pos_with_min_dist(
            exclude=[self.hero, self.sword],
            origin=self.hero,
            min_dist=MIN_DISTANCE
        )

        while manhattan(self.hero, self.sword) <= 1:
            self.sword = random_pos([self.hero])

        while manhattan(self.hero, self.demon) <= 1:
            self.demon = random_pos([self.hero, self.sword])

        self.walls = set()
        while len(self.walls) < WALL_COUNT:
            w = random_pos([self.hero, self.sword, self.demon])
            self.walls.add(w)

        self.has_sword = False
        self.done = False
        self.win = False
        self.move_count = 0

    def blocked(self, p):
        return (
            p in self.walls or
            p == self.hero or
            p == self.demon or
            p[0] < 0 or p[0] >= N or
            p[1] < 0 or p[1] >= N
        )

    def move_demon(self):
        dx, dy = self.demon
        current_dist = manhattan(self.demon, self.hero)

        moves = [
            (dx, dy),        
            (dx + 1, dy),
            (dx - 1, dy),
            (dx, dy + 1),
            (dx, dy - 1)
        ]

        valid_moves = [m for m in moves if not self.blocked(m)]

        if not valid_moves:
            return

        non_flee_moves = [
            m for m in valid_moves
            if manhattan(m, self.hero) <= current_dist
        ]

        if not non_flee_moves:
            return

        min_dist = min(manhattan(m, self.hero) for m in non_flee_moves)
        best_moves = [m for m in non_flee_moves if manhattan(m, self.hero) == min_dist]

        self.demon = random.choice(best_moves)


    def compute_visible_cells(self):
        hx, hy = self.hero
        self.visible_cells = set()
        for x in range(hx-VISION, hx+VISION+1):
            for y in range(hy-VISION, hy+VISION+1):
                if 0 <= x < self.N and 0 <= y < self.N:
                    if line_of_sight(self, (hx, hy), (x, y)):
                        self.visible_cells.add((x, y))


class WorldView:
    def __init__(self, world: World, sense_range):
        self.N = world.N
        self.hero = world.hero
        self.has_sword = world.has_sword
        self.move_count = world.move_count
        self.moves_left = MOVES_LIMIT - world.move_count

        self.walls = {w for w in world.walls if w in world.visible_cells}
        self.demon = world.demon if world.demon in world.visible_cells else None
        self.sword = world.sword if world.sword in world.visible_cells else None
        self.hear_demon = manhattan(world.hero, world.demon) <= sense_range

    def __str__(self):
        return f"Demon: {self.demon}, Walls: {self.walls}"


def line_of_sight(world, start, end):
    x0, y0 = start
    x1, y1 = end
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    if dx > dy:
        err = dx / 2.0
        while x != x1:
            if (x, y) in world.walls and (x, y) != start and (x, y) != end:
                return False
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y1:
            if (x, y) in world.walls and (x, y) != start and (x, y) != end:
                return False
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    return True

def draw(world: World):
    screen.fill(BG)
    hx, hy = world.hero
    visible_cells = set()
    for x in range(hx-VISION, hx+VISION+1):
        for y in range(hy-VISION, hy+VISION+1):
            if 0 <= x < N and 0 <= y < N:
                if line_of_sight(world, (hx, hy), (x, y)):
                    visible_cells.add((x, y))

    for x in range(N):
        for y in range(N):
            rect = pygame.Rect(MAP_OFFSET_X + x*CELL, y*CELL, CELL, CELL)
            if (x, y) in visible_cells:
                screen.blit(images['floor'], (MAP_OFFSET_X + x*CELL, y*CELL))
            else:
                pygame.draw.rect(screen, FOG, rect)

    for w in world.walls:
        if w in visible_cells:
            screen.blit(images['wall'], (MAP_OFFSET_X + w[0]*CELL, w[1]*CELL))

    if not world.has_sword and world.sword in visible_cells:
        sx, sy = world.sword
        screen.blit(images['sword'],(MAP_OFFSET_X + sx*CELL, sy*CELL))


    screen.blit(images['hero'],(MAP_OFFSET_X + hx*CELL, hy*CELL))

    dx, dy = world.demon
    if (dx, dy) in visible_cells:
        screen.blit(images['demon'],(MAP_OFFSET_X + dx*CELL, dy*CELL))

    if manhattan(world.hero, world.demon) <= 3:
        screen.blit(images['ear'], (4, 8))

    t = font.render(f"Move: {world.move_count}/{MOVES_LIMIT}", True, TEXT)
    pygame.draw.rect(screen, (50, 50, 80), (WIDTH-130, 0, 130, 28), border_radius=6)
    screen.blit(t, (WIDTH-125, 5))


    if world.has_sword:
        padding = 8
        icon_size = CELL 

        sword_icon = pygame.transform.scale(images['sword'],(int(icon_size), int(icon_size)))

        screen.blit(sword_icon, (padding, 60 + padding))
    
    pygame.display.flip()

def main():
    world = World()
    agent = Agent()

    while True:
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not world.done:
            world.compute_visible_cells()
            world.hero = agent.decide(WorldView(world, SENSE_RANGE))
            world.move_count += 1

            world.move_demon()

            if world.hero == world.sword:
                world.has_sword = True

            if manhattan(world.hero, world.demon) <= 1:
                world.done = True
                world.win = world.has_sword

            if world.move_count >= MOVES_LIMIT:
                world.done = True
                world.win = False

        draw(world)

        if world.done:
            msg = "You Win!" if world.win else "You Lose!"
            draw_popup(pygame, screen, HEIGHT, WIDTH, world, MOVES_LIMIT, msg, images)
            return

if __name__ == "__main__":
    main()