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
import Jugador
import Cerebro
import HandEvaluator
import Ronda

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
        self.paso = 0
        
    def juego(self):
        '''
        Devuelve el resultado de juego en una lista
        la primera posición es True si el juego continúa
        la segunda es la posición en la lista de jugadores de la mesa
        del jugador que ganó esta iteración del juego y la 
        tercera posición indica el nombre de la jugada 
        ganadora.
        '''
        self.poner_ciegas()
        self.jugador_actual = self.dealer
        
        for tipo in range(1,5): #iterador de rondas
            self.croupier(tipo) #acciones del croupier, repartir manos y colocar comunitarias
            if not self.allin:
                resultado_ronda = self.ronda(tipo)
                if resultado_ronda == "fin_juego":
                    break
                
            self.jugador_actual = self.obtener_no_dealer()#después del pre-flop el que juega primero es el que no es dealer
        
        self.dealer = self.obtener_no_dealer()
        
        return self.evaluar_ganador()
        
    def evaluar_ganador(self):
        #self.hand_eval.evaluar(jugador1, jugador2) obtiene el nombre de la jugada ganadora y el ganador
        #verificar si termina el juego
        #armar la lista resultado de self.juego()
        pass    
    
    def ronda(self, tipo_ronda):
        #retorna si se continúa o no con la siguiente ronda
        resultado = "continuar"
        for nro_apuesta in range(0, 4):
            for i in range(0, self.nro_jugadores):
                if not self.allin:
                    ronda = Ronda(tipo_ronda, nro_apuesta, self.ciega, self.bote)
                    self.ronda_actual = ronda
                    jugada = self.jugadores[self.jugador_actual].obtener_jugada(ronda, self.comunitarias)
                    resultado = self.evaluar_accion(jugada, nro_apuesta, self.jugadores[self.jugador_actual])
                    if resultado != "continuar":
                        break

                self.siguiente_jugador()
            if resultado != "continuar" or self.allin:
                break
                
        return resultado
    
    
    def evaluar_accion(self, jugada, nro_apuesta, jugador): 
        #se calcula que se debe hacer a partir de lo que devuelve el jugador actual
        #(acciones posibles devueltas son "apostar", "igualar" o "no_ir"
        #retorna true si terminó la ronda, false
        if jugada == "no_ir":
            self.no_ir(jugador)
            return "fin_juego"
        elif jugada == "igualar":
            return "fin_ronda"
        elif jugada == "apostar":
            return "continuar"
        
            
            
    def no_ir(self, jugador):
        ganador = self.jugadores[self.obtener_contrario(jugador.dealer)]
        ganador.fichas += self.bote
        
        
            
    def siguiente_jugador(self):
        if self.jugador_actual == self.dealer:
            self.jugador_actual =  self.obtener_no_dealer()
        else:
            self.jugador_actual = self.dealer
          
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
    
    def obtener_contrario(self, dealer):
        if dealer:
            return self.dealer
        else:
            return self.obtener_no_dealer()
                   
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
        
        

        