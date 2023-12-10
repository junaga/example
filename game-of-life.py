VERSION = "v0.1"

from shutil import get_terminal_size
from os import environ as env
from sys import argv
from random import random
from time import sleep

COLUMNS = env.get("COLUMNS")
ROWS = env.get("ROWS")
LINES = env.get("LINES")

TPS = 1
RANDOM_CELLS = 0
HELP = """
conways game of life cli

usage:
  game [OPTIONS] [COORDINATE ...]

COORDINATE          alive cells in the format X/Y

options:
  --speed   SPEED   simulation speed. default: 1
  --random  PCT     percentage of random alive cells

examples:
  game 1/0 1/1 1/2
  game --speed 100 --random 20
"""

CONSOLE = -1, 0


def rules(game, x, y):
    world, (len_x, len_y) = game

    neighbors = 0
    neighborhood = [
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, 1),
        # (0, 0)
        (0, -1),
        (1, 1),
        (1, 0),
        (1, -1),
    ]
    for move_x, move_y in neighborhood:
        x1 = x + move_x
        y1 = y + move_y
        in_world = -1 < x1 < len_x and -1 < y1 < len_y
        if in_world:
            alive = world[x1][y1] == True
            if alive:
                neighbors += 1

    alive = world[x][y] == True
    under_populated = neighbors <= 1
    # balanced = neighbors == 2
    flourishing = neighbors == 3
    over_populated = neighbors >= 4
    death = alive and (under_populated or over_populated)
    birth = not alive and flourishing
    if birth:
        alive = True
    if death:
        alive = False
    return alive


def tick(game):
    _world, (len_x, len_y) = game

    world = []
    for x in range(len_x):
        chunk = []
        for y in range(len_y):
            cell = rules(game, x, y)
            chunk.append(cell)
        world.append(chunk)
    return world, (len_x, len_y)


def render(game, time):
    world, (len_x, len_y) = game

    life = "■"  # BLACK SQUARE
    not_life = " "  # SPACE
    frame = "\n"
    for y in range(len_y):
        for x in range(len_x):
            cell = world[x][y]
            alive = cell is True
            if alive:
                frame += life
            else:
                frame += not_life
        frame += "\n"
    frame += f"time: {time}"  # CONSOLE + 1

    print(frame, end="", flush=True)


def term_dims():
    """
    get terminal dimensions, terminal viewport height and width, in rows and columns
    """

    if ROWS:
        rows = int(ROWS)
    elif LINES:
        rows = int(LINES)
    else:
        rows = get_terminal_size().lines

    if COLUMNS:
        cols = int(COLUMNS)
    else:
        cols = get_terminal_size().columns

    return rows, cols


def init(cells, random_cells):
    rows, cols = term_dims()
    _rows, _cols = CONSOLE
    rows += _rows
    cols += _cols

    world = []
    for x in range(cols):
        chunk = []
        for y in range(rows):
            cell = False
            alive = (x, y) in cells or (random() * 100) < random_cells
            if alive:
                cell = True
            chunk.append(cell)
        world.append(chunk)
    return (world, (cols, rows))


def main(cells, random_cells, tps):
    game = init(cells, random_cells)

    time = 1
    while True:  # CTRL+C to cancel
        render(game, time)
        sleep(1 / tps)
        game = tick(game)
        time += 1


if __name__ == "__main__":
    [_bin, *args] = argv

    i = 0
    cells = []
    random_cells = RANDOM_CELLS
    tps = TPS
    exit = False
    while i < len(args):
        if args[i] == "--help":
            print(HELP)
            exit == True
            break
        elif args[i] == "--version":
            print(VERSION)
            exit == True
            break
        elif args[i] == "--speed":
            i += 1
            tps = int(args[i])
        elif args[i] == "--random":
            i += 1
            random_cells = int(args[i])
        else:
            x, y = args[i].split("/")
            x, y = int(x), int(y)
            cells.append((x, y))
        i += 1

    if not exit:
        main(cells, random_cells, tps)
