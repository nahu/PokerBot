#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import os, sys, pygame 
from pygame.locals import * 
import threading  
from Jugador import Jugador
from Mesa import Mesa
from Bot import Bot

# Constantes
WIDTH = 1084
HEIGHT = 600

FICHAS1 = 10000
FICHAS2 = 10000
CIEGA = 100

# Clases 
# ---------------------------------------------------------------------
  
class Thread(threading.Thread):  
    def __init__(self, mesa):
        threading.Thread.__init__(self)
        self.mesa = mesa
        self.term = False
    
    def run(self):
        while True:
            resultado = self.mesa.juego()
#            print "Ganó el jugador" + str(self.mesa.jugadores[resultado[1]])
#            print "Jugada ganadora: " + resultado[2]
            
            if not resultado[0] or self.term:#el juego terminó
                break
        
    def dibujado(self):
        self.mesa.set_dibujado()
        
    def mostrar_boton(self):
        ''' Devuelve True si tengo que mostrar botos del jugador'''
        return self.mesa.jugadores[self.mesa.jugador_actual].dibujar_botones()
    
    def establecer_jugada(self, jugada):
        self.mesa.jugadores[self.mesa.jugador_actual].definir_jugada(jugada)
        
    def terminar(self):
        self.term = True
        

class Carta(pygame.sprite.Sprite):    
    def __init__(self, card , px, py):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("imagenes/cartas/b.gif", True)
        self.back_img = self.image
        self.front_img = load_image("imagenes/cartas/"+card+".gif", True)
        
        self.value = card
        
        self.rect = self.image.get_rect()
        self.rect.centerx = px
        self.rect.centery = py
        
        self.speed = [8, -8]
    
    def set_carta(self, card):
        self.front_img = load_image("imagenes/cartas/"+card+".gif", True)
        self.value = card

    def repartir(self, px, py):
#        print ('x: ', px, 'y: ', py)    #DEBUG
        if self.rect.centerx > px :        
            self.rect.centerx -= self.speed[0]
            bx=False
        elif self.rect.centerx < px :
            self.rect.centerx += self.speed[0]
            bx=False
        else:
            bx=True
        if self.rect.centery < py :        
            self.rect.centery -= self.speed[1]
            by=False
        elif self.rect.centery > py :
            self.rect.centery += self.speed[1]
            by=False
        else:
            by=True
        if bx and by:
            return True
        else:
            return False
        
    def flip(self):
        if self.image == self.back_img:
            self.image = self.front_img
        else:
            self.image = self.back_img    

