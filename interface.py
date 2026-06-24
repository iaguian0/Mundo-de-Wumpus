import pygame
import sys

from ambiente import AmbienteWumpus
from agente import AgenteBaseadoConhecimento
from sprites import SpriteManager


# ==========================================
# CONFIGURAÇÕES
# ==========================================

GRID_SIZE = 6
CELL_SIZE = 120

PANEL_WIDTH = 360

WIDTH = GRID_SIZE * CELL_SIZE + PANEL_WIDTH
HEIGHT = GRID_SIZE * CELL_SIZE

FPS = 60


# ==========================================
# AMBIENTE E AGENTE
# ==========================================

world = AmbienteWumpus(tamanho=GRID_SIZE)

agente = AgenteBaseadoConhecimento(
    tamanho=GRID_SIZE,
    env=world
)


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

YELLOW = (255, 215, 0)

ALPHA = 80


# ==========================================
# DESENHAR MUNDO
# ==========================================

def draw_world():

    fatos_agente = agente.kb.fatos

    for row in range(GRID_SIZE):

        for col in range(GRID_SIZE):

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            rect = pygame.Rect(
                x,
                y,
                CELL_SIZE,
                CELL_SIZE
            )


            # ==========================================
            # ADICIONADO: RENDERIZAR CHÃO PRIMEIRO
            # ==========================================
            sprite_chao = sprites.chao.copy()
            
            # Se o agente não sabe se a célula é segura, o chão fica escurecido
            if f'Segura({row},{col})' not in fatos_agente:
                sprite_chao.set_alpha(ALPHA)
                
            screen.blit(sprite_chao, (x, y))


            # GRADE (BORDAS)

            if f'Segura({row},{col})' in fatos_agente:

                pygame.draw.rect(
                    screen,
                    WHITE,
                    rect,
                    2
                )

            else:

                pygame.draw.rect(
                    screen,
                    GRAY,
                    rect,
                    2
                )


            # CONTEÚDO DA CÉLULA

            cell = world.grade[row][col]


            # POÇO

            if 'Poco' in cell:

                sprite = sprites.poco.copy()

                if f'Poco({row},{col})' not in fatos_agente:

                    sprite.set_alpha(ALPHA)

                screen.blit(
                    sprite,
                    (
                        x,
                        y
                    )
                )


            # WUMPUS

            elif 'Wumpus' in cell:

                sprite = sprites.wumpus.copy()

                if f'Wumpus({row},{col})' not in fatos_agente:

                    sprite.set_alpha(ALPHA)

                screen.blit(
                    sprite,
                    (
                        x,
                        y
                    )
                )


            # OURO (sprite)

            elif 'Ouro' in cell:

                sprite = sprites.ouro.copy()

                if f'Ouro({row},{col})' not in fatos_agente:

                    sprite.set_alpha(ALPHA)

                screen.blit(
                    sprite,
                    (
                        x,
                        y
                    )
                )


# ==========================================
# DESENHAR AGENTE
# ==========================================

def draw_agent():

    row, col = agente.pos_atual

    x = col * CELL_SIZE
    y = row * CELL_SIZE

    screen.blit(
        sprites.jogador,
        (
            x,
            y
        )
    )


# ==========================================
# PAINEL LATERAL
# ==========================================

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

    title = font.render(
        "Status",
        True,
        WHITE
    )

    screen.blit(
        title,
        (
            panel_x + 20,
            20
        )
    )

    agent_row, agent_col = agente.pos_atual

    steps = agente.passo

    notificacoes = agente.get_notificacoes(3)

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

    continuar = agente.caminhar()


# ==========================================
# EVENTO AUTOMÁTICO
# ==========================================

MOVE_EVENT = pygame.USEREVENT + 1

pygame.time.set_timer(
    MOVE_EVENT,
    400
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