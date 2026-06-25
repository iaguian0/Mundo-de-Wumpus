import pygame
import random

SPRITE_SIZE = 32


class SpriteManager:

    def __init__(self, cell_size):

        self.cell_size = cell_size


        # Carrega spritesheets
        self.tiles = pygame.image.load(
            "assets/tiles.png"
        ).convert_alpha()


        self.monsters = pygame.image.load(
            "assets/monsters.png"
        ).convert_alpha()


        self.rogues = pygame.image.load(
            "assets/rogues.png"
        ).convert_alpha()


        self.items = pygame.image.load(
            "assets/items.png"
        ).convert_alpha()

        self.animals = pygame.image.load(
            "assets/animals.png"
        ).convert_alpha()

        # ==========================
        # SPRITES DO JOGO
        # ==========================


        # Chão
        self.chao = self.get_sprite(
            self.tiles,
            0,
            0
        )
        self.jogadores = []
        # Jogador
        self.jogador = self.get_sprite(
            self.rogues,
            0,0,)

        monstros_list = [
            (1, 1),
            (2, 2),
            (1, 2),
            (1, 7),
            (0, 4),
            (4, 5),
            (9, 7),
            (2, 8),
            (2, 12),
        ]

        monstro_cord = random.choice(monstros_list)

        # Wumpus
        self.wumpus = self.get_sprite(
            self.monsters,
            *monstro_cord,
        )


        # Poço
        self.poco = self.get_sprite(
            self.tiles,
            11,
            16
        )


        # Ouro
        self.ouro = self.get_sprite(
            self.tiles,
            0,
            17
        )


        # Ouro
        self.ouro_achado = self.get_sprite(
            self.tiles,
            1,
            17
        )


        bolsa_list = [
            (3, 24), #bolsa
            (3, 21), #livro
            (1, 17), #anel 
            (0, 22), #chave
            (10, 0), #espada fogo
            (6, 10), #cajado fogo
            (3, 6), #trident
            (2, 12), #manto
            (5, 11), #escudo
            (2, 16), #colar 
        ]

        bolsa_cord = random.choice(bolsa_list)


        self.bolsa_ouro = self.get_sprite(
            self.items,
            *bolsa_cord
        )

        self.saida = self.get_sprite(
            self.tiles,
            3, 
            16
        )




    def get_sprite(self, sheet, coluna, linha):

        sprite = pygame.Surface(
            (
                SPRITE_SIZE,
                SPRITE_SIZE
            ),
            pygame.SRCALPHA
        )


        sprite.blit(
            sheet,
            (
                0,
                0
            ),
            (
                coluna * SPRITE_SIZE,
                linha * SPRITE_SIZE,
                SPRITE_SIZE,
                SPRITE_SIZE
            )
        )


        sprite = pygame.transform.scale(
            sprite,
            (
                self.cell_size,
                self.cell_size
            )
        )


        return sprite