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
inicios = cenario.inicios

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

small_font = pygame.font.SysFont(None, 22)
font_name = pygame.font.SysFont(None, int(CELL_SIZE*0.22))
font_name.set_underline(True)
font_name.set_bold(True)


# ==========================================
# CORES
# ==========================================

BLACK = (20, 20, 20)

WHITE = (255, 255, 255)

GRAY = (50, 50, 50)

RED = (200, 50, 50)
BLUE = (50, 100, 255)
GREEN = (0, 180, 0)
YELLOW = (255, 215, 0)

ALPHA = 80

cores_times = [
    RED, 
    BLUE,
    GREEN, 
    YELLOW, 
    ]

passos = 0

def draw_world():
        TM_POINT = CELL_SIZE/8
        achou_ouro = False
        for agts in times:
            for agt in agts:
                if agt.tem_ouro:
                    achou_ouro = True


        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):

                x = col * CELL_SIZE
                y = row * CELL_SIZE


                rect = pygame.Rect(x, y, CELL_SIZE,CELL_SIZE)
                
                sprite_chao = sprites.chao.copy()
                pygame.draw.rect(screen, GRAY, rect, 2)
                
                screen.blit(sprite_chao, (x, y))

                for i, agentes in enumerate(times):
                    conhecimento = agentes[0].kb
                    fatos_agente = conhecimento.fatos
                    
                    if conhecimento.eh_segura(row, col):
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
                        if achou_ouro:
                            sprite = sprites.ouro_achado.copy()
                        else:
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
            sprite = sprites.jogadores[t].copy()
            
            if not agente.esta_vivo:
                sprite.set_alpha(ALPHA)

            screen.blit(
                sprite,
                (
                    x,
                    y
                )
            )
            nome_ag = agente.name.upper()

            if N_TIMES > 1:
                name = font_name.render(nome_ag, True, cores_times[t])
            else:
                name = font_name.render(nome_ag, True, WHITE)
            
            l_t, a_t = font_name.size(nome_ag)
            
            x_nome = x + (CELL_SIZE - l_t)//2

            pos = (x_nome, y)
            
               
            if agente.tem_ouro:
                screen.blit(
                    sprites.bolsa_ouro,
                    (
                        x+(CELL_SIZE/2),
                        y
                    )
                )

            pygame.draw.rect(screen, BLACK, (*pos, l_t, a_t))
            screen.blit(name, pos)

            

             

def draw_inicios():
    for inicio in inicios:
        y, x = inicio
        x = x * CELL_SIZE
        y = y * CELL_SIZE
        sprite = sprites.saida.copy()
        sprite.set_alpha(180)
        screen.blit(
            sprite,
            (
                x,
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

    ganhador = ''

    if not continuar:
        pontos = []
        for t, agentes in enumerate(times):
            pontos.append((t, sum([ag.get_pontuacao() for ag in agentes])))

        pontos.sort(key=lambda x: x[1], reverse=True)
        ganhador = f'Ganhador: Time {pontos[0][0]+1}'

    info = [
        str(ganhador) if ganhador else "",
        f"Passos: {passos}",
        "",
    ]

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

    pont_times = []
    for t, agentes in enumerate(times):
        pontuacao_time = sum([ag.get_pontuacao() for ag in agentes])
        pont_times.append((t, (f'Time {t+1}: {pontuacao_time}')))
        notificacoes = []
        for agente in agentes:
            notificacoes.extend(agente.get_notificacoes(1))
        pont_times.extend([(t, n) for n in notificacoes ])
        pont_times.append('')



    for pont in pont_times:
        y += 18
        if not pont: continue

        t, line = pont
        text = small_font.render(
            line,
            True,
            cores_times[t]
        )

        screen.blit(
            text,
            (
                panel_x + 20,
                y
            )
        )




# ==========================================
# MOVIMENTO DO AGENTE
# ==========================================

def move_agent():

    global continuar
    global passos
    passos += 1

    times_win = []
    for agentes in times:
        for agente in agentes:
            agente.caminhar()
            times_win.append(not agente.ativo())

    if all(times_win):
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
    
    draw_inicios()

    draw_agent()


    draw_panel()

    pygame.display.flip()

pygame.quit()

sys.exit()