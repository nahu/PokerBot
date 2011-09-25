# -*- coding: utf-8 -*-
'''
Creado el 23/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

import Jugador
from copy import deepcopy

class Bot(Jugador):
    '''
    El bot extiende de un jugador, redefine los métodos del mismo
    '''
    
    def __init__(self, identificador, fichas, nombre = None, bot = False):
        '''
        Constructor del Bot

        '''
        pass
    
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
    
        
    def calcular_odds(self, ronda, comunitarias):
        cartas_restantes = [50, 47, 46, 45]
        odds={"carta alta":None,"par":None, "doble par":None, "trio":None, "escalera interna":None, "escalera abierta":None, 
              "color":None, "full":None, "poker":None}
        numero,colores = self.hanEval.gobysificar(self.mano, comunitarias)
        
        if self.tiene_carta_alta():
            odds["carta alta"]=0
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++  
        tipo, jugada = self.handEval.comprobar_par(numero,colores)
          
        if tipo: #tiene par
            odds["trio"] = (2/cartas_restantes[ronda])-1
            odds["doble par"]= (3/cartas_restantes[ronda])-1
            odds["par"]=0
        else: #no tiene par
            odds["par"] = (6/cartas_restantes[ronda])-1
             
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++  
        tipo, jugada = self.handEval.comprobar_doble_par(numero,colores)
        if tipo:
            #tiene doble par
            odds["doble par"]=0
            odds["full"]= (4/cartas_restantes[ronda])-1
            
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tipo, jugada = self.handEval.comprobar_trio(numero,colores)
        if tipo:
            #tiene trio
            odds["trio"]= 0
            odds["full"]=(3/cartas_restantes[ronda])-1
            odds["poker"] = (1/cartas_restantes[ronda])-1
            
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tipo, jugada = self.handEval.comprobar_escalera(numero,colores)
        if tipo: #tiene Escalera
                odds["escalera abierta"]=0
                odds["escalera interna"]=0     
        else:#no tiene escalera
            if self.handEval.posible_escalera_abierta(numero,colores):
                odds["escalera abierta"]= (8/cartas_restantes[ronda])-1
            else:
                if self.handEval.posible_escalera_interna(numero,colores):
                    odds["escalera interna"] = (4/cartas_restantes[ronda])-1
                    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tipo,jugada = self.handEval.comprobar_color(numero,colores)
        
        if tipo:
            #tiene color
            odds["color"]= 0
        else:
            if self.handEval.posible_color(numero,colores):
                odds["color"]= (9/cartas_restantes[ronda])-1
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++               
        tipo,jugada = self.handEval.comprobar_full(numero, colores)
        if tipo:
            odds["full"]=0
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tipo, jugada = self.handEval.comprobar_poker(numero,colores)
        if tipo:
            odds["poker"]=0    
                    
            
                    
                        
                    
                    
                
        
        
#    def tiene_par(self, comunitarias):
#        i=0  
#        for carta in comunitarias:
#            if (self.mano[0][0] == carta[0]):
#                i++
#            if (self.mano[1][0]== carta[0]):
#                i++
#        return i
#
#            for j in range(i,4):
#                if comunitarias[j]!= "None":
#                    if(carta[0] == comunitarias[j][0])
#                        return True
                
    def tiene_carta_alta(self):
        if self.mano[0][0]== "7" or self.mano[0][0]=="8" or self.mano[0][0]=="9" \
        or self.mano[0][0]=="10"or self.mano[0][0]=="j" or self.mano[0][0]=="q" \
        or self.mano[0][0]=="k" or self.mano[0][0]=="1":
            return True
        return False
    
    def tiene_par_en_mano(self):
        if self.mano[0][0] == self.mano[0][0] :
            return True
        return False
        
        
        
#    def tiene_carta_alta(self):
#        if self.mano[1].find("j")!=-1 or self.mano[1].find("q")!=-1 \
#        or self.mano[1].find("k")!=-1 or self.mano[1].find("1")!=-1 :
#            return True 
#        
#        if self.mano[1].find("j")!=-1 or self.mano[1].find("q")!=-1 \
#        or self.mano[1].find("k")!=-1 or self.mano[1].find("1")!=-1 :
#            return True
        
    
