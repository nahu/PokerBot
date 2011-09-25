# -*- coding: utf-8 -*-
'''
Creado el 23/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

#import Jugador

class Bot():
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
    
    def mejor_en_mano(self, comunitarias):
        orden = ["carta alta","par","doble par","trio","escalera","color","full","poker","escalera color","escalera real"]
        peso = ["123456789djqx1"]
        while comunitarias.count(None)>0 :
            comunitarias.remove(None)
        total = self.cartas + comunitarias
        total = total.arreglar(total)
        total = total.sort()
        jugada = ""
        mejor = "carta alta"
        probable_mejor = ""
        probable_mejor_jugada = ""
        numeros_distintos = self.cant_num_distintos(total)
        colores = []
        total = self.unificar(total, colores)
        if total[0] == "1":
            jugada = total[0]
        else:
            jugada =  total[len(total)-1]
        
        if numeros_distintos > 3:
            probable_mejor, probable_mejor_jugada = self.comprobar_escalera(total, colores, peso)
            if probable_mejor != None:
                if orden.index(probable_mejor) > orden.index(mejor):
                    mejor = probable_mejor
                    jugada = probable_mejor_jugada
            if orden.index("poker") > orden.index(mejor):
                probable_mejor,probable_mejor_jugada = self.comprobar_poker(total,colores)
                if probable_mejor != None:
                    mejor = probable_mejor
                    jugada = probable_mejor_jugada
            if orden.index("full") > orden.index(mejor):
                probable_mejor,probable_mejor_jugada = self.comprobar_full(total,colores)
                if probable_mejor != None:
                    mejor = probable_mejor
                    jugada = probable_mejor_jugada
            if orden.index("color") > orden.index(mejor):
                probable_mejor,probable_mejor_jugada = self.comprobar_color(total,colores)
                if probable_mejor != None:
                    mejor = probable_mejor
                    jugada = probable_mejor_jugada
            if orden.index("trio") > orden.index(mejor):
                probable_mejor,probable_mejor_jugada = self.comprobar_trio(total,colores)
                if probable_mejor != None:
                    mejor = probable_mejor
                    jugada = probable_mejor_jugada
            if orden.index("doble par") > orden.index(mejor):
                probable_mejor,probable_mejor_jugada = self.comprobar_doble_par(total,colores)
                if probable_mejor != None:
                    mejor = probable_mejor
                    jugada = probable_mejor_jugada
        if orden.index("par") > orden.index(mejor):
                probable_mejor,probable_mejor_jugada = self.comprobar_par(total,colores)
                if probable_mejor != None:
                    mejor = probable_mejor
                    jugada = probable_mejor_jugada
        return mejor, jugada
                
                
            
        
    def cant_num_distintos(self,total):
        encontrados = []
        for carta in total:
            numero = carta[0]
            if encontrados.count(numero) == 0:
                encontrados.apend(numero)
        return len(encontrados)
    def arreglar(self,total):
        for carta in total:
            if carta[0] == "k":
                carta[0]= "x"
    def comprobar_escalera(self,total2,colores,peso):
        if total2[0] == "1":
            total2.append(total2[0])
            colores.append(colores[0])
        bandera = 0
        i = -1
        jugada = []
        encontrado = False
        escalera_color = False
        while bandera == 0:
            i = i+1
            j = 0
            subcadena_numeros = ""
            for j in range (i,i+4):
                subcadena_numeros = subcadena_numeros + total2[j]                 
            
            if peso.find(subcadena_numeros) > -1 :
                encontrado = True
                color_comun = ""
                jugada = ""
                if escalera_color == False:
                    for color in colores[i]:
                        if colores[i+1].count(color)>0 and colores[i+2].count(color)>0 and colores[i+3].count(color)>0:
                            escalera_color = True
                            color_comun = color
                    if escalera_color == True:
                        for j in range (i , i+4):
                            jugada = jugada + total2[j] + color_comun
                    else:
                        for j in range (i,i+4):
                            jugada = jugada + total2[j] + colores[j][0]         
            if i + 4 > len(total2) - 1:
                bandera = 1
                
                
        escalera_real = False
        if encontrado == True:
            if jugada[0] == "j" and escalera_color == True:
                escalera_real = True
            if escalera_real == True:
                return ("escalera real",jugada)
            if escalera_color == True:
                return ("escalera color",jugada)
            return ("escalera",jugada)
        else:
            return (None,None)
    
    def unificar(self, total, colores):
        #funcion probada
        unificado = []
        indice = -1
        for carta in total:
            if unificado.count(carta[0]) == 0:
                indice = indice + 1
                unificado.append(carta[0])
                colores.append([carta[1]])
            else:
                colores[indice].append(carta[1])
        return unificado
                
        
        
                
    
        
        
    
