# -*- coding: utf-8 -*-
'''
Creado el 23/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''
import Mazo

class Mesa(object):
    '''
    Manejadora del juego
    '''


    def __init__(self, ciega, mazo):
        '''
        Constructor
        '''
        self.ciega = ciega
        self.mazo = Mazo
        self.bote = 0
        self.jugadores = []
        self.dealer = 0 #posicion en la lista jugaores
        self.comunitarias = []
        self.ronda_actual = None
        