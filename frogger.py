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

screen = pygame.display.set_mode((448,546), 0, 32)


# Load the custom font
font_path = './frogger/Fonts/bit5x3.ttf'  # Update this to the correct path where your font is located
game_font = pygame.font.Font(font_path, 30)  # For the main game font
info_font = pygame.font.Font(font_path, 30)  # For the info font
menu_font = pygame.font.Font(font_path, 30)  # For the menu font


# --- Carregando imagens ---
background_filename = './frogger/images/bg2.png'
frog_filename = './frogger/images/sprite_sheets_up.png'
arrived_filename = './frogger/images/frog_arrived.png'
car1_filename = './frogger/images/car1.png'
car2_filename = './frogger/images/car2.png'
car3_filename = './frogger/images/car3.png'
car4_filename = './frogger/images/car4.png'
car5_filename = './frogger/images/car5.png'
plataform_filename = './frogger/images/tronco2.png'
turtle_filename = './frogger/images/Turtle_03.png'  # Nueva imagen de tortuga
home_filename = './frogger/images/Home.png'  # Imagen de los arbustos
fill_filename = './frogger/images/relleno.png'  # Ruta a la imagen de relleno

tortu_vida = './frogger/images/frog_arrived.png'  # Ruta a la imagen de relleno


frog_image = pygame.image.load(frog_filename).convert_alpha()
background = pygame.image.load(background_filename).convert()
sprite_sapo = pygame.image.load(frog_filename).convert_alpha()
sprite_arrived = pygame.image.load(arrived_filename).convert_alpha()
sprite_car1 = pygame.transform.scale(pygame.image.load(car1_filename).convert_alpha(), (38, 30))
sprite_car2 = pygame.transform.scale(pygame.image.load(car2_filename).convert_alpha(), (38, 30))
sprite_car3 = pygame.transform.scale(pygame.image.load(car3_filename).convert_alpha(), (38, 30))
sprite_car4 = pygame.transform.scale(pygame.image.load(car4_filename).convert_alpha(), (38, 30))
sprite_car5 = pygame.transform.scale(pygame.image.load(car5_filename).convert_alpha(), (55, 30))
sprite_plataform = pygame.transform.scale(pygame.image.load(plataform_filename).convert_alpha(), (100, 30))
sprite_turtle = pygame.transform.scale(pygame.image.load(turtle_filename).convert_alpha(), (30, 30))  # Escalar la tortuga si es necesario
# Escalar la imagen del arbusto a un tamaño mayor
sprite_home = pygame.transform.scale(pygame.image.load('./frogger/images/Home.png').convert_alpha(), (70, 30))  # Cambiar dimensiones
# --- Escalar la imagen de relleno ---
sprite_fill = pygame.transform.scale(pygame.image.load('./frogger/images/relleno.png').convert_alpha(), (50, 29))  # Ajustar el tamaño
sprite_tortuvida= pygame.image.load(tortu_vida).convert_alpha()
sprite_tortuvida = pygame.transform.flip(sprite_tortuvida, False, True)
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
                frog_filename = './frogger/images/sprite_sheets_up.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "down":
                frog_filename = './frogger/images/sprite_sheets_down.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "left":
                frog_filename = './frogger/images/sprite_sheets_left.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()
            elif self.way == "right":
                frog_filename = './frogger/images/sprite_sheets_right.png'
                self.sprite = pygame.image.load(frog_filename).convert_alpha()

    def moveFrog(self, key_pressed, key_up):
        if self.animation_counter == 0:
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
                    if self.animation_counter == 2:
                        self.position[0] = self.position[0]-13
                    else:
                        self.position[0] = self.position[0]-14
            elif key_pressed == "right":
                if self.position[0] < 401:
                    if self.animation_counter == 2:
                        self.position[0] = self.position[0]+13
                    else:
                        self.position[0] = self.position[0]+14

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
        self.position = [207, 475]

    def draw(self):
        current_sprite = self.animation_counter * 30
        screen.blit(self.sprite, (self.position), (0 + current_sprite, 0, 30, 30 + current_sprite))

    def rect(self):
        return Rect(self.position[0], self.position[1], 30, 30)


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

    def move(self, speed):
        if self.way == "right":
            self.position[0] = self.position[0] + speed  # Troncos van a la derecha
        elif self.way == "left":
            self.position[0] = self.position[0] - speed  # Tortugas van a la izquierda


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
        if i.position[0] < -80:
            list.remove(i)
        elif i.position[0] > 516:
            list.remove(i)

def destroyPlataforms(list):
    for i in list:
        if i.position[0] < -100:
            list.remove(i)
        elif i.position[0] > 448:
            list.remove(i)

