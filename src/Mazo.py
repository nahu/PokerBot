# -*- coding: utf-8 -*-
'''
Creado el 23/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

import random

'''    
    Configuren bien su editor a utf-8 para no tener problemas,
    si usan Eclipse, Window->preferences->general->workspace->text file encoding
    
    A, 2, 3, 4, 5, 6, 7, 8, 9, D, J, Q, K
    s = spades = picas
    h = hearts = corazones
    d = diamonds = diamantes
    c = clubs = tréboles 
'''

NOMBRES = {'1s' : 'As de picas',
          '2s' : 'Dos de picas',
          '3s' : 'Tres de picas',
          '4s' : 'Cuatro de picas',
          '5s' : 'Cinco de picas',
          '6s' : 'Seis de picas',
          '7s' : 'Siete de picas',
          '8s' : 'Ocho de picas',
          '9s' : 'Nueve de picas',
          'ds' : 'Diez de picas',
          'js' : 'Jack de picas',
          'qs' : 'Reina de picas',
          'ks' : 'Rey de picas',
          
          '1h' : 'As de corazones',
          '2h' : 'Dos de corazones',
          '3h' : 'Tres de corazones',
          '4h' : 'Cuatro de corazones',
          '5h' : 'Cinco de corazones',
          '6h' : 'Seis de corazones',
          '7h' : 'Siete de corazones',
          '8h' : 'Ocho de corazones',
          '9h' : 'Nueve de corazones',
          'dh' : 'Diez de corazones',
          'jh' : 'Jack de corazones',
          'qh' : 'Reina de corazones',
          'kh' : 'Rey de corazones',          
          
          '1d' : 'As de diamantes',
          '2d' : 'Dos de diamantes',
          '3d' : 'Tres de diamantes',
          '4d' : 'Cuatro de diamantes',
          '5d' : 'Cinco de diamantes',
          '6d' : 'Seis de diamantes',
          '7d' : 'Siete de diamantes',
          '8d' : 'Ocho de diamantes',
          '9d' : 'Nueve de diamantes',
          'dd' : 'Diez de diamantes',
          'jd' : 'Jack de diamantes',
          'qd' : 'Reina de diamantes',
          'kd' : 'Rey de diamantes',
          
          '1c' : 'As de tréboles',
          '2c' : 'Dos de tréboles',
          '3c' : 'Tres de tréboles',
          '4c' : 'Cuatro de tréboles',
          '5c' : 'Cinco de tréboles',
          '6c' : 'Seis de tréboles',
          '7c' : 'Siete de tréboles',
          '8c' : 'Ocho de tréboles',
          '9c' : 'Nueve de tréboles',
          'dc' : 'Diez de tréboles',
          'jc' : 'Jack de tréboles',
          'qc' : 'Reina de tréboles',
          'kc' : 'Rey de tréboles'
          }
class Mazo(object):
    '''
    Clase que represente el mazo de cartas
    '''

    def __init__(self):
        '''
        Constructor
        obtienes las claves del diccionario como una lista
        el indice es seteado a -1
        '''
        self.cartas = NOMBRES.keys()
        self.indice = -1
        
    def mezclar(self):
        '''
        Mezcla las cartas
        '''
        random.shuffle(self.cartas)
        self.indice = -1
        
    def obtener_siguiente(self):
        self.indice += 1
        return self.cartas[self.indice]

#m = Mazo()   
#for i in range(0, 3):
#    print m.obtener_siguiente()
    
