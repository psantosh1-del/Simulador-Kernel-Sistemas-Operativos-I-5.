from collections import deque
from procesos import Estado

class SemaforoBinario:
    def __init__(self):
        self.dueno = None
        self.espera = deque()
        self.variable_compartida = 0

    def wait(self, pid, procesos, planificador):
        if pid not in procesos or procesos[pid].estado == Estado.TERMINADO:
            raise ValueError('PID inexistente o terminado.')
        if self.dueno == pid:
            raise ValueError('El proceso ya posee el semaforo.')
        if pid in self.espera:
            raise ValueError('El proceso ya esta en espera.')
        if self.dueno is None:
            self.dueno = pid
            return f'P{pid} ingreso a la seccion critica.'
        procesos[pid].estado = Estado.BLOQUEADO
        planificador.quitar(pid)
        self.espera.append(pid)
        return f'P{pid} BLOQUEADO; seccion critica ocupada por P{self.dueno}.'

    def incrementar(self, pid):
        if self.dueno != pid:
            raise PermissionError('Solo el propietario modifica la variable compartida.')
        self.variable_compartida += 1
        return self.variable_compartida

    def signal(self, pid, procesos, planificador):
        if self.dueno != pid:
            raise PermissionError('Solo el propietario puede liberar el semaforo.')
        self.dueno = None
        while self.espera:
            siguiente = self.espera.popleft()
            if siguiente in procesos and procesos[siguiente].estado != Estado.TERMINADO:
                self.dueno = siguiente
                procesos[siguiente].estado = Estado.LISTO
                planificador.agregar(procesos[siguiente])
                return f'Semaforo transferido a P{siguiente}.'
        return 'Semaforo liberado.'

    def eliminar(self, pid, procesos, planificador):
        self.espera = deque(x for x in self.espera if x != pid)
        if self.dueno == pid:
            self.dueno = None
            while self.espera:
                sig = self.espera.popleft()
                if sig in procesos and procesos[sig].estado != Estado.TERMINADO:
                    self.dueno = sig
                    procesos[sig].estado = Estado.LISTO
                    planificador.agregar(procesos[sig])
                    break
