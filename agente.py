from typing import List, Tuple, Optional
from ambiente import AmbienteWumpus
from conhecimento import BaseConhecimento
from busca import encontrar_caminho

class AgenteBaseadoConhecimento:
    """
    Agente que toma decisoes deliberativas a partir das percepcoes e inferencias
    logicas armazenadas de forma estruturada na Base de Conhecimento.
    """
    def __init__(self, tamanho: int, env: AmbienteWumpus):
        self.tamanho = tamanho
        self.env = env
        self.kb = BaseConhecimento(tamanho)
        self.pos_atual = env.inicio_agente
        self.tem_ouro = False
        self.esta_vivo = True
        self.historico_trajetoria: List[Tuple[int, int]] = [self.pos_atual]
        self.registro_acoes: List[str] = []
        
        # Conhecimento inicial da celula de partida
        self.kb.tell_visitado(self.pos_atual[0], self.pos_atual[1])
        self.kb.inferir_conhecimento()
        self.passo = 0

        self.caminho_retorno = []
        self.notificacoes = []

    def perceber_e_inferir(self):
        r, c = self.pos_atual
        percepcoes = self.env.obter_percepcoes(r, c)
        self.registro_acoes.append(f"Percebeu {list(percepcoes)} em ({r},{c})")
        
        # Insere a percepcao positiva ou negativa na KB
        if "Brisa" in percepcoes:
            self.kb.tell(f"Brisa({r},{c})")
        else:
            self.kb.tell(f"~Brisa({r},{c})")
            
        if "Fedor" in percepcoes:
            self.kb.tell(f"Fedor({r},{c})")
        else:
            self.kb.tell(f"~Fedor({r},{c})")
            
        if "Brilho" in percepcoes:
            self.kb.tell(f"Brilho({r},{c})")
            
        self.kb.inferir_conhecimento()

    def escolher_proximo_movimento(self) -> Optional[Tuple[int, int]]:
        seguras_nao_visitadas = []
        for r in range(self.tamanho):
            for c in range(self.tamanho):
                if self.kb.eh_segura(r, c) and (r, c) not in self.kb.visitados:
                    seguras_nao_visitadas.append((r, c))

        if seguras_nao_visitadas:
            menor_caminho = None
            celula_escolhida = None
            for celula in seguras_nao_visitadas:
                caminho = encontrar_caminho(self.tamanho, self.pos_atual, celula, self.kb)
                if caminho is not None:
                    if menor_caminho is None or len(caminho) < len(menor_caminho):
                        menor_caminho = caminho
                        celula_escolhida = celula
            if celula_escolhida:
                return celula_escolhida

        # Gerenciamento de Risco calculado quando encurralado
        vizinhos = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = self.pos_atual[0] + dr, self.pos_atual[1] + dc
            if 0 <= nr < self.tamanho and 0 <= nc < self.tamanho:
                vizinhos.append((nr, nc))
                
        vizinhos_nao_visitados = [n for n in vizinhos if n not in self.kb.visitados]
        if vizinhos_nao_visitados:
            melhor_celula = vizinhos_nao_visitados[0]
            menor_risco = 999
            for n in vizinhos_nao_visitados:
                risco = 0
                if self.kb.eh_suspeita_poco(n[0], n[1]): risco += 1
                if self.kb.eh_suspeita_wumpus(n[0], n[1]): risco += 2
                if risco < menor_risco:
                    menor_risco = risco
                    melhor_celula = n
            return melhor_celula

        return None
    
    def caminhar(self):
        if not self.esta_vivo: return False

        if not self.tem_ouro:
            r, c = self.pos_atual

            print(f"\nPASSO {self.passo} - Posicao Atual do Agente: ({r},{c})")
            
            self.perceber_e_inferir()
            
            if "Ouro" in self.env.grade[r][c]:
                print("[EVENTO] Ouro encontrado. Coletando e planejando retorno.")
                self.notificacoes.append('[EVENTO] Ouro encontrado')

                self.registro_acoes.append(f"Pegou o ouro em ({r},{c})")
                self.tem_ouro = True
                self.caminho_retorno = encontrar_caminho(self.tamanho, self.pos_atual, self.env.inicio_agente, self.kb)
                return True

            if "Wumpus" in self.env.grade[r][c]:
                print("[FAIL] Agente eliminado pelo Wumpus.")
                self.notificacoes.append('[FAIL] Agente eliminado pelo Wumpus.')

                self.esta_vivo = False
                return False

            if "Poco" in self.env.grade[r][c]:
                print("[FAIL] Agente caiu em um poco.")
                self.notificacoes.append('[FAIL] Agente caiu em um poco.')

                self.esta_vivo = False
                return False

            proximo_alvo = self.escolher_proximo_movimento()
            if proximo_alvo is None:
                print("[AVISO] Agente encurralado. Sem rotas validas disponiveis.")
                self.notificacoes.append('[AVISO] Agente encurralado')
                return False
                
            caminho = encontrar_caminho(self.tamanho, self.pos_atual, proximo_alvo, self.kb)
            self.passo += 1
            if caminho:
                movimento = caminho[0]
                self.pos_atual = movimento
                self.historico_trajetoria.append(movimento)
                self.kb.tell_visitado(movimento[0], movimento[1])
                self.registro_acoes.append(f"Moveu-se para ({movimento[0]},{movimento[1]})")
            else:
                self.pos_atual = proximo_alvo
                self.historico_trajetoria.append(proximo_alvo)
                self.kb.tell_visitado(proximo_alvo[0], proximo_alvo[1])
                self.registro_acoes.append(f"Moveu-se para ({proximo_alvo[0]},{proximo_alvo[1]})")
            return True
        
        else:
            print("\nIniciando trajetoria de retorno para a origem (0,0)...")
            print(self.caminho_retorno)
            if self.caminho_retorno:
                self.passo += 1
                movimento = self.caminho_retorno.pop(0)
                self.pos_atual = movimento
                self.historico_trajetoria.append(movimento)
                self.registro_acoes.append(f"Retorno: Moveu-se para ({movimento[0]},{movimento[1]})")
                return True
            print("[SUCESSO] Ouro coletado e retorno executado em seguranca.")
            self.notificacoes.append('[SUCESSO] Retorno executado')
            return False

    def executar_simulacao(self):
        print("\n==================================================")
        print("INICIO DA SIMULACAO: MUNDO DE WUMPUS (HORN-SAT)")
        print("==================================================")

        continuar = True
        while continuar:
            continuar = self.caminhar()

        self._exibir_relatorio_final()

    def _exibir_relatorio_final(self):
        print("\n" + "="*50)
        print("RELATORIO FINAL DE EXECUCAO DO AGENTE")
        print("="*50)
        print(f"Status Final: {'VIVO' if self.esta_vivo else 'MORTO'}")
        print(f"Objetivo Concluido (Ouro): {'SIM' if self.tem_ouro else 'NAO'}")
        print(f"Trajetoria Completa: {self.historico_trajetoria}")
        print("\nHistorico de Acoes Executadas:")
        for log in self.registro_acoes:
            print(f" - {log}")
        print("\nSentencas Atomicas Provadas na KB:")
        print(sorted(list(self.kb.fatos)))

    def get_notificacoes(self, n: int):
        return self.notificacoes[len(self.notificacoes)-min(len(self.notificacoes), n):][::-1]
    