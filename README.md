# Simulador de funciones del Kernel — Sistemas Operativos I

Proyecto académico de simulación (no modifica procesos, memoria ni hardware reales).

## Requisitos
- Python 3.10 o superior. No requiere librerías externas.

## Ejecución
```bash
python main.py
```

## Pruebas
Desde la carpeta principal:
```bash
python -m unittest discover -s pruebas -v
```

## Organización
- `procesos.py`: PCB y planificador Round Robin con quantum 3.
- `memoria.py`: asignación contigua dinámica first-fit de 100 MB.
- `semaforo.py`: sección crítica, cola de espera, `wait()` y `signal()`.
- `deadlock.py`: recursos exclusivos, grafo de espera y detección de ciclos.
- `kernel.py`: coordinación de módulos, creación y finalización.
- `main.py`: interfaz interactiva y validaciones.
- `pruebas/test_kernel.py`: pruebas automatizadas.

## Demostración rápida
1. Crear P1 con 80 MB, luego P2 con 30 MB: se rechaza P2 por Out of Memory.
2. Reiniciar. Crear P1 (10 MB, CPU 5), P2 (10 MB, CPU 4). Ejecutar todos: P1 0-3, P2 3-6, P1 6-8, P2 8-9.
3. Reiniciar. Crear P1 y P2. `wait(1)` y `wait(2)`; P2 queda bloqueado. `signal(1)` transfiere a P2.
4. Reiniciar. Crear P1 y P2. Simular Deadlock, detectar y abortar P1. Verificar que P2 recupera el recurso.

## Limitaciones didácticas
El planificador es de un solo CPU; el reloj avanza por ráfagas simuladas. No hay ejecución concurrente real ni hilos. Los procesos nuevos llegan al reloj actual. El modelo de RAM no compacta fragmentos. La sección crítica se simula mediante un propietario y una cola. Las operaciones sobre recursos son eventos lógicos y no consumen tiempo de CPU. Se prioriza el escenario de dos recursos exclusivos exigido en el enunciado.

## GitHub
Crear un repositorio y subir estos archivos desde su cuenta; el enlace debe incorporarse al reporte antes de entregar.
