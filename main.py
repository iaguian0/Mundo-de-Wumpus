from ambiente import AmbienteWumpus
from agente import AgenteBaseadoConhecimento
from conhecimento import BaseConhecimento

def executar_projeto():
    # Define a dimensao minima exigida de 4x4
    TAMANHO_GRADE = 4 
    
    print(f"Inicializando Componentes e Gerando Ambiente {TAMANHO_GRADE}x{TAMANHO_GRADE}...")
    mundo = AmbienteWumpus(tamanho=TAMANHO_GRADE)
    
    print("\nMapa Real do Mundo Oculto (A=Agente, W=Wumpus, P=Poco, O=Ouro):")
    mundo.exibir_ambiente(mundo.inicio_agente)
    
    kb = BaseConhecimento(TAMANHO_GRADE)
    
    agente = AgenteBaseadoConhecimento(tamanho=TAMANHO_GRADE, env=mundo, kb=kb)
    
    # Executa as inferencias logicas e as acoes
    agente.executar_simulacao()

if __name__ == "__main__":
    executar_projeto()