# -*- coding: utf-8 -*-
'''
Creado el 23/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''
from Mazo import *
from HandEvaluator import HandEvaluator
from Ronda import Ronda

class Mesa(object):
    '''
    Manejadora del juego
    
    the person with the dealer button posts the small blind, 
    while his/her opponent places the big blind.
    The dealer acts first before the flop. After the flop, 
    the dealer acts last and continues to do so for the remainder of the hand.
    '''


    def __init__(self, ciega, jugadores, lock):
        '''
        Constructor
        p es un número entre 0 y 1 para determinar la estrategia de juego del bot
        '''
        self.ciega = ciega
        self.mazo = Mazo()
        self.bote = 0
        self.jugadores = jugadores
        self.dealer = 1 #posicion en la lista jugaores
        self.comunitarias = []#[False, False, False, False, False]
        self.ronda_actual = None
        self.nro_jugadores = 2
        self.jugador_actual = 0
        self.allin = False
        self.dibujar = False
        self.se_fue = False
        self.resultado = None #si es distinto de None, tiene el resultado del juego
        self.lock = lock
    
    def inicializar_mesa(self):
        self.bote = 0
        self.comunitarias = []
        self.allin = False
        self.dibujar = False
        self.se_fue = False
        self.resultado = None #si es distinto de None, tiene el resultado del juego
        self.dealer = self.obtener_no_dealer()#se cambia el dealer para la siguiente ronda
        self.jugadores[self.dealer].dealer = True
        self.jugadores[self.obtener_no_dealer()].dealer = False
        for j in self.jugadores:
            j.cerar_apuesta()
#        print "Fondo Jugadores: "
#        print self.jugadores[0].nombre, self.jugadores[0].fichas
#        print self.jugadores[1].nombre, self.jugadores[1].fichas 
      
    def set_dibujar(self):
        self.lock.acquire()
        self.dibujar = True
        self.lock.release()

    def set_dibujado(self):
        self.lock.acquire()
        self.dibujar = False
        self.lock.release()
        
    def esperar_dibujo(self):
        while True:
            if not self.dibujar:
                break
            

    #def imprimir(self):
        #print "bote: ",  self.bote
        #for j in self.jugadores:
            #print "Jugador :"
            #j.imprimir()

            

        #print "posicion dealer: ",  self.dealer
        #print "comunitarias: ", self.comunitarias
        #print "ronda actual:"
        #self.ronda_actual.imprimir()
        #print "jugador actual: ", self.jugador_actual
        #print "es allin: ", self.allin

    def juego(self):
        '''
        Devuelve el resultado de juego en una lista
        la primera posición es True si el juego continúa
        la segunda es la posición en la lista de jugadores de la mesa
        del jugador que ganó esta iteración del juego y la 
        tercera posición indica el nombre de la jugada 
        ganadora.
        '''
        self.inicializar_mesa()
        
        #solucionar evaluar allin de poner_ciegas
        self.poner_ciegas()
        self.jugador_actual = self.dealer
        
        #si es un bot vuelve a recalcular la estrategia
        for jug in self.jugadores:
            if jug.bot:
                jug.inicializar_estrategia()
                
        
        for tipo in range(1,5): #iterador de rondas
            self.croupier(tipo) #acciones del croupier, repartir manos y colocar comunitaria
            self.ronda_actual = Ronda(tipo, 1, self.ciega, self.bote)
            if tipo > 1:
                for j in self.jugadores:
                    j.cerar_apuesta()
                
            self.set_dibujar()
            self.esperar_dibujo()
            if not self.allin:
                resultado_ronda = self.ronda(tipo) #resulatado continuas, fin_ronda o fin_juego
                if resultado_ronda == "fin_juego":
                    break
                
            self.jugador_actual = self.obtener_no_dealer()#después del pre-flop el que juega primero es el que no es dealer
        
        if self.se_fue:
            if self.jugador_actual == 0: #es jugador actual es cero y se fue y el otro es ganador
                ganador = 1
            else:
                ganador = 0
                
            self.jugadores[ganador].fichas += self.bote
            self.resultado = [True, ganador, "Jugador Retirado"]
            self.set_dibujar()
            self.esperar_dibujo()
            return [True, ganador, "Jugador Retirado"]
        
        
        return self.evaluar_ganador()
        
    def evaluar_ganador(self):
        #self.hand_eval.evaluar(jugador1, jugador2) obtiene el nombre de la jugada ganadora y el ganador
        #verificar si termina el juego si alguno de los jugadores se quedo sin ficha
        #armar la lista resultado de self.juego()
        '''HandEvaluator().ganador(comunitarias, mano1, mano2)
           jugador: Jugador 1 , Jugador 2, empate
           nombre de la jugada: 
           jugada: [], None'''
        #jugador, nombre_jugada, cartas = HandEvaluator().ganador(self.comunitarias, self.jugadores[0].mano, self.jugadores[1].mano)

        jugador, nombre_jugada, cartas = HandEvaluator().ganador(self.comunitarias, self.jugadores[0].mano, self.jugadores[1].mano)
        

        if cartas:
            print "cartas de la jugada: ", cartas
        
        print "cartas de la jugada: ", cartas

        gana = None
        if jugador == "Jugador1" :
            gana = 0
        
        if jugador == "Jugador2" :
            gana = 1
        
        
        
        if gana == None: #empate
            for j in self.jugadores:
                j.fichas =+ self.bote//2
        else:   
            self.jugadores[gana].fichas += self.bote
        
        continua_juego = True 
        if self.jugadores[0].fichas == 0 or self.jugadores[1].fichas == 0:
            continua_juego = False
        
        self.resultado = [continua_juego, gana, nombre_jugada]
        
        if not gana: #empate
            for j in self.jugadores:
                j.fichas =+ self.bote//2
        else:   
            self.jugadores[gana].fichas += self.bote
            
        self.set_dibujar()
        self.esperar_dibujo()    

        return self.resultado

            
            
    
    def ronda(self, tipo_ronda):
        #retorna si se continúa o no con la siguiente ronda
        resultado = "continuar"
        if tipo_ronda == 4:
            resultado = "fin_juego" #por defecto
            
#        self.jugadores[self.dealer].mano[0] = "9c"
#        self.jugadores[self.dealer].mano[1] = "9d"
        #print "Ronda ", tipo_ronda
            
        c = 0
        while True:
            for i in range(0, self.nro_jugadores):
                #print "-----> iteracion ", c
                #self.imprimir()
                if not self.allin:
                    self.ronda_actual.pot = self.bote
                    jugada = self.jugadores[self.jugador_actual].obtener_jugada(self.ronda_actual, self.comunitarias)
                    self.set_dibujar()
                    self.esperar_dibujo()
                    resultado = self.evaluar_accion(jugada, self.jugador_actual)
                    if resultado != "continuar":
                        break

                self.siguiente_jugador()
                c += 1
                
            if resultado != "continuar" or self.allin:
                break
                
        return resultado
    
    def evaluar_accion(self, jugada, jugador): 
        #se calcula que se debe hacer a partir de lo que devuelve el jugador actual
        #(acciones posibles devueltas son "apostar", "igualar" o "no_ir"
        #retorna true si terminó la ronda, false
        #igualar: si las apuestas ya estan iguales, equivale a un "pasar"
        #actualizar la apuesta del jugador y la mesa!!!!
        #descontar al jugador!
        #si fin apuestas de la ronda > fin_ronda
        #si no_ir > fin_juego
        #si igualan las apuestas y se pasa > fin_ronda
        #print "JUGADA: ", jugada        
        if jugada=="no_ir":
            print "+++++++accion: se fue"
            self.se_fue = True

            return "fin_juego"
        accion = ''
        #PRE FLOP
        if self.ronda_actual.tipo == 1:
            accion = self.pre_flop(jugada, jugador)
        if self.ronda_actual.tipo == 2:
            accion = self.otras_rondas(jugada, self.ciega, jugador)
        if self.ronda_actual.tipo == 3:
            accion = self.otras_rondas(jugada, self.ciega*2, jugador)
        if self.ronda_actual.tipo == 4:
            accion = self.otras_rondas(jugada, self.ciega*2, jugador)

        return accion
    '''
    def set_nro_apuesta(self, ciega):
        apuesta1 = self.jugadores[0].apuesta_actual
        apuesta2 = self.jugadores[1].apuesta_actual
        
        if apuesta1 > apuesta2:
            mayor = apuesta1
        else:
            mayor = apuesta2
            
        if mayor < ciega*2:
            self.ronda_actual.nro_apuesta = 1
        if mayor < ciega*3:
            self.ronda_actual.nro_apuesta = 2
        if mayor < ciega*4:
            self.ronda_actual.nro_apuesta = 3
        if mayor >= ciega*4:
            self.ronda_actual.nro_apuesta = 4
    '''
                    
    def pre_flop(self, jugada, jugador):
        if self.jugadores[jugador].dealer:
            if jugada=="igualar":
                print "igualar preflop dealer"
                if self.jugadores[jugador].apuesta_actual == self.ciega/2:
                    self.jugadores[jugador].completar_ciega(self.ciega)
                    self.bote+=self.ciega/2
                    self.ronda_actual.pot = self.bote
                else:
                    monto = self.jugadores[self.obtener_no_dealer()].apuesta_actual
                    #print self.jugadores

                    print "dealer / igualar: ", monto

                    apuesta, allin =self.jugadores[jugador].igualar(monto)

                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    if allin:
                        if self.jugadores[self.obtener_no_dealer()].allin:
                            self.allin = True
                            return "fin_ronda"
                        
                return "continuar"
            
            if jugada=="apostar":
                if self.jugadores[jugador].apuesta_actual == self.ciega/2:
                    print "QUIERE APOSTAR1"
                    apuesta, allin = self.jugadores[jugador].subir_apuesta(self.ciega*1.5)
                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    self.ronda_actual.nro_apuesta = 2
#                    if not allin:
#                        return "fin_ronda"                   
                    return "continuar"                
                else:
                    print "QUIERE APOSTAR2"
                    #dif = self.jugadores[jugador].apuesta_actual - self.jugadores[self.obtener_contrario(True)].apuesta_actual
                    
                    
                    monto = self.jugadores[self.obtener_no_dealer()].apuesta_actual
                    apuesta, allin = self.jugadores[jugador].igualar(monto)                    
                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    if self.jugadores[self.obtener_no_dealer()].allin:#el otro pibe esta en allin y solo puedo igualar
                        self.allin = True
                        return "fin_ronda"
                    
                    elif self.ronda_actual.nro_apuesta < 4:
                        print "QUIERE APOSTAR3"
                        apuesta, allin = self.jugadores[jugador].subir_apuesta(self.ciega)                      
                        self.bote += apuesta
                        self.ronda_actual.pot = self.bote
                        self.ronda_actual.nro_apuesta += 1
#                        if allin:
#                            return "fin_ronda"
                        return "continuar"
                        
#                    if allin:
#                        return "fin_ronda"
                    
#                    if monto >= self.ciega*4:
#                        return "fin_ronda"
                    print "LLEGA ACA SI IGUALA UN ALLIN EN EL PREFLOP"
                    return "continuar"
        else: #NO ES DEALER
            print "no es dealer"
            contrario = self.dealer
            monto = self.jugadores[contrario].apuesta_actual
            if jugada=="igualar":

                if self.jugadores[contrario].allin:#el contrario esta en all in y tenemos que igualarlo

                    print "Apuestas diferentes"
                    apuesta, allin = self.jugadores[jugador].igualar(monto)
                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    self.allin = True
                    return "fin_ronda"
#                    
#                    if self.allin:
#                        return "fin_ronda"

                else:
                    apuesta, allin = self.jugadores[jugador].igualar(monto)
                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    if allin:
                        dif = self.jugadores[contrario].apuesta_actual - self.jugadores[jugador].apuesta_actual #esto se tiene que devolver a sus fichas porque mi allin no alcanza para hacer iguales las apuestas actuales
                        self.jugadores[contrario].fichas += dif
                        self.jugadores[contrario].apuesta_actual -= dif
                        self.bote -= dif
                        self.ronda_actual.pot -= dif
                        self.allin = True
                        return "fin_ronda"
                    if apuesta == 0:#juega ultimo y paso
                        return "fin_ronda"

                    return "fin_ronda"
                
                
            if jugada=="apostar":#preflop no dealer
                print "no dealer / apostar"
                apuesta, allin = self.jugadores[jugador].igualar(monto)
                self.bote += apuesta
                self.ronda_actual.pot = self.bote
                if self.jugadores[self.dealer].allin:
                    #hasta aca llegamos
                    self.allin = True
                    return "fin_ronda"
                
                if allin: #mirar, pero vane tiene razon
                    #si al igualar me quedo en allin, soy el ultimo y se le devuelve
                    dif = self.jugadores[contrario].apuesta_actual - self.jugadores[jugador].apuesta_actual #esto se tiene que devolver a sus fichas porque mi allin no alcanza para hacer iguales las apuestas actuales
                    self.jugadores[contrario].fichas += dif
                    self.jugadores[contrario].apuesta_actual -= dif
                    self.bote -= dif
                    self.ronda_actual.pot -= dif
                    self.allin = True
                    return "fin_ronda"

                
                if self.ronda_actual.nro_apuesta < 4:
                    print "apostar/no dealer/ No ha llegado al limite"
                    apuesta, allin = self.jugadores[jugador].subir_apuesta(self.ciega)
                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    self.ronda_actual.nro_apuesta += 1
#                    if allin:
#                        return "fin_ronda"

                    return "continuar"
                
                print "========aca no======"
                return "fin_ronda"

    def otras_rondas(self, jugada, ciega_minima, jugador): 
        if self.jugadores[jugador].dealer:#es dealer y actua ultimo
            print "es dealer en otras rondas"
            contrario = self.obtener_no_dealer()
            monto = self.jugadores[contrario].apuesta_actual
            if jugada=="igualar":
                if self.jugadores[contrario].allin:#el contrario esta en all in y tenemos que igualarlo
                    print "Apuestas diferentes"
                    apuesta, allin = self.jugadores[jugador].igualar(monto)
                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    self.allin = True
                    return "fin_ronda"

                else:
                    apuesta, allin = self.jugadores[jugador].igualar(monto)
                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    if allin:
                        dif = self.jugadores[contrario].apuesta_actual - self.jugadores[jugador].apuesta_actual #esto se tiene que devolver a sus fichas porque mi allin no alcanza para hacer iguales las apuestas actuales
                        self.jugadores[contrario].fichas += dif
                        self.jugadores[contrario].apuesta_actual -= dif
                        self.bote -= dif
                        self.ronda_actual.pot -= dif
                        self.allin = True
                        return "fin_ronda"
                    
                    if apuesta == 0:#juega ultimo y paso
                        return "fin_ronda"
                
                    return "fin_ronda"
                
            if jugada=="apostar":#dealer apostar
                print "es dealer / apostar / otras rondas"
                apuesta, allin = self.jugadores[jugador].igualar(monto)
                self.bote += apuesta
                self.ronda_actual.pot = self.bote
                if self.jugadores[contrario].allin:
                    #hasta aca llegamos
                    self.allin = True
                    return "fin_ronda"
                
                if allin:
                    #si al igualar me quedo en allin, soy el ultimo y se le devuelve
                    dif = self.jugadores[contrario].apuesta_actual - self.jugadores[jugador].apuesta_actual #esto se tiene que devolver a sus fichas porque mi allin no alcanza para hacer iguales las apuestas actuales
                    self.jugadores[contrario].fichas += dif
                    self.jugadores[contrario].apuesta_actual -= dif
                    self.bote -= dif
                    self.ronda_actual.pot -= dif
                    self.allin = True
                    return "fin_ronda"
                
                if self.ronda_actual.nro_apuesta < 4:
                    print "apostar/no dealer/ No ha llegado al limite"
                    apuesta, allin = self.jugadores[jugador].subir_apuesta(self.ciega)
                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    self.ronda_actual.nro_apuesta += 1
#                    if allin:
#                        return "fin_ronda"

                    return "continuar"
                
                print "========aca no======"
                return "fin_ronda"
            
        else: #no es dealer y actua primero
            contrario = self.dealer
            if jugada=="igualar":
                print "igualar otras rondas dealer"

                monto = self.jugadores[contrario].apuesta_actual
                print "no dealer / igualar: ", monto
                apuesta, allin =self.jugadores[jugador].igualar(monto)
                self.bote += apuesta
                self.ronda_actual.pot = self.bote
                if allin:
                    if self.jugadores[contrario].allin:
                        self.allin = True
                        return "fin_ronda"
                        
                return "continuar"
            
            if jugada=="apostar":
              
                print "QUIERE APOSTAR2 otras rondas"
                #dif = self.jugadores[jugador].apuesta_actual - self.jugadores[self.obtener_contrario(True)].apuesta_actual
                
                
                monto = self.jugadores[contrario].apuesta_actual
                apuesta, allin = self.jugadores[jugador].igualar(monto)                    
                self.bote += apuesta
                self.ronda_actual.pot = self.bote
                if self.jugadores[contrario].allin:#el otro pibe esta en allin y solo puedo igualar
                    self.allin = True
                    return "fin_ronda"
                
                elif self.ronda_actual.nro_apuesta < 4:
                    print "QUIERE APOSTAR3 enn otras rondas"
                    apuesta, allin = self.jugadores[jugador].subir_apuesta(self.ciega)                      
                    self.bote += apuesta
                    self.ronda_actual.pot = self.bote
                    self.ronda_actual.nro_apuesta += 1
#                        if allin:
#                            return "fin_ronda"
                    return "continuar"

                print "LLEGA ACA SI IGUALA UN ALLIN EN otras rondas"
                return "continuar"
          
            
            
    '''            
    def otras_rondas(self, jugada, ciega_minima, jugador):        
        if jugada=="igualar":
            if self.apuestas_igualadas():
                if self.jugadores[jugador].dealer: #puede terminar la ronda
                    #print "+++++++accion: fin ronda - pasaron"
                    return "fin_ronda"
                else:
                    return "continuar"
            else:
                monto = self.jugadores[self.obtener_no_dealer()].apuesta_actual
                apuesta, self.allin =self.jugadores[jugador].igualar(monto) 
                self.bote += apuesta
                if self.allin:
                    return "fin_ronda"
                if self.jugadores[jugador].dealer and self.jugadores[jugador].apuesta_actual >= ciega_minima*4:
                    return "fin_ronda"
                return "continuar"
        if jugada=="apostar":
            contrario = self.obtener_contrario(jugador) 
            monto = self.jugadores[contrario].apuesta_actual
            
            apuesta, self.allin = self.jugadores[jugador].igualar(monto)
            self.bote += apuesta
            if self.allin:
                return "fin_ronda"
            if self.jugadores[contrario].apuesta_actual >= ciega_minima*4:
                return "fin_ronda"
            else:
                apuesta, self.allin = self.jugadores[jugador].subir_apuesta(ciega_minima)
                self.bote += apuesta
                if self.allin:
                    return "fin_ronda"
                return "continuar"
    '''        
                
    def apuestas_igualadas(self):
        if self.jugadores[0].apuesta_actual == self.jugadores[1].apuesta_actual:
            return True
        else:
            return False
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
        #print "BOTE INICIAL: ", self.bote
        #el dealer pone la ciega chica.
        if self.jugadores[self.dealer].verificar_allin(self.ciega/2):
            self.establecer_allin(self.dealer)
        else:
#            apuesta, self.allin = self.jugadores[self.dealer].subir_apuesta(self.ciega/2)
#            self.bote += apuesta
            self.jugadores[self.dealer].fichas -= (self.ciega / 2)
            self.jugadores[self.dealer].apuesta_actual = (self.ciega / 2)
            self.bote += (self.ciega / 2)
        #el otro pone la ciega grande.
        if self.jugadores[self.obtener_no_dealer()].verificar_allin(self.ciega):
            self.establecer_allin(self.obtener_no_dealer())
        else:
#            apuesta, self.allin = self.jugadores[self.obtener_no_dealer()].subir_apuesta(self.ciega)
#            self.bote += apuesta
            self.jugadores[self.obtener_no_dealer()].fichas -= (self.ciega)
            self.jugadores[self.obtener_no_dealer()].apuesta_actual = (self.ciega)
            self.bote += (self.ciega)
 
    def establecer_allin(self, jugador):
        self.allin = True   
        self.bote += self.jugadores[jugador].fichas
        self.jugadores[jugador].apuesta_actual = self.jugadores[jugador].fichas
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
                    jug.mano[i] = self.mazo.obtener_siguiente()
        elif tipo_ronda == 2:#flop
            for i in range(0, 3):
                self.comunitarias.append(self.mazo.obtener_siguiente())
        elif tipo_ronda == 3:#turn
            self.comunitarias.append(self.mazo.obtener_siguiente())
        elif tipo_ronda == 4:#river
            self.comunitarias.append(self.mazo.obtener_siguiente())
        
        

        
