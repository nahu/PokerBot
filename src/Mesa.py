# -*- coding: utf-8 -*-
'''
Creado el 23/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''
import Mazo.Mazo
import Jugador.Jugador
import Cerebro.Cerebro
import HandEvaluator.HandEvaluator
import Ronda.Ronda

class Mesa(object):
    '''
    Manejadora del juego
    
    the person with the dealer button posts the small blind, 
    while his/her opponent places the big blind.
    The dealer acts first before the flop. After the flop, 
    the dealer acts last and continues to do so for the remainder of the hand.
    '''


    def __init__(self, ciega, jugadores):
        '''
        Constructor
        p es un número entre 0 y 1 para determinar la estrategia de juego del bot
        '''
        self.ciega = ciega
        self.mazo = Mazo()
        self.bote = 0
        self.jugadores = jugadores
        self.dealer = 0 #posicion en la lista jugaores
        self.comunitarias = [None, None, None, None, None]
        self.ronda_actual = None
        self.nro_jugadores = 2
        self.jugador_actual = 0
        self.allin = False
        
    def juego(self):
        '''
        Devuelve el resultado de juego en una lista
        la primera posición es True si el juego continúa
        la segunda es la posición en la lista de jugadores de la mesa
        del jugador que ganó esta iteración del juego y la 
        tercera posición indica el nombre de la jugada 
        ganadora.
        '''         
            
        for tipo in range(1,5): #iterador de rondas
            self.ronda(tipo)
            
    
    
    def ronda(self, tipo_ronda):
        if tipo_ronda == 1: #pre-flop, juega primero el dealer, tiene la ciega chica
            self.poner_ciegas()
            self.croupier(tipo_ronda) #acciones del croupier
            
            for nro_apuesta in range(0, 4):
                for i in range(0, self.nro_jugadores):
                    if not self.allin:
                        ronda = Ronda(tipo_ronda, nro_apuesta, self.ciega, self.bote)
                        nro_jugador = self.siguiente_jugador()
                        jugada = self.jugadores[nro_jugador].obtener_jugada(ronda, self.comunitarias)
                        self.actualizar_mesa(jugada, nro_apuesta, self.jugadores[nro_jugador].dealer)
                '''
                if not self.allin:
                    ronda = Ronda(tipo_ronda, nro_apuesta, self.ciega, self.bote)
                    jugada = self.jugadores[self.dealer].obtener_jugada(ronda, self.comunitarias)
                    self.actualizar_mesa(jugada, nro_apuesta, self.jugadores[self.dealer])
                    if not self.allin:
                        jugada = self.jugadores[self.obtener_no_dealer()].obtener_jugada(ronda, self.comunitarias)
                        self.actualizar_mesa(jugada, nro_apuesta, self.jugadores[self.dealer])
                '''
        
        elif tipo_ronda == 2:#flop, juega primero el que no es dealer.

        elif tipo_ronda == 3:#turn, juega primero el que no es dealer.
            self.croupier(tipo_ronda)
            
        elif tipo_ronda == 4:#river, juega primero el que no es dealer.
            self.croupier(tipo_ronda) 
    
    def actualizar_mesa(self, jugada, nro_apuesta, dealer):
        if jugada == "apostar":
            
    def siguiente_jugador(self):
        retorno = self.jugador_actual
        if self.jugador_actual == self.dealer:
            self.jugador_actual =  self.obtener_no_dealer()
        else:
            self.jugador_actual = self.dealer
        return retorno
          
    def poner_ciegas(self):
        self.bote = 0
        #el dealer pone la ciega chica.
        if self.jugadores[self.dealer].verficar_allin():
            self.establecer_allin(self.dealer)
        else:
            self.jugadores[self.dealer].fichas -= self.ciega / 2
        #el otro pone la ciega grande.
        if self.jugadores[self.obtener_no_dealer()].verficar_allin():
            self.establecer_allin(self.obtener_no_dealer())
        else:
            self.jugadores[self.obtener_no_dealer()].fichas -= self.ciega
 
    def establecer_allin(self, jugador):
        self.allin = True   
        self.bote += self.jugadores[jugador].fichas
        self.jugadores[jugador].fichas = 0
            
    def establecer_siguiente_dealer(self):
        if self.dealer == 0:
            self.dealer = 1
        else:
            self.dealer = 0
    
    def obtener_no_dealer(self):
        if self.dealer == 0:
            return 1
        else:
            return 0  
                
    def croupier(self, tipo_ronda):
        if tipo_ronda == 1: #pre-flop, repartir dos cartas a cada jugador
            self.mazo.mezclar()
            for i in range(0, self.nro_jugadores):
                for jug in self.jugadores:
                    self.jugadores[jug].mano[i] = self.mazo.obtener_siguiente()
        elif tipo_ronda == 2:#flop
            for i in range(0, 3):
                self.comunitarias[i] = self.mazo.obtener_siguiente()
                elif tipo_ronda == 3:#turn
            self.comunitarias[3] = self.mazo.obtener_siguiente()
        elif tipo_ronda == 4:#river
            self.comunitarias[4] = self.mazo.obtener_siguiente()
        
        

        