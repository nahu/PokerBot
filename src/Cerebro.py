'''
Creado el Sep 25, 2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

import random

#'''
#para ordenar los odds:
#importancia de cada juego en cada mano,
#en la posición 0 en el juego.
#En la 1 preflop, 2-flop, etc...
#'''
#JUEGOS = {'carta alta' : [0, 8, 0, 0, 0],
#          'par' : [1, 9, 5, 4, 2, 1]
#          'doble par' : [2, 
#          'trio' : [3,
#          'escalera' : [4,
#          'escalera interna' : [4,
#          'escalera abierta' : [5,
#          'color' : [6,
#          'full' : [7,
#          'poker' : [8,
#          'escalera color' : 9
#          }


'''
valores de los juegos,
mientras más pequeño es el valor,
mejor es la jugada
'''

JUEGOS = {'carta alta' : 9,
          'par' : 8,
          'doble par' : 7, 
          'trio' : 6,
          'escalera' : 5,
          'escalera interna' : 5,
          'escalera abierta' : 5,
          'color' : 3,
          'full' : 2,
          'poker' : 1,
          'escalera color' : 0
          }

class Cerebro(object):
    '''
    Clase que ve que hacer según los tipos de estrategia
    '''

    def __init__(self, estrategia, limite_mentira = None):
        '''
        Constructor, la estrategia se determina
        como va a actuar el bot, puede ser un 
        número del 0 al 3
        '''
        self.mentir = 0
        self.odd = False
        
        #se elige una estrategia aleatoria
        if (estrategia == 0):
            estrategia = random.randint(1, 3)
            if (estrategia == 1):
                limite_mentira = random.randint(1, 4)
            
        if (estrategia == 1): #se elige una estragia mentirosa
            self.mentir = limite_mentira
            
        elif (estrategia == 2):#solo en base a odds
            self.odd = True
            
        elif (estrategia == 3):#mezclado
            self.odd = True
            self.mentir = limite_mentira
    
        
    def elegir_accion(self, mano, comunitarias, ronda, dict_odd, dealer): 
        '''
        Devuelve igualar, apostar o no ir
        la mesa decide que hacer según estas condiciones,
        si iguala y no puede igualar y tiene que apostar entonces noir
        si iguala y no puede igualar y no tiene que apostar entonces pasar
        si apuesta y no puede apostar entonces iguala
        si apuesta o iguala y el dinero no le alcanza hace all-in
        '''
        odd = self.seleccionar_odd(dict_odd) 
        if self.odd:
            if self.mentir:#mezclado
                if random.randint(0,1):
                    return self.jugar_con_odds(odd, dict_odd, mano, comunitarias, ronda, dealer)
                else:
                    return self.jugar_mintiendo(odd, ronda)
            else:#solo odds
                return self.jugar_con_odds(odd, dict_odd, mano, comunitarias, ronda, dealer)
                                
        elif self.mentir: #solo mentir
            return self.jugar_mintiendo(odd, ronda)      
                        
    
    def jugar_mintiendo(self, odd, ronda):
        if (ronda.nro_apuesta == 1): #en el preflop se apuesta hasta el nivel indicando sin importar la mano que tiene
            if (self.mentir > ronda.nro_apuesta):
                return "apostar"
            else:
                return "igualar"
        else:
            if len(odd) and odd[0][0] == 0: #continuamos mientiendo si por lo menos tenemos una carta alta
                if (self.mentir > ronda.nro_apuesta):
                    return "apostar"
                else:
                    return "igualar"
            else:
                return "no_ir"
            
    def jugar_con_odds(self, odd, dict_odd, mano, comunitarias, ronda, dealer):    
        #TODO     verificar que el juego (odd == 0) no sea de la mesa en el turn y en el river
            if ronda.tipo == 1: #pre-flop
                if dict_odd['carta alta'] == 0 and dict_odd['par'] == 0:
                    return "apostar"
                
                if dict_odd['par'] == 0: #un par alto o un par
                    if ronda.nro_apuesta < 2:
                        return "apostar"
                    else:
                        return "igualar"
                        
                if dict_odd['carta alta'] or len(odd): #algo en los odds de escalera o color
                    if ronda.nro_apuesta == 1:
                        return "igualar"
                    elif dict_odd['color'] and ronda.nro_apuesta >= 2:
                        return "igualar"
                    else:
                        return "no_ir"
                else:
                    return "no_ir"
                
            elif ronda.tipo == 2: #flop
                if len(odd): #se tiene algo en los odds  
                    for i in odd:
                        if odd[i][1] <= 5: 
                            if odd[i][0] == 0:#se tiene un juego formado y es bueno
                                return 'apostar'
                            else:
                                
                                dif = ronda.apuesta_de_ronda() - odd[i][0] * ronda.monto_a_igualar(dealer)
    
                                if dif > 0:
                                    if ronda.monto_a_subir() > dif * 2:
                                    #si apuesto y me iguala y aún así sigo ganando algo según el odd
                                        if ronda.nro_apuesta <= 2:   
                                        #le subo hasta la 2da ronda 
                                            return "apostar"
                                        else:
                                            return "igualar"
                                    else:
                                        return "igualar"
                                else:
                                    return "no_ir"
                        
                        elif odd[i][1] == 6 or odd[i][1] == 7:#trío o escalera
                            if odd[i][1] == 0:#se tiene ese juego
                                if ronda.nro_apuesta <= 2:
                                    return "apostar"
                                else:
                                    return "igualar"
                            else: #no se tiene ese juego
                                dif = ronda.apuesta_de_ronda() - odd[i][0] * ronda.monto_a_igualar(dealer)
                                if (dif > 0):
                                    return "igualar"
                                else:
                                    return "no_ir"
                        elif odd[i][1] == 8:
                            if (mano[0][0] == mano[1][0]):#par en mano
                                return "igualar"
                return "no_ir"
  
            elif ronda.tipo == 3 or ronda.tipo == 4: #turn y river
                
                if len(odd): #se tiene algo en los odds  
                    for i in odd:
                        if odd[i][1] <= 5: 
                            if odd[i][0] == 0:#se tiene un juego formado y es bueno
                                return 'apostar'
                            else:
                                
                                dif = ronda.apuesta_de_ronda() - odd[i][0] * ronda.monto_a_igualar(dealer)
    
                                if dif > 0:
                                    if ronda.nro_apuesta <= 2:   
                                    #le subo hasta la 2da ronda
                                        return "apostar"
                                    else:
                                        return "igualar"
                                else:
                                    return "no_ir"
                        
                        elif odd[i][1] == 6 or odd[i][1] == 7:#trío o escalera
                            if odd[i][1] == 0:#se tiene ese juego
                                if ronda.nro_apuesta <= 2:
                                    return "apostar"
                                else:
                                    return "igualar"
                            else: #no se tiene ese juego
                                dif = ronda.apuesta_de_ronda() - odd[i][0] * ronda.monto_a_igualar(dealer)
                                if (dif > 0):
                                    return "igualar"
                                else:
                                    return "no_ir"
                        elif odd[i][1] == 8:
                            if (mano[0][0] == mano[1][0]):#par en mano
                                return "igualar"
                return "no_ir"
            
            return "no_ir"   
    
    def seleccionar_odd(self, dict_odd):
        '''
        selecciona odd con valores seteados y los 
        ordena de menor a mayor por valor del odd en la primera
        poscición y por el valor de la jugada en la segunda.
        '''
        buenos_odds = []
        for i in dict_odd.keys():
            if dict_odd[i]:
                buenos_odds.append([dict_odd[i], JUEGOS[i], i])
        buenos_odds.sort()
        return buenos_odds        
        
                       
            
            
            
        
        
        