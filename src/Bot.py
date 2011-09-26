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
        
        if ronda.tipo == 1:#solo en el pre-flop
            tipo = self.tiene_cartas_consecutivas()
            if tipo:
                    odds["escalera interna"] = (12/cartas_restantes[ronda.tipo])-1
                    odds["escalera abierta"] = (12/cartas_restantes[ronda.tipo])-1
            if self.tiene_cartas_del_mismo_color():
                    odds["color"]=(11/cartas_restantes[ronda.tipo])-1
            
        
        if self.tiene_carta_alta():
            odds["carta alta"]=0
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++  
        tipo, jugada = self.handEval.comprobar_par(numero,colores)
          
        if tipo: #tiene par
            odds["trio"] = (2/cartas_restantes[ronda.tipo])-1
            odds["doble par"]= (3/cartas_restantes[ronda.tipo])-1
            odds["par"]=0
        else: #no tiene par
            odds["par"] = (6/cartas_restantes[ronda.tipo])-1
             
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++  
        tipo, jugada = self.handEval.comprobar_doble_par(numero,colores)
        if tipo:
            #tiene doble par
            odds["doble par"]=0
            odds["full"]= (4/cartas_restantes[ronda.tipo])-1
            
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tipo, jugada = self.handEval.comprobar_trio(numero,colores)
        if tipo:
            #tiene trio
            odds["trio"]= 0
            odds["full"]=(cartas_restantes[ronda.tipo]/3)-1
            odds["poker"] = (cartas_restantes[ronda.tipo]/1)-1
            
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tipo, jugada = self.handEval.comprobar_escalera(numero,colores)
        if tipo: #tiene Escalera
                odds["escalera abierta"]=0
                odds["escalera interna"]=0     
        else:#no tiene escalera
            if self.handEval.posible_escalera_abierta(numero,colores):
                odds["escalera abierta"]= (8/cartas_restantes[ronda.tipo])-1
            else:
                if self.handEval.posible_escalera_interna(numero,colores):
                    odds["escalera interna"] = (4/cartas_restantes[ronda.tipo])-1
                    
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tipo,jugada = self.handEval.comprobar_color(numero,colores)
        
        if tipo:
            #tiene color
            odds["color"]= 0
        else:
            if self.handEval.posible_color(numero,colores):
                odds["color"]= (9/cartas_restantes[ronda.tipo])-1
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++               
        tipo,jugada = self.handEval.comprobar_full(numero, colores)
        if tipo:
            odds["full"]=0
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        tipo, jugada = self.handEval.comprobar_poker(numero,colores)
        if tipo:
            odds["poker"]=0    
       
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++
        if (odds["escalera interna"]==0 or odds["escalera abierta"]==0) and odds["color"]==0:
            odds["escalera color"]=0
             
        return odds 
                    
                        
                    
    def tiene_cartas_consecutivas(self):
        cartas={"1":1, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "d":10, "j":11, "q":12, "k":13}
        
        carta1 = self.mano[0][0]
        carta2 = self.mano[1][0]
        r = cartas[carta1]-cartas[carta2]
        if r==1 or r==-1 or r== 12:
            return True
        return False
    
    def tiene_cartas_del_mismo_color(self):
        if self.mano[0][1] == self.mano[1][0]:
            return True
        return False
    
    def tiene_carta_alta(self):
        if self.mano[0][0]== "7" or self.mano[0][0]=="8" or self.mano[0][0]=="9" \
        or self.mano[0][0]=="d"or self.mano[0][0]=="j" or self.mano[0][0]=="q" \
        or self.mano[0][0]=="k" or self.mano[0][0]=="1":
            return True
        return False
    
    def tiene_par_en_mano(self):
        if self.mano[0][0] == self.mano[0][0] :
            return True
        return False
        
        
    
