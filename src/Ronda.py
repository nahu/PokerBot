# -*- coding: utf-8 -*-
'''
Creado el 23/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

class Ronda(object):
    '''
    Ronda para mandar al jugador el estado de la mesa relevante para realizar
    su jugada.
    '''

    def __init__(self, tipo, nro_apuesta, ciega, pot, dealer):
        '''
        Constructor
        @param tipo : para saber el tipo de ronda y las apuesta
        hasta el momento en esa ronda
        1-preflop, 2-flop, 3-turn y 4-river
        @type tipo : int
        @param nro_apuesta : cuantas se realizaron el la ronda
        el límite es 4
        1, 2, 3 o 4 veces.
        '''
        self.tipo = tipo
        self.nro_apuesta = nro_apuesta
        self.ciega = ciega
        self.pot = pot
        self.dealer = dealer
    
    def apuesta_de_ronda(self):           
        return self.pot + (self.monto_a_subir() * self.nro_apuesta)
    
    def monto_a_subir(self):
        if (self.tipo == 1 or self.tipo == 2):
            return self.ciega
        elif (self.tipo == 3 or self.tipo == 4):
            return self.ciega * 2
    
    def monto_a_igualar(self):
        if (self.tipo == 1 and self.dealer):
            return self.ciega/2
        else:
            return self.monto_a_subir()
        
    
          
        