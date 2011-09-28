# -*- coding: utf-8 -*-
'''
Creado en 22/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

class Jugador(object):
    '''
    Clase que define un jugador
    '''


    def __init__(self, identificador, fichas, nombre = None, bot = False):
        '''
        Constructor, se definen todos los atributos para la clase Jugador
        '''
        self.fichas = fichas
        self.id = identificador
        self.nombre = nombre
        self.mano = [None, None]
        self.bot = bot
        self.apuesta_actual = 0
        self.dealer = False
        
    def verificar_allin(self, apuesta):
        if (apuesta > self.fichas):
            return True
        else:
            return False
            
    def obtener_jugada(self, ronda, comunitarias):
        '''
        Dependiendo de la ronda hace lo que tiene que hacer
        @param ronda : Ronda, para saber el tipo de ronda y las apuesta
        hasta el momento en esa ronda
        1-preflop, 2-flop, 3-turn y 4-river
        1, 2, 3 o 4 veces.
        @type ronda: Ronda
        @param comunitarias: lista de 5 strings que denotan las cartas
        comunitarias en la ronda, por ejemplo, si es el flop la lista 
        sería [carta1, carta2, carta3, None, None]
        @type comunitarias: String[]
        @return jugada : devuelve lo que tiene que hacer
        si es un jugador se obtiene de la pantalla
        si es un bot se calcula.
        [ir(igualar), no_ir, aumentar, all_in, salir, pasar, mostrar, no_mostrar (en caso de ganar porque
        el contrario se retirarse puede mostrar o no mostrar las cartas)]
        @rtype: String
        '''
        pass
        
