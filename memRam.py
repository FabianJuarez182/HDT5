# -*- coding: utf-8 -*-
"""
Creado el 9 de marzo del 2022

@author: Fabian Juarez
"""
import simpy as simpy;
import random as rand;

RANDOM_SEED = 42
interval = 10 #intervalo a utilizar
number_Programs = 25 # numero total de procesos


def source (env, number_Programs, interval, counter):
    """Source generara programas random"""
    for i in range(number_Programs):
        mem = rand.randint(1,10)
        c = ram(env, 'Program%02d' % i, counter, mem)
        env.process(c)
        t = rand.randint(1,interval)
        yield env.timeout(t)

def ram(env, id, counter, numInstruct):
    """Program arrives, is served and leaves."""
    arrive = env.now
    print('%s: Comenzando a ejecutarse. Al tiempo: %d' % (id, arrive))

    with counter.request() as req:  #pedimos conectarnos a la ram
        yield req

        # Cargamos el programa a la ram
        yield env.timeout(numInstruct)
        print('%s Proceso terminado al tiempo: %d' % (id, env.now))
        # se hizo release automatico del cargador bcs

rand.seed(RANDOM_SEED)
env = simpy.Environment()#Crea ambiente de simulacion.

RAM = simpy.Container(env, init=100, capacity=100)

#getRam = ram.get(mem)

#Ram=RAM.put(mem)
#rand.seed(RANDOM_SEED)
#Creacion de los programas
#for i in range(interval):
#    id="Programa "+ str(i)#identificacion del programa
 #   mem = rand.expovariate(1/10)
  #  numInstruct = rand.expovariate(1.0/interval)
   # env.process(ram(env,id,bcs,numInstruct))

#Corre la simulacio
counter = simpy.Resource(env, capacity=1) # RAM de la computadora que solo soporta 1 programa a la vez
env.process(source(env, number_Programs, interval, counter))
env.run()