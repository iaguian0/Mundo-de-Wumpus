import random
from typing import List, Tuple, Set

class AmbienteWumpus:
    """
    Gera o ambiente de forma automatica e aleatoria contendo os perigos e o ouro.
    Garante que a posicao de partida do agente seja 100% segura.
    """
    def __init__(self, tamanho: int = 4):
        self.tamanho = max(4, tamanho)  # Limite minimo de 4x4 conforme regras
        self.grade: List[List[Set[str]]] = [[set() for _ in range(self.tamanho)] for _ in range(self.tamanho)]
        self.pos_wumpus: List[Tuple[int, int]] = []
        self.pos_pocos: List[Tuple[int, int]] = []
        self.pos_ouro: Tuple[int, int] = (0, 0)
        self.inicio_agente: Tuple[int, int] = (0, 0)
        
        self._gerar_mundo()
        print(self.grade)

    def _obter_vizinhos(self, r: int, c: int) -> List[Tuple[int, int]]:
        vizinhos = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.tamanho and 0 <= nc < self.tamanho:
                vizinhos.append((nr, nc))
        return vizinhos

    def _gerar_mundo(self):
        restricoes_pos = [(self.inicio_agente[0]+i, self.inicio_agente[1]+j) for i in range(-1, 2) for j in range(-1, 2)]
        todas_posicoes = [(r, c) for r in range(self.tamanho) for c in range(self.tamanho) if (r, c) not in restricoes_pos]
        random.shuffle(todas_posicoes)
        
        # Posicionar Ouro
        self.pos_ouro = todas_posicoes.pop()
        self.grade[self.pos_ouro[0]][self.pos_ouro[1]].add("Ouro")
        
        # Posicionar Wumpus (Pelo menos 1)
        posicao_wumpus = todas_posicoes.pop()
        self.pos_wumpus.append(posicao_wumpus)
        self.grade[posicao_wumpus[0]][posicao_wumpus[1]].add("Wumpus")
        for nr, nc in self._obter_vizinhos(posicao_wumpus[0], posicao_wumpus[1]):
            self.grade[nr][nc].add("Fedor")
                
        # Posicionar Pocos dinamicamente por tamanho
        num_pocos = max(1, int((self.tamanho * self.tamanho) * 0.15))
        for _ in range(num_pocos):
            if not todas_posicoes:
                break
            posicao_pit = todas_posicoes.pop()
            self.pos_pocos.append(posicao_pit)
            self.grade[posicao_pit[0]][posicao_pit[1]].add("Poco")
            for nr, nc in self._obter_vizinhos(posicao_pit[0], posicao_pit[1]):
                self.grade[nr][nc].add("Brisa")

        self.grade = [
            [set(), {'Brisa'}, {'Poco'}, {'Ouro', 'Brisa'}], 
            [set(), set(), {'Brisa', 'Fedor'}, {'Brisa'}], 
            [set(), {'Fedor'}, {'Wumpus'}, {'Fedor', 'Poco'}], 
            [set(), set(), {'Fedor'}, {'Brisa'}]
        ]


    def obter_percepcoes(self, r: int, c: int) -> Set[str]:
        percepcoes = set()
        conteudo_celula = self.grade[r][c]
        if "Brisa" in conteudo_celula: percepcoes.add("Brisa")
        if "Fedor" in conteudo_celula: percepcoes.add("Fedor")
        if "Ouro" in conteudo_celula: percepcoes.add("Brilho")
        return percepcoes

    def exibir_ambiente(self, pos_agente: Tuple[int, int]):
        borda = "+" + ("--------+" * self.tamanho)
        print(borda)
        for r in range(self.tamanho):
            linha_str = "|"
            for c in range(self.tamanho):
                elementos_celula = []
                if (r, c) == pos_agente: elementos_celula.append("A")
                if "Wumpus" in self.grade[r][c]: elementos_celula.append("W")
                if "Poco" in self.grade[r][c]: elementos_celula.append("P")
                if "Ouro" in self.grade[r][c]: elementos_celula.append("O")
                
                exibicao = "".join(elementos_celula)
                linha_str += f" {exibicao.center(6)} |"
            print(linha_str)
            print(borda)