class Boton(pygame.sprite.Sprite):    
    def __init__(self, tipo , px, py):
        """
        tipo:
            aceptar
            apostar
            pasar
            retirar
            subir_apuesta
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("imagenes/botones/boton_"+tipo+".png", True)
        self.image = pygame.transform.scale(self.image, (75,30))
        self.rect = self.image.get_rect()
        self.rect.centerx = px
        self.rect.centery = py
        self.activo = False
    
    def set_activo(self):
        self.activo = True
    
    def set_inactivo(self):
        self.activo = False
    
class JugadorGUI():    
    def __init__(self,fichas,bot,carta1,carta2,turno,posicion):
        self.bot   = bot                              #Humano o IA
        self.fichas = fichas
        self.apuesta = 0
        
        self.carta1 = Carta(carta1, WIDTH/4, HEIGHT/2)
        self.carta2 = Carta(carta2, WIDTH/4, HEIGHT/2)
        
        self.turno = turno
        self.dealer = False
        
        self.posicion = posicion                        # arriba / abajo
        
        px= WIDTH/1.5 - 50
        
        if self.posicion == "abajo":
            py= HEIGHT/1.5 + 45
            self.credito_jug = Texto('Credito: ' + str(self.fichas), WIDTH-WIDTH/1.5, 475)
            self.apuesta_jug = Texto('Apuesta: ' + str("0"), WIDTH/2, 417)
            self.ganador = Texto('Ganador!!  ' + str(" "), WIDTH/2 -10, 397)
        elif self.posicion == "arriba":
            py= HEIGHT/6.5 - 15
            self.credito_jug = Texto('Credito: ' + str(self.fichas), WIDTH-WIDTH/1.5, 125)
            self.apuesta_jug = Texto('Apuesta: ' + str("0"), WIDTH/2, 175)
            self.ganador = Texto('Ganador!!  ' + str(" "), WIDTH/2 -10, 195)
    
        self.boton_retirar = Boton("retirar", px, py) 
        self.boton_pasar   = Boton("pasar", px, py+35)
        self.boton_aceptar = Boton("aceptar", px, py+35)
        self.boton_apostar = Boton("apostar", px, py+70)
        self.boton_subir_apuesta = Boton("subir_apuesta", px, py+70)
               
    
    def cartas_al_maso(self):    
        
        self.carta1.rect.centerx = WIDTH/4 
        self.carta1.rect.centery = HEIGHT/2
        
        self.carta2.rect.centerx = WIDTH/4 
        self.carta2.rect.centery = HEIGHT/2
        
        self.carta1.image = load_image("imagenes/cartas/b.gif", True)
        self.carta2.image = load_image("imagenes/cartas/b.gif", True)
        
    def set_cartas(self,carta1,carta2):
        self.carta1.value = carta1
        self.carta2.value = carta2
    
    def get_cartas(self):
        return self.carta1 , self.carta2
    
    def get_boton(self, tipo):
        """
        tipo:
            aceptar
            apostar
            pasar
            retirar
            subir_apuesta
        """
        if tipo == "pasar":
            return self.boton_pasar
        if tipo == "aceptar":
            return self.boton_aceptar
        if tipo == "retirar":
            return self.boton_retirar
        if tipo == "apostar":
            return self.boton_apostar
        if tipo == "subir_apuesta":
            return self.boton_subir_apuesta
    
    def set_apuesta(self, apuesta):
        self.apuesta_jug.update_texto('Apuesta: ' + str(apuesta))
        self.apuesta = apuesta
        
    def set_credito(self, fichas):
        self.credito_jug.update_texto('Credito: ' + str(fichas))    
        self.fichas = fichas
            
    def set_ganador(self, jugada):
        self.ganador.update_texto('Ganador!!  ' + jugada)

        
class MesaGUI():
    def __init__(self):
        self.pozo = Texto('Pozo: ' + str('0'), 815, HEIGHT/2)
        self.carta1 = Carta('b', WIDTH/4, HEIGHT/2)
        self.carta2 = Carta('b', WIDTH/4, HEIGHT/2)
        self.carta3 = Carta('b', WIDTH/4, HEIGHT/2)
        self.carta4 = Carta('b', WIDTH/4, HEIGHT/2)
        self.carta5 = Carta('b', WIDTH/4, HEIGHT/2)
        
    def cartas_al_maso(self):
        
        self.carta1.image = load_image("imagenes/cartas/b.gif", True)
        self.carta1.rect.centerx = WIDTH/4 
        self.carta1.rect.centery = HEIGHT/2
        
        self.carta2.image = load_image("imagenes/cartas/b.gif", True)
        self.carta2.rect.centerx = WIDTH/4 
        self.carta2.rect.centery = HEIGHT/2
        
        self.carta3.image = load_image("imagenes/cartas/b.gif", True)
        self.carta3.rect.centerx = WIDTH/4 
        self.carta3.rect.centery = HEIGHT/2
        
        self.carta4.image = load_image("imagenes/cartas/b.gif", True)
        self.carta4.rect.centerx = WIDTH/4 
        self.carta4.rect.centery = HEIGHT/2
        
        self.carta5.image = load_image("imagenes/cartas/b.gif", True)
        self.carta5.rect.centerx = WIDTH/4 
        self.carta5.rect.centery = HEIGHT/2

    def mostrar_flop(self):
        
        repartida = [False, False,False]
                
        repartida[0] = self.carta1.repartir(383, HEIGHT/2)
        if repartida[0]:
            repartida[1] = self.carta2.repartir(463, HEIGHT/2)
        if repartida[1]:
            repartida[2] = self.carta3.repartir(543, HEIGHT/2)
            

        if repartida[0] and repartida[1] and repartida[2]:
            self.carta1.flip()
            self.carta2.flip()
            self.carta3.flip()
            return False
        return True

    def mostrar_turn(self):
        repartida = self.carta4.repartir(623, HEIGHT/2)
        if repartida:
            self.carta4.flip()
            return False
        return True

    def mostrar_river(self):
        repartida = self.carta5.repartir(703, HEIGHT/2)
        if repartida:
            self.carta5.flip()
            return False
        return True

    def set_pozo(self, monto):
        self.pozo.update_texto('Pozo: ' + str(monto))

class Dealer(pygame.sprite.Sprite):    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("imagenes/fichas/dealer.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
        self.speed = [8, -8]
    
    def set_pos(self, pos):
        if pos == "abajo":
            self.rect.centerx = WIDTH/2.4
            self.rect.centery = HEIGHT/1.42
        elif pos == "arriba":
            self.rect.centerx = WIDTH/2.4
            self.rect.centery = HEIGHT/3.45
        

class Texto(pygame.sprite.Sprite):
    def __init__(self,texto, posx, posy, color=(255, 255, 255)):
        pygame.sprite.Sprite.__init__(self)
        self.fuente = pygame.font.Font('imagenes/DroidSans.ttf', 16)
        self.color = color
        self.image = pygame.font.Font.render(self.fuente, texto, 1, color)
        self.rect = self.image.get_rect()
        self.rect.centerx = posx
        self.rect.centery = posy
        
    def update_texto(self, texto):
        self.image = pygame.font.Font.render(self.fuente, texto, 1, self.color)

# ---------------------------------------------------------------------
# Funciones
# ---------------------------------------------------------------------


def load_image(filename, transparent=False):
    try: image = pygame.image.load(filename)
    except pygame.error, message:
        raise SystemExit, message
    image = image.convert_alpha()
    if transparent:
        color = image.get_at((0,0))
        image.set_colorkey(color, RLEACCEL)
    return image
    
    
def borrar_botones(sprites , jugador):
        if jugador.get_boton("aceptar") in sprites:
            sprites.remove(jugador.get_boton("aceptar"))
        if jugador.get_boton("pasar") in sprites:
            sprites.remove(jugador.get_boton("pasar"))
        if jugador.get_boton("retirar") in sprites:
            sprites.remove(jugador.get_boton("retirar"))
        if jugador.get_boton("subir_apuesta") in sprites:
            sprites.remove(jugador.get_boton("subir_apuesta"))

def actualizar_mesa(mesa , hilo, tipo):
    '''tipo: 1 = Flop, 2 = Turn, 3 = River '''
    if tipo == 2:
        mesa.carta1.set_carta(hilo.mesa.comunitarias [0])
        mesa.carta2.set_carta(hilo.mesa.comunitarias [1])
        mesa.carta3.set_carta(hilo.mesa.comunitarias [2])
    elif tipo == 3:
        mesa.carta4.set_carta(hilo.mesa.comunitarias [3])
    elif tipo == 4:
        mesa.carta5.set_carta(hilo.mesa.comunitarias [4])

def actualizar_jugador(jugador1, jugador2, hilo ):
    jugador1.carta1.set_carta(hilo.mesa.jugadores[0].mano[0])
    jugador1.carta2.set_carta(hilo.mesa.jugadores[0].mano[1])
    jugador2.carta1.set_carta(hilo.mesa.jugadores[1].mano[0])
    jugador2.carta2.set_carta(hilo.mesa.jugadores[1].mano[1])                
    
    jugador1.dealer = hilo.mesa.jugadores[0].dealer
    jugador2.dealer = hilo.mesa.jugadores[1].dealer
    
    jugador1.bot = hilo.mesa.jugadores[0].bot
    jugador2.bot = hilo.mesa.jugadores[1].bot
    
    jugador1.set_credito(hilo.mesa.jugadores[0].fichas)
    jugador2.set_credito(hilo.mesa.jugadores[1].fichas)
                    
    jugador1.set_apuesta(hilo.mesa.jugadores[0].apuesta_actual)
    jugador2.set_apuesta(hilo.mesa.jugadores[1].apuesta_actual)
           
    
def repartir_manos(repartida, jugador1, jugador2, cartas_abiertas):
#    if jugador1.carta1.image != jugador1.carta1.back_img:
#        jugador1.carta1.image = jugador1.carta1.back_img
#    if jugador1.carta2.image != jugador1.carta2.back_img:
#        jugador1.carta2.image = jugador1.carta2.back_img
#    if jugador2.carta1.image != jugador2.carta1.back_img:
#        jugador2.carta1.image = jugador2.carta1.back_img
#    if jugador2.carta2.image != jugador2.carta2.back_img:
#        jugador2.carta2.image = jugador2.carta2.back_img    
    
    repartida = [False,False,False,False]
    repartida[0] = jugador2.get_cartas()[0].repartir(583, 108)
    if repartida[0]:
        repartida[1] = jugador2.get_cartas()[1].repartir(503, 108)
    if repartida[1]:
        repartida[2] = jugador1.get_cartas()[0].repartir(583, 484)
    if repartida[2]:
        repartida[3] = jugador1.get_cartas()[1].repartir(503, 484)
    if repartida[0] and repartida[1] and repartida[2] and repartida[3] :
        jugador1.get_cartas()[0].flip()
        jugador1.get_cartas()[1].flip()
        if cartas_abiertas:
            jugador2.get_cartas()[0].flip()
            jugador2.get_cartas()[1].flip()
        return False
    return True

# ---------------------------------------------------------------------
 
def main():
    
    '''Definiciones Pygame'''
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    pygame.display.set_caption("Wumpus Poker")
    
    '''Fondo'''
    
    background_image = load_image('imagenes/fondo.gif')
    background_image = pygame.transform.scale(background_image, (WIDTH,HEIGHT))
    
    '''Instancias'''

#    jug1 = Jugador(1,FICHAS1, "Pibe",  lock_jugador)
#    jug2 = Jugador(2,FICHAS2, "PC")
    lock_dibujar = threading.Lock()
    lock_jugador = threading.Lock()
    
#   jug1 = Jugador(1,FICHAS1, "Pibe")
#   jug2 = Bot(2,FICHAS2, "PC")
    
    jug1 = Jugador(1,FICHAS1, "Pibe", lock_jugador)
    jug2 = Bot(2,FICHAS2, "PC")
    mesa_nahu = Mesa(CIEGA, [jug1, jug2], lock_dibujar)
    
    hilo = Thread(mesa_nahu)
    
    hilo.start()
     
    mesa = MesaGUI()
    mazo = Carta("b", WIDTH/4, HEIGHT/2)
    ficha_dealer = Dealer()

    jugador1 = JugadorGUI(FICHAS1,False,"b","b",0, "abajo")
    jugador2 = JugadorGUI(FICHAS2,True,"b","b",0, "arriba")
    
    jugador1.dealer=True                                    #DEBUG
    ficha_dealer.set_pos("abajo")
    
    ''' Instancia Grupo de Sprites'''
    all_sprites=pygame.sprite.RenderUpdates()

    sprites = [
        mazo, 
        ficha_dealer, 
        mesa.pozo, 
        jugador1.credito_jug, 
        jugador2.credito_jug, 
        jugador1.apuesta_jug, 
        jugador2.apuesta_jug, 
        mesa.carta1, 
        mesa.carta2, 
        mesa.carta3, 
        mesa.carta4, 
        mesa.carta5, 
        jugador1.get_cartas()[0], 
        jugador1.get_cartas()[1], 
        jugador2.get_cartas()[0], 
        jugador2.get_cartas()[1], 
        #jugador1.get_boton("aceptar"), 
        #jugador1.get_boton("apostar"), 
        #jugador1.get_boton("pasar"), 
        #jugador1.get_boton("retirar"), 
        #jugador1.get_boton("subir_apuesta"), 
        #jugador2.get_boton("aceptar"), 
        #jugador2.get_boton("apostar"), 
        #jugador2.get_boton("pasar"), 
        #jugador2.get_boton("retirar"), 
        #jugador2.get_boton("subir_apuesta")
        ]
    
        
    all_sprites.add(sprites)
    
    
    ## Set de variables
    jugador1.turno = True
    jugador2.turno = False    
    conta = 0                                                           #DEBUG
    cartas_abiertas = False
        
    repartida_manos = False
    repartida_terminada = False
    flop = False
    flop_terminado = False
    turn = False
    turn_terminado = False
    river = False
    river_terminado = False
    dibujar_ganador1 = False
    dibujar_ganador2 = False
    
    mano_nueva = False
    
    while True:
        conta +=1                                                       #DEBUG
        time = clock.tick(60)  
        
        if hilo.mesa.dibujar:
            if hilo.mesa.ronda_actual.tipo == 1:
                if river_terminado:
                    jugador1.cartas_al_maso()
                    jugador2.cartas_al_maso()
                    mesa.cartas_al_maso()
                    river_terminado = False

                print 'Entro Ronda 1' 
                
                if mano_nueva == True:
                    pass
                actualizar_jugador(jugador1, jugador2, hilo )
                
                if jugador1.dealer:
                    ficha_dealer.set_pos("abajo")
                elif jugador2.dealer:
                    ficha_dealer.set_pos("arriba")
                
                mesa.set_pozo(hilo.mesa.bote)
                
                if not repartida_manos:
                    repartida_manos = True
                    
#                print ('j1.dibuBotones: ' , hilo.mesa.jugadores[0].dibujar_botones())
#                print ('j1.carta1', hilo.mesa.jugadores[0].mano[0])
#                print ('j1.carta2',hilo.mesa.jugadores[0].mano[1])                
#                print ('j1.dealer :', hilo.mesa.jugadores[0].dealer)
#                print ('j1.bot',hilo.mesa.jugadores[0].bot)
#                print ('j1.fichas',hilo.mesa.jugadores[0].fichas)
#                print ('j1.apuesta',hilo.mesa.jugadores[0].apuesta_actual)
#                print '  '    
#                print ('j2.dibuBotones: ' , hilo.mesa.jugadores[1].dibujar_botones())
#                print ('j2.carta1', hilo.mesa.jugadores[1].mano[0])
#                print ('j2.carta2',hilo.mesa.jugadores[1].mano[1])                
#                print ('j2.dealer :', hilo.mesa.jugadores[1].dealer)
#                print ('j2.bot',hilo.mesa.jugadores[1].bot)
#                print ('j2.fichas',hilo.mesa.jugadores[1].fichas)
#                print ('j2.apuesta',hilo.mesa.jugadores[1].apuesta_actual)
#                print '  '
#                print ('j1.nro apuesta', hilo.mesa.ronda_actual.nro_apuesta)
#                print ('mesa bote: ', hilo.mesa.bote)
                
                hilo.dibujado()

            elif hilo.mesa.ronda_actual.tipo == 2:
                print 'Entro Ronda 2'
                
                repartida_manos = True
                
                actualizar_jugador(jugador1, jugador2, hilo )
                actualizar_mesa(mesa,hilo,2)
                
                if jugador1.dealer:
                    ficha_dealer.set_pos("abajo")
                elif jugador2.dealer:
                    ficha_dealer.set_pos("arriba")
                
                mesa.set_pozo(hilo.mesa.bote)
                
                if not flop:
                    flop = True

#                print ('j1.dibuBotones: ' , hilo.mesa.jugadores[0].dibujar_botones())
#                print ('j1.carta1', hilo.mesa.jugadores[0].mano[0])
#                print ('j1.carta2',hilo.mesa.jugadores[0].mano[1])                
#                print ('j1.dealer :', hilo.mesa.jugadores[0].dealer)
#                print ('j1.bot',hilo.mesa.jugadores[0].bot)
#                print ('j1.fichas',hilo.mesa.jugadores[0].fichas)
#                print ('j1.apuesta',hilo.mesa.jugadores[0].apuesta_actual)
#                print '  '    
#                print ('j2.dibuBotones: ' , hilo.mesa.jugadores[1].dibujar_botones())
#                print ('j2.carta1', hilo.mesa.jugadores[1].mano[0])
#                print ('j2.carta2',hilo.mesa.jugadores[1].mano[1])                
#                print ('j2.dealer :', hilo.mesa.jugadores[1].dealer)
#                print ('j2.bot',hilo.mesa.jugadores[1].bot)
#                print ('j2.fichas',hilo.mesa.jugadores[1].fichas)
#                print ('j2.apuesta',hilo.mesa.jugadores[1].apuesta_actual)
#                print '  '
#                print ('j1.nro apuesta', hilo.mesa.ronda_actual.nro_apuesta)
#                print ('mesa bote: ', hilo.mesa.bote)                
                
                hilo.dibujado()

            elif hilo.mesa.ronda_actual.tipo == 3:
                print 'Entro Ronda 3'
                
                flop = True
                
                actualizar_jugador(jugador1, jugador2, hilo )
                actualizar_mesa(mesa,hilo,3)
                
                if jugador1.dealer:
                    ficha_dealer.set_pos("abajo")
                elif jugador2.dealer:
                    ficha_dealer.set_pos("arriba")
                
                mesa.set_pozo(hilo.mesa.bote)
                
                if not turn:
                    turn = True

#                print ('j1.dibuBotones: ' , hilo.mesa.jugadores[0].dibujar_botones())
#                print ('j1.carta1', hilo.mesa.jugadores[0].mano[0])
#                print ('j1.carta2',hilo.mesa.jugadores[0].mano[1])                
#                print ('j1.dealer :', hilo.mesa.jugadores[0].dealer)
#                print ('j1.bot',hilo.mesa.jugadores[0].bot)
#                print ('j1.fichas',hilo.mesa.jugadores[0].fichas)
#                print ('j1.apuesta',hilo.mesa.jugadores[0].apuesta_actual)
#                print '  '    
#                print ('j2.dibuBotones: ' , hilo.mesa.jugadores[1].dibujar_botones())
#                print ('j2.carta1', hilo.mesa.jugadores[1].mano[0])
#                print ('j2.carta2',hilo.mesa.jugadores[1].mano[1])                
#                print ('j2.dealer :', hilo.mesa.jugadores[1].dealer)
#                print ('j2.bot',hilo.mesa.jugadores[1].bot)
#                print ('j2.fichas',hilo.mesa.jugadores[1].fichas)
#                print ('j2.apuesta',hilo.mesa.jugadores[1].apuesta_actual)
#                print '  '
#                print ('j1.nro apuesta', hilo.mesa.ronda_actual.nro_apuesta)
#                print ('mesa bote: ', hilo.mesa.bote)
                
                hilo.dibujado()
            elif hilo.mesa.ronda_actual.tipo == 4:
                print 'Entro Ronda 4'
                
                turn = True
                
                actualizar_jugador(jugador1, jugador2, hilo )
                actualizar_mesa(mesa,hilo,4)
                
                if jugador1.dealer:
                    ficha_dealer.set_pos("abajo")
                elif jugador2.dealer:
                    ficha_dealer.set_pos("arriba")
                
                mesa.set_pozo(hilo.mesa.bote)
                
                if not river:
                    river = True

#                print ('j1.dibuBotones: ' , hilo.mesa.jugadores[0].dibujar_botones())
#                print ('j1.carta1', hilo.mesa.jugadores[0].mano[0])
#                print ('j1.carta2',hilo.mesa.jugadores[0].mano[1])                
#                print ('j1.dealer :', hilo.mesa.jugadores[0].dealer)
#                print ('j1.bot',hilo.mesa.jugadores[0].bot)
#                print ('j1.fichas',hilo.mesa.jugadores[0].fichas)
#                print ('j1.apuesta',hilo.mesa.jugadores[0].apuesta_actual)
#                print '  '    
#                print ('j2.dibuBotones: ' , hilo.mesa.jugadores[1].dibujar_botones())
#                print ('j2.carta1', hilo.mesa.jugadores[1].mano[0])
#                print ('j2.carta2',hilo.mesa.jugadores[1].mano[1])                
#                print ('j2.dealer :', hilo.mesa.jugadores[1].dealer)
#                print ('j2.bot',hilo.mesa.jugadores[1].bot)
#                print ('j2.fichas',hilo.mesa.jugadores[1].fichas)
#                print ('j2.apuesta',hilo.mesa.jugadores[1].apuesta_actual)
#                print '  '
#                print ('j1.nro apuesta', hilo.mesa.ronda_actual.nro_apuesta)
#                print ('mesa bote: ', hilo.mesa.bote)
                
                hilo.dibujado()
            if hilo.mesa.resultado != None:
                if not hilo.mesa.resultado[0]:
                    mano_nueva = True
                    if hilo.mesa.resultado[1] == 0:
                        jugador1.set_ganador(hilo.mesa.resultado[2])
                        dibujar_ganador1 = True
                    elif hilo.mesa.resultado[1] == 1:
                        jugador2.set_ganador(hilo.mesa.resultado[2])
                        dibujar_ganador2 = True
                    elif hilo.mesa.resultado[1] == None:
                        dibujar_ganador1 = True
                        dibujar_ganador2 = True
                        jugador1.set_ganador('Empate')
                        jugador2.set_ganador('Empate')
                        
                        #mesa.cartas_al_maso()
                        #repartida_manos = False
                        #flop = False
                        #turn = False
                        #river = False        
        if hilo.mesa.jugadores[0].dibujar_botones():
            borrar_botones(all_sprites, jugador1)
            all_sprites.add( jugador1.get_boton("apostar"),
                             jugador1.get_boton("pasar"),
                             jugador1.get_boton("retirar")) 
        
         
        if hilo.mesa.jugadores[1].dibujar_botones():
            borrar_botones(all_sprites, jugador2)
            all_sprites.add( jugador2.get_boton("apostar"),
                             jugador2.get_boton("pasar"),
                             jugador2.get_boton("retirar"))
        
        '''Fondo y Sprites Fijos'''
        
        screen.blit(background_image, (0, 0))
           
        
        '''Eventos:'''
            
        for eventos in pygame.event.get():                    
            if eventos.type == QUIT:
                hilo.terminar()
                hilo.join()
                sys.exit(0)
        
            elif eventos.type == MOUSEBUTTONUP:
                if eventos.button == 1: 
                    mX, mY = pygame.mouse.get_pos()
                    if (jugador1.get_cartas()[0].rect.collidepoint((mX,mY))):
                        jugador1.get_cartas()[0].flip()
                    if (jugador1.get_cartas()[1].rect.collidepoint((mX,mY))):
                        jugador1.get_cartas()[1].flip()
                    if (jugador2.get_cartas()[0].rect.collidepoint((mX,mY))):
                        jugador2.get_cartas()[0].flip()
                    if (jugador2.get_cartas()[1].rect.collidepoint((mX,mY))):
                        jugador2.get_cartas()[1].flip()
                        
                    if (jugador1.get_boton("aceptar").rect.collidepoint((mX,mY)) and jugador1.turno and (jugador1.get_boton("aceptar") in all_sprites) and hilo.mesa.jugadores[0].dibujar_botones() ):
                        hilo.establecer_jugada("igualar")
                    if (jugador1.get_boton("apostar").rect.collidepoint((mX,mY)) and jugador1.turno and (jugador1.get_boton("apostar") in all_sprites) and hilo.mesa.jugadores[0].dibujar_botones() ):
                        hilo.establecer_jugada("apostar")
                    if (jugador1.get_boton("retirar").rect.collidepoint((mX,mY)) and jugador1.turno and (jugador1.get_boton("retirar") in all_sprites) and hilo.mesa.jugadores[0].dibujar_botones() ):
                        hilo.establecer_jugada("no_ir")
                    if (jugador1.get_boton("subir_apuesta").rect.collidepoint((mX,mY)) and jugador1.turno and (jugador1.get_boton("subir_apuestas") in all_sprites) and hilo.mesa.jugadores[0].dibujar_botones() ):
                        hilo.establecer_jugada("apostar")
                    if (jugador1.get_boton("pasar").rect.collidepoint((mX,mY)) and jugador1.turno and (jugador1.get_boton("pasar") in all_sprites) and hilo.mesa.jugadores[0].dibujar_botones()):
                        hilo.establecer_jugada("igualar")
                                
            elif eventos.type == KEYDOWN:
                if eventos.key == 109:
                    jugador2.get_cartas()[0].flip()
                    jugador2.get_cartas()[1].flip()
                elif eventos.key == 102:    
                    pygame.display.toggle_fullscreen()    
                elif eventos.key == 113:
                    hilo.terminar()
                    hilo.join()    
                    sys.exit(0)
        
        '''DEBUG'''

        
        '''Jugador 1'''
        #print ('jug1 turno: ',jugador1.turno,'jug2 turno: ',jugador2.turno, 'Bandera: ' , bandera)         #DEBUG
        
#        if jugador1.turno == True: 
#            if bandera1 == True:
#                jugador1.turno = False
#                jugador2.turno = True
#                bandera1 = False
#                print obtenerju
#                print jug1
#        
#        '''Jugador 2'''
#        if jugador2.turno == True:
#            if bandera2 == True:                
#                jugador1.turno = True
#                jugador2.turno = False
#                bandera2 = False
#                print obtenerju
#                print jug2
        
        '''Animaciones'''

        if repartida_manos:
            repartida_manos = repartir_manos(repartida_manos, jugador1, jugador2, cartas_abiertas)
            if not repartida_manos:
                jugador1.carta1.image = jugador1.carta1.front_img
                jugador1.carta2.image = jugador1.carta2.front_img
                #jugador2.carta1.image = jugador2.carta1.front_img
                #jugador2.carta2.image = jugador2.carta2.front_img                
                repartida_terminada = True
                
        if flop and repartida_terminada:
            flop = mesa.mostrar_flop()
            if not flop:
                mesa.carta1.image = mesa.carta1.front_img
                mesa.carta2.image = mesa.carta2.front_img
                mesa.carta3.image = mesa.carta3.front_img
                flop_terminado = True

        if turn and flop_terminado:
            turn = mesa.mostrar_turn()
            if not turn:
                mesa.carta4.image = mesa.carta4.front_img
                turn_terminado = True
                
        if river and turn_terminado:
            river = mesa.mostrar_river()
            if not river:
                mesa.carta5.image = mesa.carta5.front_img
                river_terminado = True
        
        if dibujar_ganador1 and river_terminado:
            all_sprites.add(jugador1.ganador)

        if dibujar_ganador2 and river_terminado:
            all_sprites.add(jugador2.ganador)
            

        
        '''Actualizar Sprites'''
        
        all_sprites.update(background_image, sprites)
        
        '''Dibujar en Pantalla'''
        
        all_sprites.draw(screen)        
        
        pygame.display.flip()
    return 0

if __name__ == '__main__':
    pygame.init()
    main() 
