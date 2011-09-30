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
from Mesa import Mesa

FICHAS1 = 10000
FICHAS2 = 10000
CIEGAS = 500
P = 0.5

class loco():
    def acquire(self):
        pass
    def release(self):
        pass
    
lock = loco()

class PokerBot(object):
    '''
    Clase principal del juego
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def main(self):

        jugadas = 0
        empates = 0
        jugador1 = Bot(1, FICHAS1, "Bot 1", 0.1)
        jugador2 = Bot(2, FICHAS2, "bot 2", 0.1)
        mesa = Mesa(CIEGAS, [jugador1, jugador2], lock)
        
        while True:
            resultado = mesa.juego()
            jugadas += 1
            print "resultado: ", resultado
            if resultado[1] != None:
                print "Ganó el jugador: " + str(mesa.jugadores[resultado[1]].nombre)
                print "Jugada ganadora: " + resultado[2]
            else:
                empates += 1
                print "empate"
                print "Jugada empatadora: ", resultado[2]
            
            print "----------Estado final de mesa-----------"
            mesa.imprimir()
            if not resultado[0]:#el juego terminó
                print "El juego terminó"
                break
        
        
        print "Jugadas: ", jugadas
        print "Empates: ", empates
    
            #raw_input()
            
            

a = PokerBot()
a.main()

            
                
