import pgzrun
from platformer import *

#platformer constants
TILE_SIZE = 18
ROWS = 30
COLS = 20

#pygame constants
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "jogo de plataforma"

#build lvl
platforms = build("platformer_platforms.csv", TILE_SIZE)
decos = build("platformer_decos.csv", TILE_SIZE)
coins = build("platformer_coins.csv", TILE_SIZE)
obstacles = build("platformer_obstacles.csv", TILE_SIZE)

#def player actor
player = Actor("p_right")
player.bottomleft = (0, HEIGHT - TILE_SIZE)
#actor variables
player.velocity_x = 2
player.velocity_y = 0
player.jumping = False
player.alive = True

#def global variables
gravity = 1
jump_velocity = -10
over = False
win = False

def draw():
    screen.clear()
    screen.fill("skyblue")
    #draw platforms
    for platform in platforms:
        platform.draw()
    #draw deco
    for deco in decos:
        deco.draw()
    #draw coins
    for coin in coins:
        coin.draw()
    #draw obstacles
    for obstacle in obstacles:
        obstacle.draw()

    #draw player
    if player.alive:
        player.draw()

    #display messages
    if over:
        screen.draw.text("Game Over!", center=(WIDTH / 2, HEIGHT / 2) )
    if win:
        screen.draw.text("You Win!", center=(WIDTH / 2, HEIGHT / 2) )

def update():
    global over, win
    #left movement
    if keyboard.LEFT and player.midleft[0] > 0:
        player.x -= player.velocity_x
        player.image = "p_left"
        if player.collidelist(platforms) != -1:
            object = platforms[player.collidelist(platforms)]
            player.x = object.x + (object.width / 2 + player.width / 2)
    #right movement
    elif keyboard.RIGHT and player.midright[0] < WIDTH:
        player.x += player.velocity_x
        player.image = "p_right"
        if player.collidelist(platforms) != -1:
            object = platforms[player.collidelist(platforms)]
            player.x = object.x - (object.width / 2 + player.width / 2)
    #gravity
    player.y += player.velocity_y
    player.velocity_y += gravity
    if player.collidelist(platforms) != -1:
        object = platforms[player.collidelist(platforms)]

        if player.velocity_y >=0:
            player.y = object.y - (object.height / 2 + player.height / 2)
            player.jumping = False
        else:
            player.y = object.y + (object.height / 2 + player.height / 2)

        player.velocity_y = 0

    if player.collidelist(obstacles) != -1:
        player.alive = False
        over = True
    
    #coins collision
    for coin in coins:
        if player.colliderect(coin):
            coins.remove(coin)
    if len(coins) == 0:
        win = True


def on_key_down(key):
    if key == keys.UP and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True


pgzrun.go()