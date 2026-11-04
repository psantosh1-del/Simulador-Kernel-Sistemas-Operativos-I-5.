"""python main.py"""
from kernel import Kernel
from procesos import Estado

MENU = '''\n====== SIMULADOR DE KERNEL (UMG) ======
RAM: 100 MB | Quantum RR: 3
1. Crear proceso
2. Listar PCB
3. Ejecutar un turno Round Robin
4. Ejecutar todos los turnos disponibles
5. Ver mapa de RAM
6. Semaforo wait()
7. Modificar variable compartida (+1)
8. Semaforo signal()
9. Simular Deadlock
10. Detectar Deadlock
11. Abortar proceso
12. Historial de eventos
0. Salir
======================================'''

def entero(mensaje):
    try:
        valor = int(input(mensaje).strip())
    except ValueError:
        raise ValueError('Introduzca un numero entero valido.')
    return valor

def mostrar_pcb(k):
    print('PID | ESTADO     | RAM | TOTAL | RESTANTE | ESPERA | FIN')
    for p in sorted(k.procesos.values(), key=lambda p:p.pid):
        print(f'{p.pid:>3} | {p.estado.value:<10} | {p.memoria:>3} | {p.rafaga_total:>5} | {p.rafaga_restante:>8} | {p.espera:>6} | {str(p.finalizacion):>3}')

def iniciar():
    k = Kernel()
    while True:
        print(MENU)
        try:
            op = entero('Opcion: ')
            if op == 0:
                print('Hasta luego.')
                break
            elif op == 1:
                print(k.crear(entero('PID: '), entero('Memoria MB: '), entero('Rafaga CPU: ')))
            elif op == 2:
                mostrar_pcb(k)
            elif op == 3:
                print(k.ejecutar() or 'No hay procesos LISTOS.')
            elif op == 4:
                ev = k.ejecutar_todos()
                for e in ev:
                    print(f"P{e['pid']}: {e['inicio']}->{e['fin']} ({e['resultado']})")
                print(f'{len(ev)} turnos completados; reloj={k.planificador.reloj}.')
            elif op == 5:
                print(f'Usada: {k.memoria.usada} MB | Libre total: {100-k.memoria.usada} MB')
                print('Segmentos (inicio, MB, PID):', k.memoria.mapa())
            elif op == 6:
                print(k.semaforo.wait(entero('PID: '), k.procesos, k.planificador))
            elif op == 7:
                print('Variable global =', k.semaforo.incrementar(entero('PID propietario: ')))
            elif op == 8:
                print(k.semaforo.signal(entero('PID propietario: '), k.procesos, k.planificador))
            elif op == 9:
                mensajes, ciclo = k.provocar_deadlock(entero('PID A: '), entero('PID B: '))
                print('\n'.join(mensajes))
                print('ALERTA: DEADLOCK', ciclo)
            elif op == 10:
                print('DEADLOCK:', k.recursos.detectar() or 'No detectado')
            elif op == 11:
                print(k.terminar(entero('PID a abortar: ')))
            elif op == 12:
                print('\n'.join(k.eventos) or 'Sin eventos.')
            else:
                print('Opcion no disponible.')
        except (ValueError, MemoryError, PermissionError) as exc:
            print('ERROR:', exc)
        except (EOFError, KeyboardInterrupt):
            print('\nSesion finalizada.')
            break

if __name__ == '__main__':
    iniciar()
