import pygame


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
            4
        )


        # Jogador
        self.jogador = self.get_sprite(
            self.animals,
            8,
            6
        )


        # Wumpus
        self.wumpus = self.get_sprite(
            self.animals,
            0,
            3
        )


        # Poço
        self.poco = self.get_sprite(
            self.tiles,
            14,
            16
        )


        # Ouro
        self.ouro = self.get_sprite(
            self.items,
            0,
            25
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