'''
Creado el 24/09/2011

@author: Nahuel Hernández
@author: Javier Pérez
@author: Carlos Bellino
@author: Vanessa Jannete Cañete
@author: Gabriela Gaona
'''

#Oa los pibes, no apostaria ningun vello pubico por el funcionamiento correcto de estos metodos... 
from copy import deepcopy



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
          3 : 'trio',
          4 : 'escalera',
          5 : 'color',
          6 : 'full',
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
    
    #def comparar_manos(self, mano1, mano2):
    #    '''
    #    Devuelve un lista, en la primera posición la mano (1 ó 2)
    #    y el nombre de la jugada ganadora
    #    '''
    #    cantidad = []
    #    for i in range(0,13):
    
    def ganador(self,comunitarias,mano1,mano2):
        nombre_jugada1, jugada1 = self.mejor_en_mano(comunitarias, mano1)
        nombre_jugada2, jugada2 = self.mejor_en_mano(comunitarias, mano2)
        orden = ["carta alta","par","doble par","trio","escalera","color","full","poker","escalera color","escalera real"]
        peso = ["23456789djqk1"]
        if orden.index(nombre_jugada1) > orden.index(nombre_jugada2):
            return "Jugador1",nombre_jugada1,jugada1
        if orden.index(nombre_jugada1) < orden.index(nombre_jugada2):
            return "Jugador2",nombre_jugada2,jugada2
        if orden.index(nombre_jugada1) == orden.index(nombre_jugada2):
            if nombre_jugada1 == "carta alta" or nombre_jugada1 == "par" or nombre_jugada1 == "trio" or nombre_jugada1 == "poker":
                if peso.index(jugada1[0][0]) > peso.index(jugada1[0][0]):
                    return "Jugador1",nombre_jugada1,jugada1
                if peso.index(jugada1[0][0]) < peso.index(jugada1[0][0]):
                    return "Jugador2",nombre_jugada2,jugada2
                if peso.index(jugada1[0][0]) == peso.index(jugada1[0][0]):
                    return "Empate",nombre_jugada1,None
            if nombre_jugada1 == "doble par":
                if peso.index(jugada1[3][0]) > peso.index(jugada2[3][0]):
                    return "Jugador1",nombre_jugada1,jugada1
                if peso.index(jugada1[3][0]) < peso.index(jugada2[3][0]):
                    return "Jugador2",nombre_jugada2,jugada2
                if peso.index(jugada1[3][0]) == peso.index(jugada2[3][0]):
                    return "Empate",nombre_jugada1,None
            if nombre_jugada1 == "full" or nombre_jugada1 == "color" or nombre_jugada1 == "escalera" or nombre_jugada1 == "escalera color":
                if peso.index(jugada1[4][0]) > peso.index(jugada2[4][0]):
                    return "Jugador1",nombre_jugada1,jugada1
                if peso.index(jugada1[4][0]) < peso.index(jugada2[4][0]):
                    return "Jugador2",nombre_jugada2,jugada2
                if peso.index(jugada1[4][0]) == peso.index(jugada2[4][0]):
                    return "Empate",nombre_jugada1,None
            if nombre_jugada1 == "escalera real":
                return "Empate",nombre_jugada1,None
            
                
        
        
    def mejor_en_mano(self, comunitarias, cartas):
        orden = ["carta alta","par","doble par","trio","escalera","color","full","poker","escalera color","escalera real"]
        #peso = ["123456789djqx1"]
        while comunitarias.count(None)>0 :
            comunitarias.remove(None)
        total = cartas + comunitarias
        numeros_distintos = len(total)
        #self.gobisificar(total)
        total = self.arreglar(total)
        total = total.sort()
        jugada = ""
        mejor = "carta alta"
        probable_mejor = ""
        probable_mejor_jugada = ""
        colores = []
        total = self.unificar(total, colores)
        if total[0][0] == "1":
            jugada = self.normalizar(total[0])
        else:
            jugada =  self.normalizar(total[len(total)-1])
        
        if numeros_distintos > 3:
            probable_mejor, probable_mejor_jugada= self.comprobar_escalera(total, colores)
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
                
                



