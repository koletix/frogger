#! /usr/bin/env python
import pygame
import random as Random
from pygame.locals import *
from sys import exit


pygame.init()
pygame.font.init()
pygame.mixer.pre_init(44100, 32, 2, 4096)

font_name = pygame.font.get_default_font()
game_font = pygame.font.SysFont(font_name, 20)
info_font = pygame.font.SysFont(font_name, 20)
menu_font = pygame.font.SysFont(font_name, 20)

screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN, 32)

def scale_sprite(sprite, screen_width):
    scale_factor = screen_width / 448  # Assuming original width was 448
    new_width = int(sprite.get_width() * scale_factor)
    new_height = int(sprite.get_height() * scale_factor)
    return pygame.transform.scale(sprite, (new_width, new_height))



# Game boundaries based on the new screen size
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
game_boundary_right = screen_width - 40  # Set boundary slightly inward
game_boundary_left = 0
game_boundary_top = 40  # Start after the upper panel area
game_boundary_bottom = screen_height - 50  # Start above the bottom bar (time and lives)


# Load the custom font
font_path = './frogger/Fonts/bit5x3.ttf'  # Update this to the correct path where your font is located
game_font = pygame.font.Font(font_path, 30)  # For the main game font
info_font = pygame.font.Font(font_path, 30)  # For the info font
menu_font = pygame.font.Font(font_path, 30)  # For the menu font


# --- Carregando imagens ---
background_filename = './frogger/images/bg2.png'

frog_filename = './frogger/images/pruebaup.png'
arrived_filename = './frogger/images/frog_arrived.png'
car1_filename = './frogger/images/car1.png'
car2_filename = './frogger/images/car2.png'
car3_filename = './frogger/images/car3.png'
car4_filename = './frogger/images/car4.png'
car5_filename = './frogger/images/car5.png'
plataform_filename = './frogger/images/tronco2.png'
turtle_filename = './frogger/images/Turtle_03.png'  # Nueva imagen de tortuga
home_filename = './frogger/images/Home.png'  # Imagen de los arbustos ################
fill_filename = './frogger/images/relleno.png'  # Ruta a la imagen de relleno

tortu_vida = './frogger/images/frog_arrived.png'  # Ruta a la imagen de relleno


frog_image = pygame.image.load(frog_filename).convert_alpha()
background = pygame.image.load(background_filename).convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

sprite_sapo = pygame.image.load(frog_filename).convert_alpha()


sprite_arrived = pygame.image.load(arrived_filename).convert_alpha()
#sprite_car1 = scale_sprite(pygame.image.load(car1_filename).convert_alpha(), screen_width)
sprite_car1 = scale_sprite(pygame.image.load(car1_filename).convert_alpha(), screen_width)
sprite_car2 = scale_sprite(pygame.image.load(car2_filename).convert_alpha(), screen_width)
sprite_car3 = scale_sprite(pygame.image.load(car3_filename).convert_alpha(), screen_width)
sprite_car4 = scale_sprite(pygame.image.load(car4_filename).convert_alpha(), screen_width)
sprite_car5 = scale_sprite(pygame.image.load(car5_filename).convert_alpha(), screen_width)

sprite_plataform = scale_sprite(pygame.image.load(plataform_filename).convert_alpha(), screen_width)

sprite_turtle= scale_sprite(pygame.image.load(turtle_filename).convert_alpha(), screen_width)
#sprite_turtle = pygame.transform.scale(pygame.image.load(turtle_filename).convert_alpha(), (30, 30))  # Escalar la tortuga si es necesario
# Escalar la imagen del arbusto a un tamaño mayor
sprite_home = scale_sprite(pygame.image.load(home_filename).convert_alpha(), screen_width)
#sprite_home = pygame.transform.scale(pygame.image.load('./frogger/images/Home.png').convert_alpha(), (70, 30))  # Cambiar dimensiones
# --- Escalar la imagen de relleno ---
sprite_fill = pygame.transform.scale(pygame.image.load('./frogger/images/relleno.png').convert_alpha(), (130, 85))  # Ajustar el tamaño
sprite_tortuvida= pygame.image.load(tortu_vida).convert_alpha()
sprite_tortuvida = pygame.transform.flip(sprite_tortuvida, False, True)
sprite_tortuvida = pygame.transform.scale(sprite_tortuvida, (int(sprite_tortuvida.get_width() * 1.5), int(sprite_tortuvida.get_height() * 1.5)))
# --- Carregando Efeitos Sonoros ---
hit_sound = pygame.mixer.Sound('./frogger/sounds/boom.wav')
agua_sound = pygame.mixer.Sound('./frogger/sounds/agua.wav')
chegou_sound = pygame.mixer.Sound('./frogger/sounds/success.wav')
trilha_sound = pygame.mixer.Sound('./frogger/sounds/guimo.wav')

