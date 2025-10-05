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

#variáveis de estado
game_state = 'menu'
som_ligado = True

#botões menu
botao_iniciar = Rect((WIDTH/2 - 120, HEIGHT/2 - 20), (240, 50))
botao_som = Rect((WIDTH/2 - 120, HEIGHT/2 + 40), (240, 50))
botao_sair = Rect((WIDTH/2 - 120, HEIGHT/2 + 100), (240, 50))
botao_reiniciar = Rect((WIDTH/2 - 120, HEIGHT/2 + 40), (240, 50))

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
jump_velocity = -12
platforms = []
decos = []
coins = []
obstacles = []

def reset_jogo():
    global platforms, decos, coins, obstacles

    #carrega o nível a partir dos arquivos
    platforms = build("platformer_platforms.csv", TILE_SIZE)
    decos = build("platformer_decos.csv", TILE_SIZE)
    coins = build("platformer_coins.csv", TILE_SIZE)
    obstacles = build("platformer_obstacles.csv", TILE_SIZE)

    #reseta o estado e a posição do player
    player.bottomleft = (0, HEIGHT - TILE_SIZE)
    player.velocity_y = 0
    player.jumping = False
    player.alive = True
    player.image = "p_right"

def draw():
    screen.clear()
    
    if game_state == 'menu':
        draw_menu()
    elif game_state == 'playing':
        draw_jogo()
    elif game_state == 'game_over':
        draw_game_over()
    elif game_state == 'win':
        draw_win()

def draw_menu():
    screen.fill("skyblue")
    screen.draw.text("jogo de plataforma", center=(WIDTH/2, HEIGHT/3), fontsize=45, color="black")
    
    # Desenhar botão Iniciar
    screen.draw.filled_rect(botao_iniciar, "green")
    screen.draw.text("Começar o Jogo", center=botao_iniciar.center, fontsize=30, color="white")
    
    # Desenhar botão Som
    texto_som = f"Som: {'LIGADO' if som_ligado else 'DESLIGADO'}"
    cor_som = "orange" if som_ligado else "gray"
    screen.draw.filled_rect(botao_som, cor_som)
    screen.draw.text(texto_som, center=botao_som.center, fontsize=30, color="white")

    # Desenhar botão Sair
    screen.draw.filled_rect(botao_sair, "red")
    screen.draw.text("Sair", center=botao_sair.center, fontsize=30, color="white")

def draw_jogo():
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
def draw_game_over():
    screen.fill((80, 0, 0))
    screen.draw.text("Game Over!", center=(WIDTH / 2, HEIGHT / 2 - 40), fontsize=60, color="white")
    # Botão para jogar novamente
    screen.draw.filled_rect(botao_reiniciar, "green")
    screen.draw.text("Jogar Novamente", center=botao_reiniciar.center, fontsize=30, color="white")

def draw_win():
    screen.fill((0, 80, 0))
    screen.draw.text("Você Venceu!", center=(WIDTH / 2, HEIGHT / 2 - 40), fontsize=60, color="yellow")
    
    # Botão para jogar novamente
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
            game_state = 'game_over'
    
        #coins collision
        for coin in coins:
            if player.colliderect(coin):
                coins.remove(coin)
                if som_ligado:
                    try:
                        # Ajusta o volume e toca o som no mesmo instante
                        sounds.collect_coin.set_volume(0.2)
                        sounds.collect_coin.play()
                    except Exception as e:
                        # Se falhar, avisa no terminal mas não fecha o jogo
                        print(f"Não foi possível tocar o som da moeda: {e}")
        if len(coins) == 0:
            game_state = 'win'

def on_key_down(key):
    if game_state == 'playing':
        if key == keys.UP and not player.jumping:
            player.velocity_y = jump_velocity
            player.jumping = True

def on_mouse_down(pos):
    global game_state, som_ligado

    if game_state == 'menu':
        if botao_iniciar.collidepoint(pos):
            reset_jogo()
            game_state = 'playing'
        elif botao_som.collidepoint(pos):
            som_ligado = not som_ligado
        elif botao_sair.collidepoint(pos):
            sys.exit()
            
    elif game_state == 'game_over' or game_state == 'win':
        if botao_reiniciar.collidepoint(pos):
            reset_jogo()
            game_state = 'playing'

pgzrun.go()