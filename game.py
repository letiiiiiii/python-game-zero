import pgzrun
import sys
from platformer import *

TILE_SIZE = 18
ROWS = 30
COLS = 20

WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "jogo de plataforma"

#animações
color_key = (0, 0, 0)
fox_stand_sprite = Sprite("fox.png", (0, 32 + 8, 32, 24), 14, color_key, 30)
fox_walk_sprite = Sprite("fox.png", (0, 64 + 8, 32, 24), 8, color_key, 5)

ANIMATION_STAND_FRAMES = fox_stand_sprite.images
ANIMATION_WALK_FRAMES = fox_walk_sprite.images
ANIMATION_SPEED = 5 

#variáveis de estado
game_state = 'menu'
som_ligado = True

#botões menu
botao_iniciar = Rect((WIDTH/2 - 120, HEIGHT/2 - 20), (240, 50))
botao_som = Rect((WIDTH/2 - 120, HEIGHT/2 + 40), (240, 50))
botao_sair = Rect((WIDTH/2 - 120, HEIGHT/2 + 100), (240, 50))
botao_reiniciar = Rect((WIDTH/2 - 120, HEIGHT/2 + 40), (240, 50))

player = Actor('p_right')
player.anchor = ('center', 'bottom')

#controle de animação e direção
player.current_animation = ANIMATION_STAND_FRAMES
player.frame_index = 0
player.animation_timer = 0
player.direction = 'right'

player.bottomleft = (0, HEIGHT - TILE_SIZE)

#actor var
player.velocity_x = 2
player.velocity_y = 0
player.jumping = False
player.alive = True

#def global var
gravity = 1
jump_velocity = -12
platforms = []
decos = []
coins = []
obstacles = []

def reset_jogo():
    global platforms, decos, coins, obstacles

    platforms = build("platformer_platforms.csv", TILE_SIZE)
    decos = build("platformer_decos.csv", TILE_SIZE)
    coins = build("platformer_coins.csv", TILE_SIZE)
    obstacles = build("platformer_obstacles.csv", TILE_SIZE)

    player.bottomleft = (0, HEIGHT - TILE_SIZE)
    player.velocity_y = 0
    player.jumping = False
    player.alive = True
    
    player.current_animation = ANIMATION_STAND_FRAMES
    player.frame_index = 0
    player.animation_timer = 0
    player.direction = 'right'

def draw():
    screen.clear()
    if game_state == 'menu': draw_menu()
    elif game_state == 'playing': draw_jogo()
    elif game_state == 'game_over': draw_game_over()
    elif game_state == 'win': draw_win()

def draw_menu():
    screen.fill("skyblue")
    screen.draw.text("jogo de plataforma", center=(WIDTH/2, HEIGHT/3), fontsize=45, color="black")
    screen.draw.filled_rect(botao_iniciar, "green")
    screen.draw.text("Começar o Jogo", center=botao_iniciar.center, fontsize=30, color="white")
    texto_som = f"Som: {'LIGADO' if som_ligado else 'DESLIGADO'}"
    cor_som = "orange" if som_ligado else "gray"
    screen.draw.filled_rect(botao_som, cor_som)
    screen.draw.text(texto_som, center=botao_som.center, fontsize=30, color="white")
    screen.draw.filled_rect(botao_sair, "red")
    screen.draw.text("Sair", center=botao_sair.center, fontsize=30, color="white")

def draw_jogo():
    screen.fill("skyblue")
    for platform in platforms: platform.draw()
    for deco in decos: deco.draw()
    for coin in coins: coin.draw()
    for obstacle in obstacles: obstacle.draw()
    if player.alive: player.draw()

def draw_game_over():
    screen.fill((80, 0, 0))
    screen.draw.text("Game Over!", center=(WIDTH / 2, HEIGHT / 2 - 40), fontsize=60, color="white")
    screen.draw.filled_rect(botao_reiniciar, "green")
    screen.draw.text("Jogar Novamente", center=botao_reiniciar.center, fontsize=30, color="white")

def draw_win():
    screen.fill((0, 80, 0))
    screen.draw.text("Você Venceu!", center=(WIDTH / 2, HEIGHT / 2 - 40), fontsize=60, color="yellow")
    screen.draw.filled_rect(botao_reiniciar, "green")
    screen.draw.text("Jogar Novamente", center=botao_reiniciar.center, fontsize=30, color="white")

def update():
    global game_state

    if game_state == 'playing' and som_ligado:
        if not music.is_playing('background'):
            music.play('background')
            music.set_volume(0.1)
    else:
        music.stop()

    if game_state == 'playing':

        #flip
        player.animation_timer += 1
        if player.animation_timer >= ANIMATION_SPEED:
            player.animation_timer = 0
            player.frame_index += 1
            if player.frame_index >= len(player.current_animation):
                player.frame_index = 0
        
        original_image = player.current_animation[player.frame_index]

        if player.direction == 'left':
            final_image = pygame.transform.flip(original_image, True, False)
        else:
            final_image = original_image
        
        player._surf = final_image
        player.width = player._surf.get_width()
        player.height = player._surf.get_height()

        #movimentação
        is_moving = False
        if keyboard.LEFT and player.left > 0:
            player.x -= player.velocity_x
            player.direction = 'left'
            if player.collidelist(platforms) != -1: player.left = platforms[player.collidelist(platforms)].right
            is_moving = True
        elif keyboard.RIGHT and player.right < WIDTH:
            player.x += player.velocity_x
            player.direction = 'right' 
            if player.collidelist(platforms) != -1: player.right = platforms[player.collidelist(platforms)].left
            is_moving = True
        
        if is_moving:
            if player.current_animation is not ANIMATION_WALK_FRAMES:
                player.current_animation = ANIMATION_WALK_FRAMES
                player.frame_index = 0
        else:
            if player.current_animation is not ANIMATION_STAND_FRAMES:
                player.current_animation = ANIMATION_STAND_FRAMES
                player.frame_index = 0
        
        player.y += player.velocity_y; player.velocity_y += gravity
        if player.collidelist(platforms) != -1:
            object = platforms[player.collidelist(platforms)]
            if player.velocity_y >= 0: player.bottom = object.top; player.jumping = False
            else: player.top = object.bottom
            player.velocity_y = 0
        
        if player.alive:
            if player.collidelist(obstacles) != -1:
                player.alive = False; 
                game_state = 'game_over'
        
            for coin in coins:
                if player.colliderect(coin):
                    coins.remove(coin)
                    if som_ligado:
                        try:
                            sounds.collect_coin.set_volume(0.2)
                            sounds.collect_coin.play()
                        except Exception as e:
                            print(f"Não foi possível tocar o som da moeda: {e}")
            if len(coins) == 0:
                game_state = 'win'

def on_key_down(key):
    if game_state == 'playing' and key == keys.UP and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True

def on_mouse_down(pos):
    global game_state, som_ligado
    if game_state == 'menu':
        if botao_iniciar.collidepoint(pos): reset_jogo(); game_state = 'playing'
        elif botao_som.collidepoint(pos): som_ligado = not som_ligado
        elif botao_sair.collidepoint(pos): sys.exit()
    elif game_state == 'game_over' or game_state == 'win':
        if botao_reiniciar.collidepoint(pos): reset_jogo(); game_state = 'playing'

pgzrun.go()