pygame.display.set_caption('Frogger')
clock = pygame.time.Clock()




class Object():
    def __init__(self,position,sprite):
        self.sprite = sprite
        self.position = position

    def draw(self):
        screen.blit(self.sprite,(self.position))

    def rect(self):
        return Rect(self.position[0],self.position[1],self.sprite.get_width(),self.sprite.get_height())


class Home(Object):
    def __init__(self, position, sprite_home):
        self.sprite = sprite_home
        self.position = position

    def draw(self):
        screen.blit(self.sprite, (self.position))

    def rect(self):
        return Rect(self.position[0], self.position[1], self.sprite.get_width(), self.sprite.get_height())

homes = []  # Lista para los arbustos


class Frog(Object):
    def __init__(self, position, sprite_sapo):
        self.sprite = sprite_sapo
        self.position = position
        self.lives = 3
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def updateSprite(self, key_pressed):
        if self.way != key_pressed:
            self.way = key_pressed
            if self.way == "up":
                frog_filename = './frogger/images/pruebaup.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "down":
                frog_filename = './frogger/images/pruebadown.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "left":
                frog_filename = './frogger/images/pruebaleft.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "right":
                frog_filename = './frogger/images/pruebaright.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()

    def moveFrog(self, key_pressed, key_up):
        if self.animation_counter == 0:
            self.updateSprite(key_pressed)
        self.incAnimationCounter()

        if key_up == 1:
            if key_pressed == "up":
                if self.position[1] > game_boundary_top:
                    self.position[1] -= 13
            elif key_pressed == "down":
                if self.position[1] < game_boundary_bottom:
                    self.position[1] += 13
            elif key_pressed == "left":
                if self.position[0] > game_boundary_left:
                    self.position[0] -= 14
            elif key_pressed == "right":
                if self.position[0] < game_boundary_right:
                    self.position[0] += 14


    def animateFrog(self, key_pressed, key_up):
        if self.animation_counter != 0:
            if self.animation_tick <= 0:
                self.moveFrog(key_pressed, key_up)
                self.animation_tick = 1
            else:
                self.animation_tick = self.animation_tick - 1

    def setPos(self, position):
        self.position = position

    def decLives(self):
        self.lives = self.lives - 1

    def cannotMove(self):
        self.can_move = 0

    def incAnimationCounter(self):
        self.animation_counter = self.animation_counter + 1
        if self.animation_counter == 3:
            self.animation_counter = 0
            self.can_move = 1

    def frogDead(self, game):
        self.setPositionToInitialPosition()
        self.decLives()  # Disminuir vidas
        update_lives(self)  # Actualizar la cantidad de vidas
        game.resetTime()  # Resetear el tiempo
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def setPositionToInitialPosition(self):
        self.position = [770, screen_height - 100]

    def draw(self):
        current_sprite = self.animation_counter * 60
        screen.blit(self.sprite, (self.position), (0 + current_sprite, 0, 60, 60 + current_sprite))

    def rect(self):
        return Rect(self.position[0], self.position[1], 60, 60)


def save_high_score(game):
    with open("high_score.txt", "w") as file:
        file.write(str(game.high_score))

