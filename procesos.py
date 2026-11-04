from dataclasses import dataclass
from enum import Enum
from collections import deque

class Estado(str, Enum):
    LISTO = 'LISTO'
    EJECUTANDO = 'EJECUTANDO'
    BLOQUEADO = 'BLOQUEADO'
    TERMINADO = 'TERMINADO'

@dataclass
class PCB:
    pid: int
    estado: Estado
    memoria: int
    rafaga_total: int
    rafaga_restante: int
    llegada: int = 0
    finalizacion: int | None = None
    espera: int = 0

class Planificador:
    def __init__(self, quantum=3):
        self.quantum = quantum
        self.cola = deque()
        self.reloj = 0
        self.historial = []

    def agregar(self, pcb):
        if pcb.estado == Estado.LISTO and pcb.pid not in self.cola:
            self.cola.append(pcb.pid)

    def quitar(self, pid):
        self.cola = deque(x for x in self.cola if x != pid)

    def ejecutar_turno(self, procesos, finalizar):
        while self.cola:
            pid = self.cola.popleft()
            p = procesos.get(pid)
            if p is None or p.estado != Estado.LISTO:
                continue
            p.estado = Estado.EJECUTANDO
            inicio = self.reloj
            duracion = min(self.quantum, p.rafaga_restante)
            self.reloj += duracion
            p.rafaga_restante -= duracion
            evento = {'pid':pid,'inicio':inicio,'fin':self.reloj,'ejecutado':duracion,'restante':p.rafaga_restante}
            self.historial.append(evento)
            if p.rafaga_restante == 0:
                p.finalizacion = self.reloj
                p.espera = p.finalizacion - p.llegada - p.rafaga_total
                finalizar(pid)
                evento['resultado'] = 'TERMINADO'
            else:
                p.estado = Estado.LISTO
                self.cola.append(pid)
                evento['resultado'] = 'CAMBIO DE CONTEXTO'
            return evento
        return None
