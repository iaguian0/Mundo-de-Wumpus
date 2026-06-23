from typing import List, Tuple, Set

class BaseConhecimento:
    """
    Base de Conhecimento que armazena sentencas da Logica Proposicional.
    Implementa um mecanismo de inferencia dedutiva (Forward Chaining) baseado em
    regras e fatos atomicos para mapear areas seguras e perigos.
    """
    def __init__(self, tamanho: int):
        self.tamanho = tamanho
        self.fatos: Set[str] = set()       # Fatos verdadeiros confirmados
        self.visitados: Set[Tuple[int, int]] = set()

    def _obter_vizinhos(self, r: int, c: int) -> List[Tuple[int, int]]:
        vizinhos = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.tamanho and 0 <= nc < self.tamanho:
                vizinhos.append((nr, nc))
        return vizinhos

    def tell(self, fato: str):
        """Adiciona uma sentenca atomica ou fato a base de conhecimento."""
        self.fatos.add(fato)

    def tell_visitado(self, r: int, c: int):
        """Registra que uma celula foi visitada e e logicamente segura."""
        self.visitados.add((r, c))
        self.tell(f"Segura({r},{c})")
        self.tell(f"~Poco({r},{c})")
        self.tell(f"~Wumpus({r},{c})")

    def inferir_conhecimento(self):
        """
        Mecanismo de Inferencia Dedutiva. Realiza iteracoes sobre as celulas para
        descobrir novas certezas logicas com base nas regras do Mundo de Wumpus.
        """
        mudancas = True
        while mudancas:
            total_antes = len(self.fatos)
            
            for r in range(self.tamanho):
                for c in range(self.tamanho):
                    vizinhos = self._obter_vizinhos(r, c)
                    
                    # 1. Sem brisa = vizinhos sem poco
                    if f"Visitada({r},{c})" in self.fatos and f"Brisa({r},{c})" not in self.fatos:
                        for nr, nc in vizinhos:
                            self.tell(f"~Poco({nr},{nc})")
                            
                    # 2. Sem fedor = vizinhos sem wumpus
                    if f"Visitada({r},{c})" in self.fatos and f"Fedor({r},{c})" not in self.fatos:
                        for nr, nc in vizinhos:
                            self.tell(f"~Wumpus({nr},{nc})")

                    # 3. Brisa e apenas um vizinho desconhecido = poco detectado
                    if f"Brisa({r},{c})" in self.fatos:
                        pocos_desconhecidos = [n for n in vizinhos if f"~Poco({n[0]},{n[1]})" not in self.fatos]
                        if len(pocos_desconhecidos) == 1:
                            pr, pc = pocos_desconhecidos[0]
                            self.tell(f"Poco({pr},{pc})")

                    # 4. Fedor e apenas um vizinho desconhecido = wumpus detectado
                    if f"Fedor({r},{c})" in self.fatos:
                        wumpus_desconhecidos = [n for n in vizinhos if f"~Wumpus({n[0]},{n[1]})" not in self.fatos]
                        if len(wumpus_desconhecidos) == 1:
                            wr, wc = wumpus_desconhecidos[0]
                            self.tell(f"Wumpus({wr},{wc})")

                    # 5. Livre de perigos = celula segura
                    if f"~Poco({r},{c})" in self.fatos and f"~Wumpus({r},{c})" in self.fatos:
                        self.tell(f"Segura({r},{c})")
                        
            if len(self.fatos) == total_antes:
                mudancas = False

    def eh_segura(self, r: int, c: int) -> bool:
        return f"Segura({r},{c})" in self.fatos

    def eh_suspeita_poco(self, r: int, c: int) -> bool:
        return f"~Poco({r},{c})" not in self.fatos

    def eh_suspeita_wumpus(self, r: int, c: int) -> bool:
        return f"~Wumpus({r},{c})" not in self.fatos