def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0  # Si no se encuentra el archivo, el puntaje más alto será 0


    def moveFrog(self,key_pressed, key_up):
        #Tem que fazer o if das bordas da tela ainda
        #O movimento na horizontal ainda não ta certin
        if self.animation_counter == 0 :
            self.updateSprite(key_pressed)
        self.incAnimationCounter()
        if key_up == 1:
            if key_pressed == "up":
                if self.position[1] > 39:
                    self.position[1] = self.position[1]-13
            elif key_pressed == "down":
                if self.position[1] < 473:
                    self.position[1] = self.position[1]+13
            if key_pressed == "left":
                if self.position[0] > 2:
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0]-13
                    else:
                        self.position[0] = self.position[0]-14
            elif key_pressed == "right":
                if self.position[0] < 401:
                    if self.animation_counter == 2 :
                        self.position[0] = self.position[0]+13
                    else:
                        self.position[0] = self.position[0]+14

    def animateFrog(self,key_pressed,key_up):
        if self.animation_counter != 0 :
            if self.animation_tick <= 0 :
                self.moveFrog(key_pressed,key_up)
                self.animation_tick = 1
            else :
                self.animation_tick = self.animation_tick - 1

    def setPos(self,position):
        self.position = position

    def decLives(self):
        self.lives = self.lives - 1

    def cannotMove(self):
        self.can_move = 0

    def incAnimationCounter(self):
        self.animation_counter = self.animation_counter + 1
        if self.animation_counter == 3 :
            self.animation_counter = 0
            self.can_move = 1

    def frogDead(self, game):
        self.setPositionToInitialPosition()
        self.decLives()  # Disminuir vidas
        update_lives(self)  # Actualizar la cantidad de vidas
        game.resetTime()  # Resetear el tiempo
        self.animation_counter = 0
        self.animation_tick = 1
        self.way = "UP"
        self.can_move = 1

    def setPositionToInitialPosition(self):
        self.position = [207, 475]

    def draw(self):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite,(self.position),(0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self):
        return Rect(self.position[0],self.position[1],30,30)

