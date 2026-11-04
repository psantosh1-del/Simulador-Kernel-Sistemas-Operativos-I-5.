class Memoria:
    """Asignacion contigua dinamica: lista de segmentos (inicio, tamano, pid)."""
    def __init__(self, capacidad=100):
        self.capacidad = capacidad
        self.segmentos = []

    @property
    def usada(self):
        return sum(t for _, t, _ in self.segmentos)

    def asignar(self, pid, tamano):
        if not isinstance(tamano, int) or tamano <= 0:
            raise ValueError('La memoria debe ser un entero positivo.')
        cursor = 0
        for inicio, largo, _ in sorted(self.segmentos):
            if inicio - cursor >= tamano:
                break
            cursor = inicio + largo
        if self.capacidad - cursor < tamano:
            raise MemoryError(f'Out of Memory: no existe un bloque contiguo de {tamano} MB disponible.')
        self.segmentos.append((cursor, tamano, pid))
        self.segmentos.sort()
        return cursor

    def liberar(self, pid):
        self.segmentos = [s for s in self.segmentos if s[2] != pid]

    def mapa(self):
        return sorted(self.segmentos)
