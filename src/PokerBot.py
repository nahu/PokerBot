# -*- coding: utf-8 -*-
'''
Creado el Sep 27, 2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''
from Bot import Bot
from Mesa2 import Mesa

FICHAS1 = 10000
FICHAS2 = 10000
CIEGAS = 100
P = 0.5
class PokerBot(object):
    '''
    Clase principal del juego
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def main(self):
        jugador1 = Bot(1, nombre="PC", fichas=FICHAS1)
        jugador2 = Bot(2, nombre="Pibe", fichas=FICHAS2)
        mesa = Mesa(CIEGAS, [jugador1, jugador2], P)
        
        while True:
            resultado = mesa.juego()
            print "Ganó el jugador" + mesa.jugadores[resultado[1]]
            print "Jugada ganadora: " + resultado[2]
            
            if not resultado[0]:#el juego terminó
                print "El juego terminó"
                break
            
            

a = PokerBot()

            
                