def createEnemys(list,enemys,game):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:
                list[0] = (40*game.speed)/game.level
                position_init = [506, 436]  # entra por la derecha
                enemy = Enemy(position_init, sprite_car1, "left", 1)
                enemys.append(enemy)
            elif i == 1:
                list[1] = (30*game.speed)/game.level
                position_init = [-80, 397]  # entra por la izquierda
                enemy = Enemy(position_init, sprite_car2, "right", 2)
                enemys.append(enemy)
            elif i == 2:
                list[2] = (40*game.speed)/game.level
                position_init = [506, 357]  # entra por la derecha
                enemy = Enemy(position_init, sprite_car3, "left", 2)
                enemys.append(enemy)
            elif i == 3:
                list[3] = (30*game.speed)/game.level
                position_init = [-80, 318]  # entra por la izquierda
                enemy = Enemy(position_init, sprite_car4, "right", 1)
                enemys.append(enemy)
            elif i == 4:
                list[4] = (50*game.speed)/game.level
                position_init = [506, 280]  # entra por la derecha
                enemy = Enemy(position_init, sprite_car5, "left", 1)
                enemys.append(enemy)


def createPlataform(list, plataforms, game, homes):
    for i, tick in enumerate(list):
        list[i] = list[i] - 1
        if tick <= 0:
            if i == 0:  # Tres tortugas en fila (primera fila)
                list[0] = (30*game.speed)/game.level
                position_init1 = [-100, 200]
                position_init2 = [-70, 200]  # Tortuga 2 al lado de la primera
                position_init3 = [-40, 200]  # Tortuga 3 al lado de la segunda
                plataform1 = Plataform(position_init1, sprite_turtle, "right")
                plataform2 = Plataform(position_init2, sprite_turtle, "right")
                plataform3 = Plataform(position_init3, sprite_turtle, "right")
                plataforms.append(plataform1)
                plataforms.append(plataform2)
                plataforms.append(plataform3)

            elif i == 1:  # Tronco
                list[1] = (30*game.speed)/game.level
                position_init = [448, 161]
                plataform = Plataform(position_init, sprite_plataform, "left")  # Tortuga va a la izquierda
                plataforms.append(plataform)

            elif i == 2:  # Tronco
                list[2] = (40*game.speed)/game.level
                position_init = [448, 122]
                plataform = Plataform(position_init, sprite_plataform, "left")
                plataforms.append(plataform)

            elif i == 3:  # Dos tortugas en fila (cuarta fila)
                list[3] = (40*game.speed)/game.level
                position_init1 = [-100, 83]  # Tortuga 1 en la cuarta fila
                position_init2 = [-70, 83]  # Tortuga 2 al lado de la primera
                plataform1 = Plataform(position_init1, sprite_turtle, "right")
                plataform2 = Plataform(position_init2, sprite_turtle, "right")  # Mover a la derecha
                plataforms.append(plataform1)
                plataforms.append(plataform2)

            elif i == 4:  # Tronco
                list[4] = (20*game.speed)/game.level
                position_init = [448, 44]
                plataform = Plataform(position_init, sprite_plataform, "left")
                plataforms.append(plataform)

            # Agregar los arbustos en la parte inferior de la pantalla
            # Cambiar la posición de los arbustos a la parte superior de la pantalla
            position_init_fill = [0, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_fill = [10, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_home = [22.5, 0]  # Mover a la parte superior izquierda
            home_obj = Home(position_init_home, sprite_home)  # Crear el objeto de los arbustos
            homes.append(home_obj)  # Agregar a la lista de arbustos

            position_init_fill = [90, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)


                        # Agregar el segundo arbusto después del primero
            position_init_home2 = [104, 0]  # Mover un poco más a la derecha
            home_obj2 = Home(position_init_home2, sprite_home)  # Crear el segundo objeto de los arbustos
            homes.append(home_obj2)  # Agregar el segundo arbusto


            position_init_fill = [174, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)


            position_init_home3 = [188, 0]  # Mover un poco más a la derecha
            home_obj3 = Home(position_init_home3, sprite_home)  # Crear el segundo objeto de los arbustos
            homes.append(home_obj3)  # Agregar el segundo arbusto
 
            position_init_fill = [256, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_home4 = [270, 0]  # Mover un poco más a la derecha
            home_obj4 = Home(position_init_home4, sprite_home)  # Crear el segundo objeto de los arbustos
            homes.append(home_obj4)  # Agregar el segundo arbusto

            position_init_fill = [336, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)            

            position_init_home5 = [350, 0]  # Mover un poco más a la derecha
            home_obj5 = Home(position_init_home5, sprite_home)  # Crear el segundo objeto de los arbustos
            homes.append(home_obj5)  # Agregar el segundo arbusto            

            position_init_fill = [420, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)   

            position_init_fill = [430, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

            position_init_fill = [440, 0]  # Coloca el relleno después del primer arbusto
            fill_obj = Object(position_init_fill, sprite_fill)  # Crear el objeto de relleno
            homes.append(fill_obj)

# def carChangeRoad(enemys):
#     enemy = Random.choice(enemys)
#     initialPosition = enemy.position[1]

#     choice = Random.randint(1,2)
#     if (choice % 2 == 0):
#         enemy.position[1] = enemy.position[1] + 39
#     else :
#         enemy.position[1] = enemy.position[1] - 39

#     if enemy.position[1] > 436:
#         enemy.position[1] = initialPosition
#     elif enemy.position[1] < 280:
#         enemy.position[1] = initialPosition


def frogOnTheStreet(frog,enemys,game):
    for i in enemys:
        enemyRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(enemyRect):
            hit_sound.play()
            frog.frogDead(game)

def frogInTheLake(frog,plataforms,game):
    #se o sapo esta sob alguma plataforma Seguro = 1
    seguro = 0
    wayPlataform = ""
    for i in plataforms:
        plataformRect = i.rect()
        frogRect = frog.rect()
        if frogRect.colliderect(plataformRect):
            seguro = 1
            wayPlataform = i.way

    if seguro == 0:
        agua_sound.play()
        frog.frogDead(game)

    elif seguro == 1:
        if wayPlataform == "right":
            frog.position[0] = frog.position[0] + game.speed

        elif wayPlataform == "left":
            frog.position[0] = frog.position[0] - game.speed

def frogArrived(frog,chegaram,game):
    if frog.position[0] > 33 and frog.position[0] < 53:
        position_init = [43,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 115 and frog.position[0] < 135:
        position_init = [125,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 197 and frog.position[0] < 217:
        position_init = [207,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 279 and frog.position[0] < 299:
        position_init = [289,7]
        createArrived(frog,chegaram,game,position_init)

    elif frog.position[0] > 361 and frog.position[0] < 381:
        position_init = [371,7]
        createArrived(frog,chegaram,game,position_init)

    else:
        frog.position[1] = 46
        frog.animation_counter = 0
        frog.animation_tick = 1
        frog.can_move = 1


def whereIsTheFrog(frog):
    #Se o sapo ainda não passou da estrada
    if frog.position[1] > 240 :
        frogOnTheStreet(frog,enemys,game)

    #Se o sapo chegou no rio
    elif frog.position[1] < 240 and frog.position[1] > 40:
        frogInTheLake(frog,plataforms,game)

    #sapo chegou no objetivo
    elif frog.position[1] < 40 :
        frogArrived(frog,chegaram,game)


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

    # Dibuja la barra negra (fondo) primero
    pygame.draw.rect(screen, (0, 0, 0), (285, 520, 100, 20))  # Barra negra de fondo
    
    # Luego dibuja la barra verde (tiempo restante)
    pygame.draw.rect(screen, (0, 255, 0), (285, 520, bar_width, 20))  # Barra verde que disminuye
    
    # Dibuja la palabra "TIME" a la derecha de la barra
    time_text = menu_font.render("TIME", True, (255, 255, 0))  # Color blanco para el texto
    screen.blit(time_text, (385, 518))  # Ajustamos la posición para que siempre esté a la derecha de la barra


def draw_score(game):
    # "HI-SCORE" en blanco y puntaje en rojo
    high_score_text = menu_font.render("HI-SCORE", True, (255, 255, 255))  # White for the text
    screen.blit(high_score_text, (280, 10))  # Adjust the position for "HI-SCORE"

    high_score_value_text = menu_font.render(f"{game.high_score:05d}", True, (255, 0, 0))  # Red for the score
    screen.blit(high_score_value_text, (300, 30))  # Adjust the position for the "HI-SCORE" score

    one_up_text = menu_font.render("1-UP", True, (255, 255, 255))  # White for the text
    screen.blit(one_up_text, (120, 10))  # Adjust the position for "1-UP"

    one_up_value_text = menu_font.render(f"{game.points:05d}", True, (255, 0, 0))  # Red for the score
    screen.blit(one_up_value_text, (105, 30))  # Adjust the position for the "1-UP" score


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
    frog_initial_position = [207, 475]
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

        createEnemys(ticks_enemys, enemys, game)
        createPlataform(ticks_plataforms, plataforms, game, homes)  # Pasar la lista de arbustos

        moveList(enemys, game.speed)
        moveList(plataforms, game.speed)

        whereIsTheFrog(frog)

        nextLevel(chegaram, enemys, plataforms, frog, game)

        # Mostrar los puntos actuales en la parte inferior
        #text_info1 = info_font.render(('Points: {1}'.format(game.level, game.points)), 1, (255, 255, 255))
        
        # Redibujar la pantalla con fondo y puntajes
        screen.blit(background, (0, 0))
        #screen.blit(text_info1, (10, 520))

        # Dibuja las vidas restantes
        draw_lives(frog, 10, 520)
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
        text_points = game_font.render(('Pontuação: {0}'.format(game.points)), 1, (255, 0, 0))
        text_reiniciar = info_font.render('Pressione qualquer tecla para reiniciar!', 1, (255, 0, 0))
        screen.blit(text, (75, 120))
        screen.blit(text_points, (10, 170))
        screen.blit(text_reiniciar, (70, 250))

        pygame.display.update()
