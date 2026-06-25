from ambiente import AmbienteWumpus
from agente import AgenteBaseadoConhecimento
from conhecimento import BaseConhecimento
from typing import List
import random


class InicializarCenario:
    def __init__(self, n_times: int, n_agentes_time: int, grid_size: int,):
        self.n_times = n_times
        self.n_agentes_time = n_agentes_time
        self.grid_size = grid_size
        self.agentes_total = n_times * n_agentes_time
        self.inicios = [(random.randrange(0, grid_size), random.randrange(0, grid_size)) \
                        for _ in range(self.agentes_total)] \
                        if self.agentes_total != 1 else [(0,0)]
        self.world: AmbienteWumpus = None
        self.times: List[List[AgenteBaseadoConhecimento]] = []
        
        self.__inicializar_mundo()
        self.__inicializar_times()



    def __inicializar_mundo(self):
        world = AmbienteWumpus(tamanho=self.grid_size, inicios_agentes=self.inicios)
        self.world = world


    def __inicializar_times(self):
        notificacoes = []
        times = []
        for i in range(self.n_times):
            kb = BaseConhecimento(self.grid_size)
            times.append([AgenteBaseadoConhecimento(tamanho=self.grid_size, env=self.world, kb=kb, inicio_agente=self.inicios[i*self.n_agentes_time+n], notificacoes=notificacoes) for n in range(self.n_agentes_time)])

        self.times = times
