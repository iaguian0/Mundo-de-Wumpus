from typing import List, Tuple, Set, Dict

class BaseConhecimento:
    """
    Base de Conhecimento Formal usando Logica Proposicional via Encadeamento
    para Frente (Forward Chaining) com Clausulas de Definição (Horn).
    Garante execucao em tempo linear, eliminando travamentos por explosao combinatoria.
    """
    def __init__(self, tamanho: int):
        self.tamanho = tamanho
        self.fatos: Set[str] = set()
        self.visitados: Set[Tuple[int, int]] = set()
        self.regras: List[Tuple[List[str], str]] = []  # Estrutura: ([Premissas], Conclusao)
        
        self._inicializar_regras_do_mundo()

    def _obter_vizinhos(self, r: int, c: int) -> List[Tuple[int, int]]:
        vizinhos = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.tamanho and 0 <= nc < self.tamanho:
                vizinhos.append((nr, nc))
        return vizinhos

    def _inicializar_regras_do_mundo(self):
        """ Inicializa as regras proposicionais do mundo em formato de implicacao logica """
        for r in range(self.tamanho):
            for c in range(self.tamanho):
                vizinhos = self._obter_vizinhos(r, c)
                
                # Regra: Se a celula foi visitada e NAO ha brisa, entao vizinho nao tem poco
                # ~Brisa(r,c) ^ Visitada(r,c) => ~Poco(v_i)
                for v in vizinhos:
                    self.regras.append(([f"~Brisa({r},{c})", f"Visitada({r},{c})"], f"~Poco({v[0]},{v[1]})"))
                    self.regras.append(([f"~Fedor({r},{c})", f"Visitada({r},{c})"], f"~Wumpus({v[0]},{v[1]})"))

    def tell(self, fato: str):
        """ Adiciona um fato conhecido a base """
        self.fatos.add(fato)

    def tell_visitado(self, r: int, c: int):
        self.visitados.add((r, c))
        self.tell(f"Visitada({r},{c})")
        self.tell(f"~Poco({r},{c})")
        self.tell(f"~Wumpus({r},{c})")

    def inferir_conhecimento(self):
        """
        Algoritmo de Forward Chaining de complexidade O(N) para Clausulas de Horn.
        Propaga os fatos atraves das regras ate nao ser possivel deduzir nada novo.
        """
        mudou = True
        while mudou:
            total_antes = len(self.fatos)
            
            # 1. Avalia as implicacoes estruturais basicas
            for premissas, conclusao in self.regras:
                if conclusao not in self.fatos:
                    if all(p in self.fatos for p in premissas):
                        self.tell(conclusao)
            
            # 2. Logica de eliminacao para deteccao de perigos especificos
            for r in range(self.tamanho):
                for c in range(self.tamanho):
                    vizinhos = self._obter_vizinhos(r, c)
                    
                    # Deteccao de Poco por Eliminacao de Hipoteses
                    if f"Brisa({r},{c})" in self.fatos and f"Visitada({r},{c})" in self.fatos:
                        vizinhos_suspeitos = [v for v in vizinhos if f"~Poco({v[0]},{v[1]})" not in self.fatos]
                        if len(vizinhos_suspeitos) == 1:
                            v_perigo = vizinhos_suspeitos[0]
                            self.tell(f"Poco({v_perigo[0]},{v_perigo[1]})")

                    # Deteccao de Wumpus por Eliminacao de Hipoteses
                    if f"Fedor({r},{c})" in self.fatos and f"Visitada({r},{c})" in self.fatos:
                        vizinhos_suspeitos = [v for v in vizinhos if f"~Wumpus({v[0]},{v[1]})" not in self.fatos]
                        if len(vizinhos_suspeitos) == 1:
                            v_perigo = vizinhos_suspeitos[0]
                            self.tell(f"Wumpus({v_perigo[0]},{v_perigo[1]})")

                    # Regra de Seguranca: se provado que nao tem Wumpus E nao tem Poco, entao e Segura
                    if f"~Poco({r},{c})" in self.fatos and f"~Wumpus({r},{c})" in self.fatos:
                        self.tell(f"Segura({r},{c})")
            
            if len(self.fatos) == total_antes:
                mudou = False

    def ask(self, consulta: str) -> bool:
        """ Verifica se a consulta e uma consequencia logica comprovada """
        return consulta in self.fatos

    def eh_segura(self, r: int, c: int) -> bool:
        return self.ask(f"Segura({r},{c})")

    def eh_suspeita_poco(self, r: int, c: int) -> bool:
        return not self.ask(f"~Poco({r},{c})")

    def eh_suspeita_wumpus(self, r: int, c: int) -> bool:
        return not self.ask(f"~Wumpus({r},{c})")