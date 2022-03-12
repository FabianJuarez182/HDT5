# -*- coding: utf-8 -*-
"""
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
─██████████████─██████████████─██████████████───██████████─██████████████─██████──────────██████────────────██████─██████──██████─██████████████─████████████████───██████████████─██████████████████─
─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░██───██░░░░░░██─██░░░░░░░░░░██─██░░██████████──██░░██────────────██░░██─██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░░░██───██░░░░░░░░░░██─██░░░░░░░░░░░░░░██─
─██░░██████████─██░░██████░░██─██░░██████░░██───████░░████─██░░██████░░██─██░░░░░░░░░░██──██░░██────────────██░░██─██░░██──██░░██─██░░██████░░██─██░░████████░░██───██░░██████████─████████████░░░░██─
─██░░██─────────██░░██──██░░██─██░░██──██░░██─────██░░██───██░░██──██░░██─██░░██████░░██──██░░██────────────██░░██─██░░██──██░░██─██░░██──██░░██─██░░██────██░░██───██░░██─────────────────████░░████─
─██░░██████████─██░░██████░░██─██░░██████░░████───██░░██───██░░██████░░██─██░░██──██░░██──██░░██────────────██░░██─██░░██──██░░██─██░░██████░░██─██░░████████░░██───██░░██████████───────████░░████───
─██░░░░░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░░░██───██░░██───██░░░░░░░░░░██─██░░██──██░░██──██░░██────────────██░░██─██░░██──██░░██─██░░░░░░░░░░██─██░░░░░░░░░░░░██───██░░░░░░░░░░██─────████░░████─────
─██░░██████████─██░░██████░░██─██░░████████░░██───██░░██───██░░██████░░██─██░░██──██░░██──██░░██────██████──██░░██─██░░██──██░░██─██░░██████░░██─██░░██████░░████───██░░██████████───████░░████───────
─██░░██─────────██░░██──██░░██─██░░██────██░░██───██░░██───██░░██──██░░██─██░░██──██░░██████░░██────██░░██──██░░██─██░░██──██░░██─██░░██──██░░██─██░░██──██░░██─────██░░██─────────████░░████─────────
─██░░██─────────██░░██──██░░██─██░░████████░░██─████░░████─██░░██──██░░██─██░░██──██░░░░░░░░░░██────██░░██████░░██─██░░██████░░██─██░░██──██░░██─██░░██──██░░██████─██░░██████████─██░░░░████████████─
─██░░██─────────██░░██──██░░██─██░░░░░░░░░░░░██─██░░░░░░██─██░░██──██░░██─██░░██──██████████░░██────██░░░░░░░░░░██─██░░░░░░░░░░██─██░░██──██░░██─██░░██──██░░░░░░██─██░░░░░░░░░░██─██░░░░░░░░░░░░░░██─
─██████─────────██████──██████─████████████████─██████████─██████──██████─██████──────────██████────██████████████─██████████████─██████──██████─██████──██████████─██████████████─██████████████████─
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Creado el 9 de marzo del 2022



@author: Fabian Juarez
"""
import simpy
import random

lista = [] #lista para obtener cuanto tarda cada proceso
num = 0

def proceso(nombre, env, memoria, cpu, llegada, cantidad_instrucciones, cantidad_ram, tiempo_ejecucion):

    # Simula la espera de llegada del proceso
    yield env.timeout(llegada)

    #grabo el tiempo de llegada
    tiempo_llegada = env.now
    #------------------------------------------------------------------NEW------------------------------------------------------------------
    print('%s proceso en cola NEW llegada -> %d cantidad ram requerida %d, disponible %d' % (nombre, env.now, cantidad_ram, memoria.level))
    yield memoria.get(cantidad_ram)  #Pide la memoria que necesita o espera automaticamente hasta que haya suficiente

    while cantidad_instrucciones > 0:  #Verificara hasta que no hayan instrucciones pendientes

    #------------------------------------------------------------------READY------------------------------------------------------------------
        # Ya tiene memoria para iniciar
        print('%s proceso en cola READY tiempo -> %d cantidad instrucciones pendientes %d' % (nombre, env.now, cantidad_instrucciones))

        with cpu.request() as req:  #pide el procesador
            yield req

            cantidad_instrucciones = cantidad_instrucciones - 3
            yield env.timeout(1) #Simula un ciclo de reloj del procesador

            #------------------------------------------------------------------RUNNING------------------------------------------------------------------
            # Ya tiene procesador
            print('%s proceso en estado RUNNING fue atendido en tiempo -> %d cantidad ram %d, Instrucciones pendientes %d ram disponible %d' % (nombre, env.now, cantidad_ram, cantidad_instrucciones, memoria.level))


    # Cuando ya finaliza devuelve la memoria utilizada
    yield memoria.put(cantidad_ram)

    #------------------------------------------------------------------TERMINATED------------------------------------------------------------------
    print('%s proceso TERMINATED salida -> %d cantidad ram devuelta %d, nueva cantidad de memoria disponible %d' % (nombre, env.now, cantidad_ram, memoria.level))
    global tiempo_total
    tiempo_total += env.now - tiempo_llegada #tiempo que tado el CPU en hacer todos los procesos
    tiempo_ejecucion = env.now - tiempo_llegada #Tiempo que tarda el proceso especifico en terminar sus instrucciones
    lista.append(tiempo_ejecucion) #agregar el tiempo que tarda cada proceso
    print('Tiempo total %d' % (env.now - tiempo_llegada))


random.seed(10)
env = simpy.Environment()  # crear ambiente de simulacion
initial_ram = simpy.Container(env, 100, init=100)  # crea el container de la ram
initial_cpu = simpy.Resource(env, capacity=1)  # se crea el procesador con capacidad establecida
initial_procesos = 25  # cantidad de procesos a generar
tiempo_total = 0 #Control para saber el tiempo que se hara el CPU en hacer todos los procesos
interval = 10 # Intervalo a usar

for i in range(initial_procesos):
    llegada = random.randint(1,interval)#Todos los procesos llegan a su tiempo
    cantidad_instrucciones = random.randint(1, 10)  # cantidad de operaciones por proceso
    UsoRam = random.randint(1, 10)  # cantidad de ram que requiere cada proceso
    env.process(proceso('proceso %d' % i, env, initial_ram, initial_cpu, llegada, cantidad_instrucciones, UsoRam, 0))

# correr la simulacion
env.run()
print('tiempo promedio %d ' % (tiempo_total / initial_procesos)) # calculo para sacar el tiempo promedio de todos los procesos
for i in range(initial_procesos):
    num += (lista[i]-(tiempo_total / initial_procesos))**2 # Calculo para sacar la sumatoria
desv_Total = (num/initial_procesos)**0.5 # calculo para sacar la desviacion estandar
print('desviacion estandar %d ' % (desv_Total))