##############################Funciondes para hallar jugadas en mano#######################################
    def comprobar_escalera(self,total,c):
        #retorna una lista donde cada elemento es un string que indica el numero que forma la escalera, y una 
        #segunda lista de strings donde cada elemento indica el color del numero que forma la escalera 
        if len(total)<4:
            return False
        peso = ["123456789djqx1"]
        colores = deepcopy(c)
        total2 = deepcopy(total)
        if total2[0] == "1":
            total2.append(total2[0])
            colores.append(colores[0])
        bandera = 0
        i = -1
        jugada = []
        colors = []
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
                if escalera_color == False:
                    jugada = []
                    colors = []
                    for color in colores[i]:
                        if colores[i+1].count(color)>0 and colores[i+2].count(color)>0 and colores[i+3].count(color)>0:
                            escalera_color = True
                            color_comun = color
                    if escalera_color == True:
                        for j in range (i , i+4):
                            jugada = jugada.append(total2[j]) 
                        colors = [[color_comun], [color_comun],[color_comun],[color_comun]]
                        retorno = self.lista_retorno(jugada, colors)
                    else:
                        for j in range (i,i+4):
                            jugada.append(total2[j])   
                            colors.append([colores[j][0]])     
                        retorno = self.lista_retorno(jugada, colors)  
            if i + 4 > len(total2) - 1:
                bandera = 1
                
                
        escalera_real = False
        if encontrado == True:
            if retorno[0][0] == "j" and escalera_color == True:
                escalera_real = True
            if escalera_real == True:
                return "escalera real",retorno
            if escalera_color == True:
                return "escalera color",retorno
            return "escalera",retorno
        else:
            return None,None
    

        
                
    def comprobar_poker(self, t, c):
        #retorna un string indicando cual es el numero, y una lista donde cada elemento es un string 
        #que indica los cuatro colores que formaron el poker
        total = deepcopy(t)
        colores = deepcopy(c)
        indice = -1
        if total[0] == "1":
            total.append(total[0])
            colores.append[colores[0]]
        encontrado = False
        for i in range (len(colores)):
            if len(colores[i]) == 4:
                indice = i
                encontrado = True
        if encontrado == True:
            return "poker",self.normalizar(self.lista_retorno([total[indice]],[colores[indice]]))
        else:
            return None, None
        
        
    def comprobar_trio(self, t, c):
        #retorna un string indicando cual es el numero, y una lista donde cada elemento es un string 
        #que indica los tres colores que formaron el trio
        total = deepcopy(t)
        colores = deepcopy(c)
        indice = -1
        if total[0] == "1":
            total.append(total[0])
            colores.append[colores[0]]
        encontrado = False
        for i in range (len(colores)):
            if len(colores[i]) == 3:
                indice = i
                encontrado = True
        if encontrado == True:
            return "trio",self.normalizar(self.lista_retorno([total[indice]],[colores[indice]]))
        else:
            return None, None
        
    
    
    def comprobar_par(self, t, c):
        #retorna un string indicando cual es el numero, y una lista donde cada elemento es un string 
        #que indica los dos colores que formaron el par
        total = deepcopy(t)
        colores = deepcopy(c)
        indice = -1
        if total[0] == "1":
            total.append(total[0])
            colores.append[colores[0]]
        encontrado = False
        for i in range (len(colores)):
            if len(colores[i]) == 2:
                indice = i
                encontrado = True
        if encontrado == True:
            return "par",self.normalizar(self.lista_retorno([total[indice]],[colores[indice]]))
        else:
            return None, None
        
        
    def comprobar_full(self,t,c):
        #retorno una lista con los dos numeros, y una lista de dos elementos, siendo los dos elementos
        #otras dos listas indicando los colores correspondientes al numero con mismo indice
        par,jugada_par = self.comprobar_par(t,c)
        if par != None:
            trio, jugada_trio = self.comprobar_trio(t,c)
            if trio != None:
                return "full",self.normalizar(jugada_trio + jugada_par)
        return None,None
    def comprobar_doble_par(self,t,c):
        total = deepcopy(t)
        colores = deepcopy(c)
        mejor,jugada = self.comprobar_par(total,colores)
        if mejor != None:
            numero = jugada[0][0]
            indice = total.index(numero)
            total.pop(indice)
            colores.pop(indice)
            mejor, jugada2 = self.comprobar_par(total,colores)
            if mejor != None:
                return "doble par", self.normalizar(jugada + jugada2)
            else:
                return None, None
        else:
            return None, None
    
    def comprobar_color(self,t,c):
        total = deepcopy(t)
        colores = deepcopy(c)
        if total[0] == "1":
            total.append(total[0])
            colores.append[colores[0]]
        total.pop(0)
        colores.pop(0)
        predefinidos = ["d","s","c","h"]
        jugada = []
        for color in predefinidos:
            contador = 0
            jugada = []
            for i in range(len(colores)):
                if colores[i].count(color)>0:
                    contador = contador + 1
                    jugada.append(total[i] + color)
            if len(jugada) == 4:
                return "color", jugada
            if len(jugada) > 4:
                while len(jugada) > 4:
                    jugada.pop(0)
                return "color",self.normalizar(jugada)
        return None, None
                
                    
            
        
