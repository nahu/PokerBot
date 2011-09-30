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
    def __init__(self, identificador, fichas, nombre, lock = None):
        '''
        Constructor, se definen todos los atributos para la clase Jugador
        '''
        self.fichas = fichas
        self.id = identificador
        self.nombre = nombre
        self.mano = [None, None]
        self.bot = False
        self.apuesta_actual = 0
        self.dealer = False
        self.lock = lock
        self.jugada = None
        self.esperar = False
    
    def imprimir(self):
        ##print "   NOMBRE: ", self.nombre
        ##print "   fichas: ", self.fichas
        ##print "   mano: ", self.mano
        ##print "   es bot: ", self.bot
        ##print "   apuesta actual: ", self.apuesta_actual
        ##print "   es dealer: ", self.dealer
        pass
        
      
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
        self.lock.acquire()
        self.esperar = True
        self.lock.release()
        while True:
            if not self.esperar:
                break
        
        return self.jugada                    
            
    def definir_jugada(self, jugada):
        self.lock.acquire()
        self.jugada = jugada
        self.esperar = False
        self.lock.release()
        

    def completar_ciega(self, ciega):
        self.apuesta_actual +=ciega/2
        self.fichas -= ciega/2
    
    def subir_apuesta(self, monto):
        if (self.fichas > monto):
            self.fichas -= monto
            self.apuesta_actual += monto
            ##print "SUBIR / apuesta_nueva: " + str(monto)
            return (monto, False)
        else:
            apuesta=self.fichas
            self.apuesta_actual += apuesta
            self.fichas = 0
            ##print "SUBIR / apuesta_nueva: " + str(apuesta)
            return (apuesta, True)
        
    def igualar(self, total):
        ##print "igualar"
        monto = 0
        ###print "total: ", total
        ###print "apuesta actual", self.apuesta_actual
        if total>self.apuesta_actual:
            ###print "dentro"
            monto = total-self.apuesta_actual
            ###print "monto: ", monto 
            if (self.fichas > monto):
                self.fichas -= monto
                self.apuesta_actual += monto
                ###print "IGUALAR / apuesta_nueva: " + str(monto)
                return (monto, False)
            else:
                apuesta = self.fichas
                self.apuesta_actual += apuesta
                self.fichas = 0
                #####print "IGUALAR / all-in: " + str(apuesta)
                return (apuesta, True)
        if (self.apuesta_actual==total):
            return (0, False)
        else:
            return (0,False)

    def dibujar_botones(self):
        return self.esperar
        
    def cerar_apuesta(self):
        self.apuesta_actual = 0
           
