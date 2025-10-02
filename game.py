import pgzrun
from platformer import *

#platformer constants
TILE_SIZE = 64
ROWS = 30
COLS = 20

#pygame constants
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "jogo de plataforma"

#build lvl
platforms = build("platformer_platforms.csv", TILE_SIZE)

def draw():
    screen.clear()
    screen.fill("skyblue")
    #draw platforms
    for platform in platforms:
        platform.draw()

def update():
    pass

pgzrun.go()