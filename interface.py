import pygame
import sys

from sprites import SpriteManager
from inicializacao_cenario import InicializarCenario
from config_parser import *

# ==========================================
# CONFIGURAÇÕES
# ==========================================

PANEL_WIDTH = panel_width

TAMANHO_H_W = tamanho_h_w
GRID_SIZE = grid_size

N_AGENTES_P_TIME = n_agentes_p_time
N_TIMES = n_times

N_AGENTES = N_AGENTES_P_TIME * N_TIMES


WIDTH = TAMANHO_H_W + PANEL_WIDTH
HEIGHT = TAMANHO_H_W 

CELL_SIZE = int(HEIGHT / GRID_SIZE)


FPS = fps


cenario = InicializarCenario(grid_size=GRID_SIZE, n_agentes_time=N_AGENTES_P_TIME, n_times=N_TIMES)

times = cenario.times
world = cenario.world


# ==========================================
# PYGAME
# ==========================================

pygame.init()

screen = pygame.display.set_mode(
    (
        WIDTH,
        HEIGHT
    )
)

pygame.display.set_caption("Mundo de Wumpus")

clock = pygame.time.Clock()

sprites = SpriteManager(CELL_SIZE)


# ==========================================
# FONTES
# ==========================================

font = pygame.font.SysFont(None, 40)

small_font = pygame.font.SysFont(None, 28)


# ==========================================
# CORES
# ==========================================

BLACK = (20, 20, 20)

WHITE = (255, 255, 255)

GRAY = (60, 60, 60)

GREEN = (0, 180, 0)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)
BLUE = (50, 100, 255)

ALPHA = 80

cores_times = [RED, YELLOW, GREEN, BLUE]

def draw_world():
        TM_POINT = CELL_SIZE/8
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):

                x = col * CELL_SIZE
                y = row * CELL_SIZE


                rect = pygame.Rect(x, y, CELL_SIZE,CELL_SIZE)
                
                sprite_chao = sprites.chao.copy()
                pygame.draw.rect(screen, GRAY, rect, 2)
                
                screen.blit(sprite_chao, (x, y))

                for i, agentes in enumerate(times):
                    fatos_agente = agentes[0].kb.fatos
                    
                    if f'Segura({row},{col})' in fatos_agente:
                        
                        pygame.draw.rect(screen, WHITE, rect, 2)
                        pygame.draw.circle(screen, cores_times[i], (x+TM_POINT+((TM_POINT*1.5)*i), y+TM_POINT), int(TM_POINT/2))


                    cell = world.grade[row][col]

                    if 'Poco' in cell:
                        sprite = sprites.poco.copy()

                        if f'Poco({row},{col})' not in fatos_agente:
                            sprite.set_alpha(ALPHA)


                    elif 'Wumpus' in cell:
                        sprite = sprites.wumpus.copy()

                        if f'Wumpus({row},{col})' not in fatos_agente:
                            sprite.set_alpha(ALPHA)

            
                    elif 'Ouro' in cell:
                        sprite = sprites.ouro.copy()

                        if f'Ouro({row},{col})' not in fatos_agente:
                            sprite.set_alpha(ALPHA)


                    else:
                        continue

                    screen.blit(sprite,(x, y))


def draw_agent():
    for t, agentes in enumerate(times):
        for i, agente in enumerate(agentes):

            y, x = agente.pos_atual
            x = x * CELL_SIZE
            y = y * CELL_SIZE
            sprite = sprites.jogador.copy()

            if N_TIMES > 1:
                superficie_cor = pygame.Surface(sprite.get_size()).convert_alpha()
                superficie_cor.fill(cores_times[t])
                
                
                sprite.blit(superficie_cor, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            if not agente.esta_vivo:
                sprite.set_alpha(ALPHA)

            screen.blit(
                sprite,
                (
                    x,
                    y
                )
            )

            if agente.tem_ouro:
                screen.blit(
                    sprites.bolsa_ouro,
                    (
                        x+(CELL_SIZE/2),
                        y
                    )
                )
             



def draw_panel():
    panel_x = GRID_SIZE * CELL_SIZE

    pygame.draw.rect(
        screen,
        GRAY,
        (
            panel_x,
            0,
            PANEL_WIDTH,
            HEIGHT
        )
    )

    agentes = times[0]
    title = font.render("Status", True, WHITE)
    screen.blit(title, (panel_x + 20, 20))
    
    agent_row, agent_col = agentes[0].pos_atual
    steps = agentes[0].passo

    notificacoes = agentes[0].get_notificacoes(3)

    info = [
        f"Passos: {steps}",
        f"Linha: {agent_row}",
        f"Coluna: {agent_col}",
        "",
        "Objetivo:",
        "Encontrar ouro",
        "",
        "Notificacoes:"
    ]

    info.extend(notificacoes)

    y = 90

    for line in info:

        text = small_font.render(
            line,
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                panel_x + 20,
                y
            )
        )

        y += 35


# ==========================================
# MOVIMENTO DO AGENTE
# ==========================================

def move_agent():

    global continuar
    for agentes in times:
        time_win = []
        for agente in agentes:
            time_win.append(not agente.caminhar())

        if all(time_win):
            continuar = False

# ==========================================
# EVENTO AUTOMÁTICO
# ==========================================

MOVE_EVENT = pygame.USEREVENT + 1

pygame.time.set_timer(
    MOVE_EVENT,
    timer_movimento
)


# ==========================================
# LOOP PRINCIPAL
# ==========================================

running = True

continuar = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if event.type == MOVE_EVENT and continuar:

            move_agent()


    screen.fill(BLACK)

    draw_world()

    draw_agent()

    draw_panel()

    pygame.display.flip()

pygame.quit()

sys.exit()