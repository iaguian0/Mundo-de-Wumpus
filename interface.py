import pygame
import sys

from ambiente import AmbienteWumpus
from agente import AgenteBaseadoConhecimento


# ==========================================
# CONFIGURAÇÕES
# ==========================================

GRID_SIZE = 5
CELL_SIZE = 120

PANEL_WIDTH = 360

WIDTH = GRID_SIZE * CELL_SIZE + PANEL_WIDTH
HEIGHT = GRID_SIZE * CELL_SIZE

FPS = 60

world = AmbienteWumpus(tamanho=GRID_SIZE)
agente = AgenteBaseadoConhecimento(tamanho=GRID_SIZE, env=world)


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mundo de Wumpus")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 28)

BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
GRAY = (60, 60, 60)

GREEN = (0, 180, 0)
RED = (200, 50, 50)
YELLOW = (255, 215, 0)
BLUE = (50, 100, 255)

ALPHA = 80

def draw_world():

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

            fatos_agente = agente.kb.fatos

            if f'Segura({row},{col})' in fatos_agente:
                pygame.draw.rect(screen, WHITE, rect, 2)
            else:
                pygame.draw.rect(screen, GRAY, rect, 2)


            cell = world.grade[row][col]

            if 'Poco' in cell:
                text = font.render("P", True, RED)
                if f'Poco({row},{col})' not in fatos_agente: text.set_alpha(ALPHA)


            elif 'Wumpus' in cell:
                text = font.render("W", True, GREEN)
                if f'Wumpus({row},{col})' not in fatos_agente: text.set_alpha(ALPHA)


            elif 'Ouro' in cell:
                text = font.render("O", True, YELLOW)
                if f'Ouro({row},{col})' not in fatos_agente: text.set_alpha(ALPHA)

            else:
                continue

            text_rect = text.get_rect(
                center=(x + CELL_SIZE // 2,
                        y + CELL_SIZE // 2)
            )

            screen.blit(text, text_rect)

def draw_agent():
    y, x = agente.pos_atual
    x = x * CELL_SIZE + CELL_SIZE // 2
    y = y * CELL_SIZE + CELL_SIZE // 2

    pygame.draw.circle(
        screen,
        BLUE,
        (x, y),
        25
    )

    label = small_font.render("A", True, WHITE)

    label_rect = label.get_rect(center=(x, y))

    screen.blit(label, label_rect)

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

    title = font.render("Status", True, WHITE)
    screen.blit(title, (panel_x + 20, 20))
    
    agent_row, agent_col = agente.pos_atual
    steps = agente.passo

    notificacoes = agente.get_notificacoes(3)

    info = [
        f"Passos: {steps}",
        f"Linha: {agent_row} - Coluna: {agent_col}",
        "",
        "Objetivo:",
        "Encontrar ouro",
        "Notificacoes:",
    ]

    info.extend(notificacoes)

    y = 90

    for line in info:

        text = small_font.render(line, True, WHITE)

        screen.blit(
            text,
            (panel_x + 20, y)
        )

        y += 35

def move_agent():
    global continuar
    continuar = agente.caminhar()
    
    if not continuar: 
        return


MOVE_EVENT = pygame.USEREVENT + 1

pygame.time.set_timer(
    MOVE_EVENT,
    400
)

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