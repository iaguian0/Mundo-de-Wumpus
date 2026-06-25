from typing import List, Tuple, Optional

def encontrar_caminho(tamanho: int, inicio: Tuple[int, int], destino: Tuple[int, int], kb) -> Optional[List[Tuple[int, int]]]:
    """
    Encontra uma rota livre de perigos entre o ponto inicial e o destino usando BFS.
    Garante que o agente trafegue apenas por caminhos validados pela Base de Conhecimento.
    """
    fila = [[inicio]]
    visitados = {inicio}
    
    if inicio == destino:
        return []

    while fila:
        caminho = fila.pop(0)
        no = caminho[-1]
        
        if no == destino:
            return caminho[1:]
            
        # Adjacencias
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = no[0] + dr, no[1] + dc
            if 0 <= nr < tamanho and 0 <= nc < tamanho:
                vizinho = (nr, nc)
                if vizinho not in visitados:
                    # So avanca se a KB provar que e seguro ou se for o alvo de risco calculado
                    if kb.eh_segura(nr, nc) or vizinho == destino:
                        visitados.add(vizinho)
                        novo_caminho = list(caminho)
                        novo_caminho.append(vizinho)
                        fila.append(novo_caminho)
    return None
