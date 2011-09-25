'''
Creado el Sep 25, 2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

import random

JUEGOS = {
          'par' : 1,
          'doble par' : 2,
          'trio' : 3,
          'escalera' : 4,
          'color' : 5,
          'full' : 6,
          'poker' : 7,
          'escalera interna' : 8,
          'escalera abierta' : 8,
          'escalera color' : 9
          }

class Cerebro(object):
    '''
    Clase que ve que hacer según los tipos de estrategia
    '''


    def __init__(self, estrategia):
        '''
        Constructor, la estrategia se determina
        como va a actuar el bot, puede ser un 
        número del 0 al 3
        '''
        self.mentir = False
        self.odd = False
        
        #se elige una estrategia aleatoria
        if (estrategia == 0):
            estrategia = random.randint(1, 3)
            
        if (estrategia == 1): #se elige una estragia mentirosa
            self.mentir = True
            
        elif (estrategia == 2):#solo en base a odds
            self.odd = True
            
        elif (estrategia == 3):#mezclado
            self.odd = True
            self.mentir = True
            
    def carta_alta(self, mano):
        if mano[0][0] in ['1', 'd', 'k', 'q', 'j']:
            return True
        else:
            return False
    
        
    def elegir_accion(self, mano, comunitarias, ronda, dict_odd): 
        if (self.odd and not self.mentir):
            odd = self.seleccionar_odd(dict_odd)
            if ronda.tipo == 1: #pre-flop
                if len(odd) > 0: #la mano no tiene esperanzas...
                    if (odd[0][0] == 0 and odd[1][0] == 0) or dict_odd['par'] == 0: #un par alto o un par
                        if ronda.nro_apuesta < 2:
                            return "apostar"
                        elif dict_odd["par"] == 0:
                            return "apostar"
                        else:
                            return "igualar"
                            
                    if odd[0][0] >= 0:
                        if ronda.nro_apuesta < 2:
                            return "igualar"
                        else:
                            return "no_ir"
                    else:
                        return "no_ir"
                else:
                    return "no_ir"
                
            elif ronda.tipo == 2: #flop
                
                      
                    dif = ronda.apuesta_de_ronda() - odd[0] * ronda.monto_a_igualar()
                    if dif > 0:
                        
                 
            
    
    def seleccionar_odd(self, dict):
        buenos_odds = []
        for i in dict.keys():
            if dict[i]:
                buenos_odds.append([dict[i], i])
        buenos_odds.sort()
        return buenos_odds        
        
                       
            
            
            
        
        
        