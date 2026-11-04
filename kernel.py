from procesos import PCB, Estado, Planificador
from memoria import Memoria
from semaforo import SemaforoBinario
from deadlock import Recursos

class Kernel:
    def __init__(self):
        self.procesos = {}
        self.memoria = Memoria(100)
        self.planificador = Planificador(3)
        self.semaforo = SemaforoBinario()
        self.recursos = Recursos()
        self.eventos = []

    def registrar(self, mensaje):
        self.eventos.append(mensaje)
        return mensaje

    def crear(self, pid, memoria, rafaga):
        if not all(isinstance(x, int) and not isinstance(x, bool) for x in (pid, memoria, rafaga)):
            raise ValueError('Los parametros deben ser enteros.')
        if pid <= 0 or memoria <= 0 or rafaga <= 0:
            raise ValueError('PID, memoria y rafaga deben ser positivos.')
        if pid in self.procesos:
            raise ValueError('PID duplicado.')
        inicio = self.memoria.asignar(pid, memoria)
        p = PCB(pid, Estado.LISTO, memoria, rafaga, rafaga, self.planificador.reloj)
        self.procesos[pid] = p
        self.planificador.agregar(p)
        return self.registrar(f'P{pid} creado: {memoria} MB desde direccion {inicio}; CPU {rafaga}.')

    def terminar(self, pid):
        p = self.procesos.get(pid)
        if p is None or p.estado == Estado.TERMINADO:
            raise ValueError('Proceso inexistente o ya terminado.')
        self.planificador.quitar(pid)
        self.semaforo.eliminar(pid, self.procesos, self.planificador)
        self.recursos.liberar_proceso(pid, self.procesos, self.planificador)
        self.memoria.liberar(pid)
        p.estado = Estado.TERMINADO
        return self.registrar(f'P{pid} TERMINADO; memoria y recursos liberados.')

    def ejecutar(self):
        evento = self.planificador.ejecutar_turno(self.procesos, self.terminar)
        if evento:
            self.registrar(f"RR: P{evento['pid']} [{evento['inicio']},{evento['fin']}] -> {evento['resultado']}")
        return evento

    def ejecutar_todos(self, limite=10000):
        eventos = []
        while self.planificador.cola and len(eventos) < limite:
            evento = self.ejecutar()
            if evento is None:
                break
            eventos.append(evento)
        return eventos

    def provocar_deadlock(self, pid_a, pid_b):
        if pid_a == pid_b:
            raise ValueError('Se necesitan dos procesos distintos.')
        for pid in (pid_a, pid_b):
            if pid not in self.procesos or self.procesos[pid].estado != Estado.LISTO:
                raise ValueError('Ambos procesos deben existir y estar LISTOS.')
        if any(v is not None for v in self.recursos.duenos.values()) or self.recursos.esperando:
            raise ValueError('Recursos ocupados; use procesos y recursos libres.')
        mensajes = [self.recursos.solicitar(pid_a, 'R1', self.procesos, self.planificador),
                    self.recursos.solicitar(pid_b, 'R2', self.procesos, self.planificador),
                    self.recursos.solicitar(pid_a, 'R2', self.procesos, self.planificador),
                    self.recursos.solicitar(pid_b, 'R1', self.procesos, self.planificador)]
        ciclo = self.recursos.detectar()
        self.registrar('DEADLOCK DETECTADO: ' + str(ciclo))
        return mensajes, ciclo
