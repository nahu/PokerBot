'''
Creado el Sep 27, 2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''
import Jugador
import Mesa

class PokerBot(object):
    '''
    Clase principal del juego
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def main(self):
        jugador1 = Jugador(1, nombre="PC", fichas=1000, bot=True)
        jugador2 = Jugador(2, nombre="Pibe", fichas=1000)
        mesa = Mesa(ciega=10, jugadores=[jugador1, jugador2])
        
        while True:
            resultado = mesa.juego()
            print "Ganó el jugador" + mesa.jugadores[resultado[1]]
            print "Jugada ganadora: " + resultado[2]
            
            if not resultado[0]:#el juego terminó
                break
            
            
            
                