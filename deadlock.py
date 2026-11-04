from procesos import Estado

class Recursos:
    def __init__(self):
        self.duenos = {'R1': None, 'R2': None}
        self.esperando = {}

    def solicitar(self, pid, recurso, procesos, planificador):
        if recurso not in self.duenos:
            raise ValueError('Recurso invalido.')
        if pid not in procesos or procesos[pid].estado == Estado.TERMINADO:
            raise ValueError('Proceso no disponible.')
        dueno = self.duenos[recurso]
        if dueno == pid:
            return f'P{pid} ya posee {recurso}.'
        if dueno is None:
            self.duenos[recurso] = pid
            self.esperando.pop(pid, None)
            return f'{recurso} asignado a P{pid}.'
        self.esperando[pid] = recurso
        procesos[pid].estado = Estado.BLOQUEADO
        planificador.quitar(pid)
        return f'P{pid} espera {recurso}, retenido por P{dueno}.'

    def detectar(self):
        # Grafo de espera: proceso -> proceso que posee el recurso esperado.
        aristas = {pid: self.duenos[r] for pid, r in self.esperando.items()
                   if self.duenos[r] is not None}
        for inicio in aristas:
            ruta = []
            actual = inicio
            while actual in aristas and actual not in ruta:
                ruta.append(actual)
                actual = aristas[actual]
            if actual in ruta:
                return ruta[ruta.index(actual):]
        return []

    def liberar_proceso(self, pid, procesos, planificador):
        self.esperando.pop(pid, None)
        for recurso, dueno in list(self.duenos.items()):
            if dueno == pid:
                self.duenos[recurso] = None
        # Reintentar las solicitudes pendientes de forma determinista.
        for p, recurso in list(self.esperando.items()):
            if self.duenos[recurso] is None:
                self.duenos[recurso] = p
                del self.esperando[p]
                if p in procesos and procesos[p].estado != Estado.TERMINADO:
                    procesos[p].estado = Estado.LISTO
                    planificador.agregar(procesos[p])
