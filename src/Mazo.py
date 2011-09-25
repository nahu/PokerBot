'''
Creado el 23/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

class Mazo(object):
    '''
    Clase que represente el mazo de cartas
    
    #TODO: completar toda el diccionario
    
    Configuren bien su editor a utf-8 para no tener problemas,
    si usan Eclipse, Window->preferences->general->workspace->text file encoding
    
    A, 2, 3, 4, 5, 6, 7, 8, 9, D, J, Q, K
    s = spades = picas
    h = hearts = corazones
    d = diamonds = diamantes
    c = clubs = tréboles
    '''
    
    nombre = {'As' : 'As de picas',
              '2s' : 'Dos de picas',
              
              
              'Jc' : 'Jack de tréboles',
              'Qc' : 'Reina de tréboles',
              'Kc' : 'Rey de tréboles'
              }

    def __init__(self, semilla):
        '''
        Constructor
        la semilla es para la generación de números aleatorios

        '''
        self.semilla = semilla
        
    #TODO metodos de generacion de numeros aleatorios, mezclado, obtención de cartas, etc.
    