class Enemy(Object):
    def __init__(self,position,sprite_enemy,way,factor):
        self.sprite = sprite_enemy
        self.position = position
        self.way = way
        self.factor = factor

    def move(self,speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed * self.factor
        elif self.way == "left":
            self.position[0] = self.position[0] - speed * self.factor


class Plataform(Object):
    def __init__(self, position, sprite_plataform, way):
        self.sprite = sprite_plataform
        self.position = position
        self.way = way
        self.collision_rect = Rect(self.position[0], self.position[1], sprite_plataform.get_width(), sprite_plataform.get_height())

    def move(self, speed):
        if self.way == "right":
            self.position[0] += speed  # Mueve la plataforma a la derecha
        elif self.way == "left":
            self.position[0] -= speed  # Mueve la plataforma a la izquierda
        
        # Actualiza el rectángulo de colisión
        self.collision_rect.topleft = self.position

    def draw(self):
        screen.blit(self.sprite, self.position)
        pygame.draw.rect(screen, (255, 0, 0), self.collision_rect, 2)  # Dibujar la caja de colisión en rojo

    def rect(self):
        return self.collision_rect






class Game():
    def __init__(self,speed,level):
        self.speed = speed
        self.level = level
        self.points = 0
        self.time = 30
        self.gameInit = 0
        self.high_score = load_high_score()  # Cargar el puntaje más alto al inicio

    def incLevel(self):
        self.level = self.level + 1

    def incSpeed(self):
        self.speed = self.speed + 1

    def incPoints(self, points):
        self.points = self.points + points
        if self.points > self.high_score:  # Si el puntaje actual es mayor que el más alto
            self.high_score = self.points
            save_high_score(self)  # Guardar el nuevo puntaje más alto

    def decTime(self):
        self.time = self.time - 1

    def resetTime(self):
        self.time = 30



#Funções gerais
def drawList(list):
    for i in list:
        i.draw()


def moveList(list,speed):
    for i in list:
        i.move(speed)

def destroyEnemys(list):
    for i in list:
        # Elimina el enemigo si se sale por el borde izquierdo (fuera de la pantalla)
        if i.position[0] + i.sprite.get_width() < 0:  # Si la posición + el ancho del enemigo es menor que 0
            list.remove(i)
        # Elimina el enemigo si se sale por el borde derecho (fuera de la pantalla)
        elif i.position[0] > screen_width:  # Si la posición del enemigo es mayor que el ancho de la pantalla
            list.remove(i)



def destroyPlataforms(list):
    """Destruye plataformas que han salido completamente de la pantalla."""
    for i in list[:]:  # Itera sobre una copia de la lista para evitar modificarla mientras iteramos
        if i.position[0] + i.sprite.get_width() < 0 or i.position[0] > screen_width:  
            list.remove(i)  # Elimina la plataforma cuando haya salido completamente de la pantalla



def createEnemys(list,enemys,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (40*game.speed)/game.level
                position_init = [screen_width - sprite_car1.get_width(), 705]  # Inicia en el borde derecho visible
                enemy = Enemy(position_init, sprite_car1, "left", 1)
                enemys.append(enemy)
            elif i == 1:
                list[1] = (30*game.speed)/game.level
                position_init = [-sprite_car1.get_width(), 645]  # entra por la izquierda
                enemy = Enemy(position_init, sprite_car2, "right", 2)
                enemys.append(enemy)
            elif i == 2:
                list[2] = (40*game.speed)/game.level
                position_init = [screen_width - sprite_car1.get_width(), 595]  # entra por la derecha
                enemy = Enemy(position_init, sprite_car3, "left", 2)
                enemys.append(enemy)
            elif i == 3:
                list[3] = (30*game.speed)/game.level
                position_init = [-sprite_car1.get_width(), 540]  # entra por la izquierda
                enemy = Enemy(position_init, sprite_car4, "right", 1)
                enemys.append(enemy)
            elif i == 4:
                list[4] = (50*game.speed)/game.level
                position_init = [screen_width - sprite_car1.get_width(), 475]  # entra por la derecha
                enemy = Enemy(position_init, sprite_car5, "left", 1)
                enemys.append(enemy)


def createPlataform(list, plataforms, game, homes):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:  # Tres tortugas en fila (primera fila)
                list[0] = (30 * game.speed) / game.level
                # Inicializar las tres tortugas al mismo tiempo en posiciones cercanas
                # Ajustamos las posiciones para que las tortugas estén separadas por una distancia pequeña
                position_init1 = [0, screen_height - 580]
                position_init2 = [55, screen_height - 580]   # Tortuga 2 al lado de la primera
                position_init3 = [110, screen_height - 580]   # Tortuga 3 al lado de la segunda
                plataform1 = Plataform(position_init1, sprite_turtle, "right")
                plataform2 = Plataform(position_init2, sprite_turtle, "right")
                plataform3 = Plataform(position_init3, sprite_turtle, "right")
                plataforms.append(plataform1)
                plataforms.append(plataform2)
                plataforms.append(plataform3) 

            elif i == 1:  # Tronco
                list[1] = (30 * game.speed) / game.level
                position_init = [1550, screen_height - 635]  # Posición ajustada para el tronco
                plataform = Plataform(position_init, sprite_plataform, "left")
                plataforms.append(plataform)

            elif i == 2:  # Tronco
                list[2] = (40 * game.speed) / game.level
                position_init = [1550, screen_height - 690]  # Posición ajustada para el tronco
                plataform = Plataform(position_init, sprite_plataform, "left")
                plataforms.append(plataform)

            elif i == 3:  # Dos tortugas en fila (cuarta fila)
                list[3] = (40 * game.speed) / game.level
                position_init1 = [0, screen_height - 750]  # Posición ajustada para tortugas
                position_init2 = [55, screen_height - 750]
                plataform1 = Plataform(position_init1, sprite_turtle, "right")
                plataform2 = Plataform(position_init2, sprite_turtle, "right")
                plataforms.append(plataform1)
                plataforms.append(plataform2)

            elif i == 4:  # Tronco
                list[4] = (20 * game.speed) / game.level
                position_init = [1550, screen_height - 810]  # Posición ajustada para tronco
                plataform = Plataform(position_init, sprite_plataform, "left")
                plataforms.append(plataform)


            # Agregar los arbustos en la parte inferior de la pantalla
            # Cambiar la posición de los arbustos a la parte superior de la pantalla

            position_init_home = [0, 0]  # Mover a la parte superior izquierda
            home_obj = Home(position_init_home, sprite_home)  # Crear el objeto de los arbustos
            homes.append(home_obj)  # Agregar a la lista de arbustos

            position_init_fill = [171, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_fill = [205, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_fill = [239, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_fill = [273, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_fill = [307, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_fill = [316, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)            

            position_init_home = [350, 0]  # Mover a la parte superior izquierda
            home_obj = Home(position_init_home, sprite_home)  # Crear el objeto de los arbustos
            homes.append(home_obj)  # Agregar a la lista de arbustos

            position_init_fill = [521, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos


            position_init_fill = [555, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos

            position_init_fill = [589, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos            

            position_init_fill = [623, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos    

            position_init_fill = [657, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos    

            position_init_fill = [680, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos    

            position_init_home = [715, 0]  # Mover a la parte superior izquierda
            home_obj = Home(position_init_home, sprite_home)  # Crear el objeto de los arbustos
            homes.append(home_obj)  # Agregar a la lista de arbustos

            position_init_fill = [880, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos  

            position_init_fill = [914, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos  

            position_init_fill = [948, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos  

            position_init_fill = [982, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos  

            position_init_fill = [1016, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos 

            position_init_fill = [1030, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos             

            position_init_home = [1065, 0]  # Mover a la parte superior izquierda
            home_obj = Home(position_init_home, sprite_home)  # Crear el objeto de los arbustos
            homes.append(home_obj)  # Agregar a la lista de arbustos   

            position_init_fill = [1235, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos       

            position_init_fill = [1269, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos     

            position_init_fill = [1303, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos                 

            position_init_fill = [1337, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos     

            position_init_fill = [1371, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos                 

            position_init_fill = [1395, 0]  # Mover a la parte superior izquierda
            fill_obj = Home(position_init_fill, sprite_fill)  # Crear el objeto de los arbustos
            homes.append(fill_obj)  # Agregar a la lista de arbustos

            position_init_home = [1415, 0]  # Mover a la parte superior izquierda
            home_obj = Home(position_init_home, sprite_home)  # Crear el objeto de los arbustos
            homes.append(home_obj)  # Agregar a la lista de arbustos                        



def frogOnTheStreet(frog,enemys,game):
    for i in enemys:
        enemyRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(enemyRect):
            hit_sound.play()
            frog.frogDead(game)

def frogInTheLake(frog, plataforms, game):
    seguro = 0
    wayPlataform = ""
    for i in plataforms:
        plataformRect = i.rect()
        frogRect = frog.rect()

        # Verifica si la rana está dentro del área de colisión de la plataforma
        if frogRect.colliderect(plataformRect):
            seguro = 1
            wayPlataform = i.way

            # Si la rana está en la plataforma, mueve la rana con la plataforma
            if wayPlataform == "right":
                frog.position[0] += game.speed  # Mueve la rana hacia la derecha con la plataforma
            elif wayPlataform == "left":
                frog.position[0] -= game.speed  # Mueve la rana hacia la izquierda con la plataforma

            # Evita que la rana se salga del agua o de la plataforma (ajuste en el eje vertical)
            if frog.position[1] > game_boundary_top:
                frog.position[1] -= 0  # Si se mueve en el eje vertical, corrige la posición si está fuera

    # Si la rana no está sobre ninguna plataforma, se considera que se ha caído al agua
    if seguro == 0:
        agua_sound.play()
        frog.frogDead(game)




def frogArrived(frog, chegam, game):
    # Iterar sobre las zonas seguras
    for zone in safe_zones:
        # Verifica si la posición de la rana está dentro de la zona segura (cuadro rojo)
        if zone.rect().colliderect(frog.rect()):
            # Si la rana entra en una zona segura, marca la llegada
            createArrived(frog, chegam, game, zone.position)
            return  # Salir de la función después de marcar la llegada

    # Si no está en ninguna zona segura, resetea la rana
    frog.position[1] = 46
    frog.animation_counter = 0
    frog.animation_tick = 1
    frog.can_move = 1

#borrar
def drawStreetAndLake():
    # Definir los límites de la calle, el lago y la zona de destino
    street_limit = screen_height - 525  # Ajuste del límite de la calle
    lake_limit = street_limit - 292  # Ajuste del límite superior del lago
    destination_limit = lake_limit - 70  # Ajuste del límite superior para la zona de destino

    # Dibujar un rectángulo verde para la calle
    pygame.draw.rect(screen, (0, 255, 0), (0, street_limit, screen_width, screen_height - street_limit))

    # Dibujar un rectángulo amarillo para el lago
    pygame.draw.rect(screen, (255, 255, 0), (0, lake_limit, screen_width, street_limit - lake_limit))

    # Dibujar un rectángulo morado para la zona de destino
    pygame.draw.rect(screen, (128, 0, 128), (0, destination_limit, screen_width, lake_limit - destination_limit))


def whereIsTheFrog(frog):

    street_limit = screen_height - 525  # Ajuste del límite de la calle

    # El límite superior del lago será la parte que está encima de la calle
    lake_limit = street_limit - 292  # Puede ajustarse según lo necesario

    # El destino de la rana es la parte superior de la pantalla, por debajo de un cierto espacio (por ejemplo, 40 píxeles)
    destination_limit = lake_limit-40  # Límite para la zona del destino

    if frog.position[1] > street_limit:  # En la calle (zona inferior de la pantalla)
        frogOnTheStreet(frog, enemys, game)
    elif frog.position[1] <= street_limit and frog.position[1] > lake_limit:  # En el lago (zona intermedia)
        frogInTheLake(frog, plataforms, game)
    elif frog.position[1] <= lake_limit and frog.position[1] > destination_limit:  # En la zona de destino
        frogArrived(frog, chegaram, game)


##BORRAR
class SafeZone(Object):
    def __init__(self, position):
        self.position = position
        self.size = 50  # Tamaño del cuadrado
        self.color = (255, 0, 0)  # Color rojo del cuadrado

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size, self.size))  # Dibuja el cuadrado en la pantalla

# Crear 5 zonas seguras con coordenadas iniciales
safe_zones = [
    SafeZone([60, screen_height-870]),  
    SafeZone([410, screen_height-870]),  
    SafeZone([775, screen_height-870]),  
    SafeZone([1125, screen_height-870]),  
    SafeZone([1478, screen_height-870]),  
]



# Load the image for the time bar (assuming a width of 100)
time_bar_image = pygame.Surface((100, 10))  # Time bar of width 100 and height 10
time_bar_image.fill((0, 255, 0))  # Green color for the time bar

# --- Cambios en la función que dibuja las ranas ---
# --- Cambios en la función que dibuja las ranas --- 
def draw_lives(frog, x_position, y_position):
    """Dibuja las ranas en la pantalla según las vidas restantes."""
    for i in range(frog.lives):  # Solo dibujar las ranas que correspondan a las vidas restantes
        screen.blit(sprite_tortuvida, (x_position + i * 35, y_position))  # Dibuja las ranas con espacio entre ellas


def update_lives(frog):
    """Actualizar las vidas cuando se pierda una."""
    if frog.lives < 0:
        frog.lives = 0  # Evitar que las vidas sean negativas

def draw_time_bar(game):
    """Dibuja la barra de tiempo que se reduce de izquierda a derecha."""
    time_left = game.time  # El tiempo actual en segundos
    total_time = 30  # Total de tiempo disponible (30 segundos en este caso)
    
    # El ancho total de la barra es de 100 píxeles, así que calculamos el ancho que debe tener la barra verde
    bar_width = int((time_left / total_time) * 100)  # La barra verde se reducirá según el tiempo restante

    # Dibuja la barra negra (fondo) primero, en x = 1400
    pygame.draw.rect(screen, (0, 0, 0), (1400, screen_height - 40, 100, 20))  # Barra negra de fondo
    
    # Luego dibuja la barra verde (tiempo restante) en x = 1400
    pygame.draw.rect(screen, (0, 255, 0), (1400, screen_height - 40, bar_width, 20))  # Barra verde que disminuye
    
    # Dibuja la palabra "TIME" a la derecha de la barra
    time_text = menu_font.render("TIME", True, (255, 255, 0))  # Color blanco para el texto
    screen.blit(time_text, (1500, screen_height - 38))  # Ajustamos la posición para que siempre esté a la derecha de la barra



def draw_score(game):
    # "HI-SCORE" en blanco y puntaje en rojo
    high_score_text = menu_font.render("HI-SCORE", True, (255, 255, 255))  # White for the text
    screen.blit(high_score_text, (screen_width - 710, 10))  # Adjust the position for "HI-SCORE"

    high_score_value_text = menu_font.render(f"{game.high_score:05d}", True, (255, 0, 0))  # Red for the score
    screen.blit(high_score_value_text, (screen_width - 690, 30))  # Adjust the position for the "HI-SCORE" score

    one_up_text = menu_font.render("1-UP", True, (255, 255, 255))  # White for the text
    screen.blit(one_up_text, (screen_width - 1040, 10))  # Adjust the position for "1-UP"

    one_up_value_text = menu_font.render(f"{game.points:05d}", True, (255, 0, 0))  # Red for the score
    screen.blit(one_up_value_text, (screen_width - 1060, 30))  # Adjust the position for the "1-UP" score


def createArrived(frog,chegaram,game,position_init):
    sapo_chegou = Object(position_init,sprite_arrived)
    chegaram.append(sapo_chegou)
    chegou_sound.play()
    frog.setPositionToInitialPosition()
    game.incPoints(10 + game.time)
    game.resetTime()
    frog.animation_counter = 0
    frog.animation_tick = 1
    frog.can_move = 1


def nextLevel(chegaram,enemys,plataforms,frog,game):
    if len(chegaram) == 5:
        chegaram[:] = []
        frog.setPositionToInitialPosition()
        game.incLevel()
        game.incSpeed()
        game.incPoints(100)
        game.resetTime()


trilha_sound.play(-1)
text_info = menu_font.render(('Press any button to start!'),1,(0,0,0))
gameInit = 0

while gameInit == 0:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            gameInit = 1

    screen.blit(background, (0, 0))
    screen.blit(text_info,(80,150))
    pygame.display.update()

while True:
    gameInit = 1
    game = Game(3, 1)
    key_up = 1
    frog_initial_position = [screen_width // 2 - sprite_sapo.get_width() // 2, screen_height - 100]
    frog = Frog(frog_initial_position, sprite_sapo)

    enemys = []
    plataforms = []
    chegaram = []
    ticks_enemys = [30, 0, 30, 0, 60]
    ticks_plataforms = [0, 0, 30, 30, 30]
    ticks_time = 30
    pressed_keys = 0
    key_pressed = 0

    while frog.lives > 0:

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYUP:
                key_up = 1
            if event.type == KEYDOWN:
                if key_up == 1 and frog.can_move == 1:
                    key_pressed = pygame.key.name(event.key)
                    frog.moveFrog(key_pressed, key_up)
                    frog.cannotMove()

        if not ticks_time:
            ticks_time = 30
            game.decTime()
        else:
            ticks_time -= 1

        if game.time == 0:
            frog.frogDead(game)

        drawStreetAndLake() 
        createEnemys(ticks_enemys, enemys, game)
        createPlataform(ticks_plataforms, plataforms, game, homes)  # Pasar la lista de arbustos

        moveList(enemys, game.speed)
        moveList(plataforms, game.speed)

        whereIsTheFrog(frog)

        nextLevel(chegaram, enemys, plataforms, frog, game)

        screen.blit(background, (0, 0))  #aaaaaaa
        #screen.blit(text_info1, (10, 520))

        for zone in safe_zones:
            zone.draw()  # Dibuja cada cuadro en la pantalla

        # Dibuja las vidas restantes
        draw_lives(frog, 40, screen_height - 50)
        # Dibuja los enemigos, plataformas y arbustos
        drawList(enemys)
        drawList(plataforms)
        drawList(chegaram)
        drawList(homes)  # Dibuja los arbustos
        draw_time_bar(game)

        frog.animateFrog(key_pressed, key_up)
        frog.draw()

        destroyEnemys(enemys)
        destroyPlataforms(plataforms)

        # Dibuja la puntuación actual y la puntuación más alta en la parte superior
        draw_score(game)

        pygame.display.update()
        time_passed = clock.tick(30)


    while gameInit == 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                gameInit = 0

        screen.blit(background, (0, 0))
        text = game_font.render('GAME OVER', 1, (255, 0, 0))
        text_points = game_font.render(('Score: {0}'.format(game.points)), 1, (255, 0, 0))
        text_reiniciar = info_font.render('Press any button to reset!', 1, (255, 0, 0))
        screen.blit(text, (75, 120))
        screen.blit(text_points, (10, 170))
        screen.blit(text_reiniciar, (70, 250))



        pygame.display.update()