#######################Funciones para hallar jugadas probables##############################################
    
    def posible_escalera_abierta(self,t,c):
        peso = ["123456789djqx1"]
        colores = deepcopy(c)
        total2 = deepcopy(t)
        if len(total2)<3:
            return False
        if total2[0] == "1":
            total2.append(total2[0])
            colores.append(colores[0])
        bandera = 0
        i = -1
        while bandera == 0:
            i = i+1
            j = 0
            subcadena_numeros = ""
            for j in range (i,i+3):
                subcadena_numeros = subcadena_numeros + total2[j]                 
            
            if peso.find(subcadena_numeros) > -1 and total2[0]!="1" and total2[len(total2)-1]!="1":
                return True
            if i + 3 > len(total2) - 1:
                bandera = 1
        return False
    
    def posible_escalera_interna(self,t,c):
        #colores = deepcopy(c)
        total2 = deepcopy(t)
        if len(total2)<3:
            return False
        if total2[0] == "1":
            total2.append(total2[0])
        peso = ["123456789djqx1"]
        encontrados = []
        for i in range(14):
            encontrados.append("0")
        bandera = 0
        i = -1
        while bandera == 0:
            i = i+1
            j = 0
            subcadena_numeros = ""
            for i in range(14):
                encontrados[i] = "0"
            for j in range (i,i+4):
                subcadena_numeros = subcadena_numeros + total2[j]
            for char in subcadena_numeros:
                index = peso.index(char)
                encontrados[index] = "1"
            if encontrados[0] == "1":
                encontrados[13] = "1"
                
            for i in range(11):
                contador = 0
                for j in range(4):
                    if encontrados[i+j] == "1":
                        contador = contador + 1
                if contador == 3:
                    return True
            if i + 4 > len(total2) - 1:
                bandera = 1
        return False
    
    
    def posible_color(self,t,c):
        total = deepcopy(t)
        colores = deepcopy(c)
        predefinidos = ["d","s","c","h"]
        for color in predefinidos:
            contador = 0
            for i in range(len(colores)):
                if colores[i].count(color)>0:
                    contador = contador + 1
            if contador == 3:
                return True
        return False
    
    
        
        
                 
#########################Funciones de modificacion de formatos y demas yerbas##############################
                
    def normalizar(self,jugada):
        for carta in jugada:
            if carta[0] == "x":
                carta = carta.replace("x","k")
                
    
    def lista_retorno(self,numeros, colores):
        retorno = []
        for i in range(len(numeros)):
            for color in colores[i]:
                retorno.append(numeros[i]+ color)
        return retorno
    
    
    def unificar(self, total, colores):
        #elimina del conjunto de cartas los numeros que estan repetidos, y separa los numerps de los colores
        #en 2 listas distintas. La lista de numeros contiene strings que indican los numeros, y la lista de 
        #colores contiene como elementos otras listas que contienen los colores de un numero dado
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
    
    
    def gobisificar(self,mano, comunitarias):
        colores = []
        while comunitarias.count(None)>0 :
            comunitarias.remove(None)
        total = mano + comunitarias
        total = self.arreglar(total)
        total = total.sort()
        numeros = self.unificar(total, colores)
        return numeros, colores
        
    def arreglar(self,total):
        #cambia las K por X, para hacer mas facil el analisis de encontrar escaleras
        for carta in total:
            if carta[0] == "k":
                carta= carta.replace("k","x")
            
            
            
        
        
        
