'''
Creado el 24/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''


NOMBRES = { '2s' : 1,
            '3s' : 2,
            '4s' : 3,
            '5s' : 4,
            '6s' : 5,
            '7s' : 6,
            '8s' : 7,
            '9s' : 8,
            'Ds' : 9,
            'Js' : 10,
            'Qs' : 11,
            'Ks' : 12,
            'As' : 13,
            
            '2h' : 1,
            '3h' : 2,
            '4h' : 3,
            '5h' : 4,
            '6h' : 5,
            '7h' : 6,
            '8h' : 7,
            '9h' : 8,
            'Dh' : 9,
            'Jh' : 10,
            'Qh' : 11,
            'Kh' : 12,
            'Ah' : 13,
            
            '2d' : 1,
            '3d' : 2,
            '4d' : 3,
            '5d' : 4,
            '6d' : 5,
            '7d' : 6,
            '8d' : 7,
            '9d' : 8,
            'Dd' : 9,
            'Jd' : 10,
            'Qd' : 11,
            'Kd' : 12,
            'Ad' : 13,
            
            '2c' : 1,
            '3c' : 2,
            '4c' : 3,
            '5c' : 4,
            '6c' : 5,
            '7c' : 6,
            '8c' : 7,
            '9c' : 8,
            'Dc' : 9,
            'Jc' : 10,
            'Qc' : 11,
            'Kc' : 12,
            'Ac' : 13
            }

PALOS = {'s' : 'picas',
         'h' : 'corazones',
         'd' : 'diamantes',
         'c' : 'tréboles'}

NOMBRE_VALOR = {1 : ['dos', 'doses'],
                2 : ['tres', 'treses'],
                3 : ['cuatro', 'cuatros'],
                4 : ['cinco', 'cincos'],
                5 : ['seis', 'seises'],
                6 : ['siete', 'sietes'],
                7 : ['ocho', 'ochos'],
                8 : ['nueve', 'nueves'],
                9 : ['diez', 'dieces'],
                10 : ['Jack', 'Jacks'],
                11 : ['Reina', 'Reinas'],
                12 : ['Rey', 'Reyes'],
                13 : ['As', 'Ases']
                }

JUEGOS = {0 : 'empate',
          1 : 'par',
          2 : 'doble par',
          3 : 'trío',
          4 : 'escalera',
          5 : 'color',
          6 : 'full house',
          7 : 'poker',
          8 : 'escalera color',
          9 : 'escalera real'
          }
  
class HandEvaluator(object):
    '''
    Sirve para evaluar las manos y decir cuál es la mejor
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def comparar_manos(self, mano1, mano2):
        '''
        Devuelve un lista, en la primera posición la mano (1 ó 2)
        y el nombre de la jugada ganadora
        '''
        cantidad = []
        for i in range(0,13):
            
            
            
        
        
        