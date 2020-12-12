
from typing import Text
import pygame as pg
import random
import pygame
from math import *
from time import *
import threading
from pygame.constants import K_w
from sprites import *
from settings import *
from PlayerSocket import * 
from TokenSocket import * 
from threading import *
from collections import namedtuple
from json import JSONEncoder
import socket as sk
import json
import sys

vec = pg.math.Vector2
bgs = ['resources/bg.jpg', 'resources/background2.jpg']
my_timer = 5

host = "127.0.0.1"
port = 6666
flag = True
format = "utf8"
bts = 4096

firstMessage = "Connected"



class Game():
    #Se encarga de iniciar la ventana del juego y cargar los datos pertenecientes a este.
    
    def __init__(self,player1_socket, player2_socket):
        # inicializa la ventana 
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.my_timer = 5
        self.load_data()
        ###################  SOCKET SIDE ##################
        self.port = port
        self.flag = True
        self.host = host
        self.request = sk.socket()
        self.request.connect((self.host, self.port))
        self.sendMessage(firstMessage)
        self.decoded = ""
        self.player1_socket = player1_socket # Jugador uno creado en la GUI
        self.player2_socket = player2_socket # Jugador dos creado en la GUI
        self.mainTokens = [] #Lista de tokens principales del reto
        self.fillerTokens = [] #Lista de tokens de relleno
        self.onGame = False
        self.level = 0
        self.depth  = 0
        self.order = 0
        self.numElements = 0
        

        

        ################ END SOCKET SIDE ############


        ############### SOCKET METHODS ###########

    def sendMessage(self, message):
        self.message = message
        print("Enviar:", self.message)
        self.out = self.message.encode(format)
        print("Salida antes de enviar:", self.out.decode(format))
        self.sending = self.request.send(self.out)
        print("Se han enviado: {} bytes al servidor.".format(self.sending))


    #Método para procesar los mensajes que mande el server
   
    def processReceived(self, message):
        self.message = message
        try:
            if "Challenges" in self.message:  
                message_dict = json.loads(self.message)          
                with open('JsonResources/CurrentChallenge.json', 'w') as json_file:
                    json.dump(message, json_file) 
                print(json.dumps(message_dict))
                self.mainTokens = []
                self.fillerTokens = []
                self.readChallenge(self.mainTokens, self.fillerTokens)
                tokenToSend = self.mainTokens[0]
                self.sendToken(tokenToSend, self.player1_socket.getID())

            elif self.message == "exit":
                self.sendMessage("exit")
                self.flag = False
                self.request.close()
                print("Terminado")
            
            elif self.message == "True":
                self.setOnGame(True)
                print("Iniciar temporizador")
                print("\n")

            elif "player1" in self.message:
                self.updatePlayerScore(self.player1_socket, self.message)
                print("El puntaje actual es: ")
                print(self.player1_socket.getScore())

            elif "player2" in self.message:
                self.updatePlayerScore(self.player2_socket, self.message)
                print("El puntaje actual es: ")
                print(self.player2_socket.getScore())
                print("\n")

            elif "depth" in self.message:
                splitted_message = self.message.split(":") 
                newDepth = int(splitted_message[1])
                self.setDepth(newDepth)
                print("La profundidad es: " + str(self.getDepth))
                print("\n")
            elif "Order" in self.message and "Level" in self.message:
                splitted_message = self.message.split(":")
                order = int(splitted_message[1])
                level = int(splitted_message[3])
                self.setOrder(order)
                self.setLevel(level)  
                print("El orden del BTree es: " + str(self.getOrder()))
                print("El nivel del BTree es: " + str(self.getLevel()))
                print("\n")

            elif "numElements" in self.message:
                splitted_message = self.message.split(":") 
                newNumElements = int(splitted_message[1])
                self.setNumElements(newNumElements)
                print("La cantidad de elementos del arbol es: " + str(self.getNumElements()))
                print("\n")

            else:
                print(self.message)    
        except IOError as e:
            print(e)
#----------------------------------Bloque de getters----------------------------------#
    def getOnGame(self):
        return self.getOnGame
    def getMainTokens(self):
        return self.mainTokens
    def getFillerTokens(self):
        return self.fillerTokens   
    def getLevel(self):
        return self.level
    def getOrder(self):
        return self.order
    def getDepth(self):
        return self.depth   
    def getNumElements(self):
        return self.numElements

    #----------------------------------Bloque de setters----------------------------------#
    def setMainTokens(self, mainTokens):
        self.mainTokens = mainTokens
    def setFillerTokens(self, fillerTokens):
        self.fillerTokens = fillerTokens
    def setOnGame(self, boolean):
        self.onGame = boolean      
    def setLevel(self, level):
        self.level = level
    def setOrder(self, order):
        self.order = order
    def setDepth(self, depth):
        self.depth = depth
    def setNumElements(self, numElements):
        self.numElements = numElements

    #--------------------------Actualizar el puntaje del jugador--------------------------#
    def updatePlayerScore(self, player, message):
        splitted_Info =  message.split(":")
        print("La info del puntaje es")
        print(splitted_Info)
        #currentScore = int(splitted_Info[1])
        #player.setScore(currentScore)

    #-------------------------------------------------------------------------------------#
    #Método que recibe un token y una id de jugador y que retorna un 
    # mensaje formato json para mandarlo al server
    def sendToken(self, Token, playerID):
        data = {
            "ID" + str(playerID):{
                "Token": {
                    "shape": Token.getShape(),
                    "value": Token.getVal(),
                    "points": Token.getPoints()
                }
            }
        }
        with open('JsonResources/CurrentToken.json', 'w') as write_file:
            json.dump(data, write_file)
        message = json.dumps(data)
        self.sendMessage(message)
        print(message)
        return message

    #-------------------------------------------------------------------------------------#    
    #Método que toma un diccionario con info de token para parsearlo a objeto de Python
    def jsonToToken(self, tokenDict): 
        return namedtuple('Token', tokenDict.keys())(*tokenDict.values())
#-------------------------------------------------------------------------------------#
#-------------------------------------------------------------------------------------#
    #Esta función se encarga de leer el json donde están los tokens de ese reto
    #estos tokens se agregan a las listas mainTokens y fillerTokens
    def readChallenge(self, mainTokens, fillerTokens):
        file_path = 'JsonResources/CurrentChallenge.json'
        with open(file_path,'r') as read_file:
            data = json.load(read_file)

        data_dict = json.loads(data)
        #mainTokens_dict
        mainTokens_dict = data_dict["Challenges"]["MainTokens"]
        fillerTokens_dict = data_dict["Challenges"]["FillerTokens"]
        #Agregando main tokens
        for key in mainTokens_dict:
            token_dict = mainTokens_dict.get(key)
            token_string = json.dumps(token_dict)
            token_object = json.loads(token_string, object_hook=self.jsonToToken)
            myFinalToken = TokenSocket(token_object.value, token_object.shape, token_object.points)
            mainTokens.append(myFinalToken)
        #Agregando filler tokens
        for key in fillerTokens_dict:
            token_dict = fillerTokens_dict.get(key)
            token_string = json.dumps(token_dict)
            token_object = json.loads(token_string, object_hook=self.jsonToToken)
            myFinalToken = TokenSocket(token_object.value, token_object.shape, token_object.points)
            fillerTokens.append(myFinalToken) 
        for token in range(len(fillerTokens)):
            print(fillerTokens[token].getPoints())
        
        self.setMainTokens(mainTokens)
        self.setFillerTokens(fillerTokens)
#-------------------------------------------------------------------------------------#    



    def load_data(self):
        self.spritesheet = Spritesheet("resources/megamanstand.png")


    #Se encarga de cargar los sprites de los componentes importantes del juego(proyectiles,
    #jugadores, plataformas, entre otros) y se llama al metodo run().
    def new(self):
        # inicia un nuevo juego 
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.temp_platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.projectiles_megaman = pg.sprite.Group()
        self.projectiles_samus = pg.sprite.Group()
        self.tokens = pg.sprite.Group()
        self.playerslist = pg.sprite.Group()
        self.powerupslist = [] 
        self.tokens_list = []
        self.powerup_shield = pg.sprite.Group()
        self.powerup_shoot = pg.sprite.Group()
        self.powerup_push = pg.sprite.Group()
        self.powerup_airjump = pg.sprite.Group()
        self.powerup_temp_platform = pg.sprite.Group()
        self.powerup_faster = pg.sprite.Group()
        self.powerup_extrapoints = pg.sprite.Group()
        self.player = Player(self,1)
        self.player2 = Player(self,2)
        #self.token = Token(self,2,"Diamond")
        #self.draw_text("Vidas: " + str(self.player.lives), 10, (0,0,0), 40, 20)
        #self.all_sprites.add(self.player2)
        #self.all_sprites.add(self.player)
        Platform(self,*PLATFORM_LIST[0],0,"first")
        Platform(self,*PLATFORM_LIST[1],1,"first")
        Platform(self,*PLATFORM_LIST[2],1,"first")
        Platform(self,*PLATFORM_LIST[3],1,"first")
        Platform(self,*PLATFORM_LIST[5],1,"first")
        Platform(self,*PLATFORM_LIST[6],2,"first")
        Platform(self,*PLATFORM_LIST[7],2,"first")
        self.run()

    #Llama a otros metodos que se encargan de la parte funcional del juego.
    def run(self):
        # Game Loop para la partida 
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            try:
                self.decoded = self.request.recv(bts).decode(format)
                self.processReceived(self.decoded)
            except IOError as e:
                print(e)

            
    
    #En este metodo se crean los hitbox para los dos jugadores(toma en cuenta los power ups).
    def update(self):
        # actualiza los sprites 
        self.all_sprites.update()
        #revisa si el jugador colisiona con una plataforma, solo si esta cayendo
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)
            shots = pg.sprite.spritecollide(self.player2, self.projectiles_megaman, True)
            pwrpshots = pg.sprite.spritecollide(self.player, self.powerup_shoot, True)
            shield = pg.sprite.spritecollide(self.player2, self.powerup_shield, True)
            push = pg.sprite.spritecollide(self.player, self.powerup_push, True)
            temp_platform = pg.sprite.spritecollide(self.player, self.powerup_temp_platform,True)

            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit 
                
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top + 1
                        self.player.vel.y = 0
                        self.player.jumping = False

            if shots:                
                self.player2.activated = True #Futura condición para el power up 'shield'
                for shot in shots:
                    if self.player.pos.x < self.player2.pos.x: #En caso que el jugador 1 este a la  izquierda del jugador 2
                        if shield:
                            self.player2.pos.x += 0  #Hitbox en caso de disparo
                            shot.kill()
                        elif pwrpshots:
                            self.player2.pos.x += 10  #Hitbox en caso de disparo
                            shot.kill()
                    elif self.player.pos.x >= self.player2.pos.x: #En caso que el jugador 1 este a la derecha del jugador 2
                        if shield:
                            self.player2.pos.x -= 0  #Hitbox en caso de disparo
                            shot.kill()
                        elif pwrpshots:
                            self.player2.pos.x -= 10  #Hitbox en caso de disparo
                            shot.kill()

                shape = random.choice(["diamond","triangle","circle","square"])
                rand_num = random.randrange(1,100)
                self.token = Token(self,rand_num,shape)
                print(len(self.tokens_list))

                for token in self.tokens_list:
                    if self.isColliding(self.player2.pos.x,self.player2.pos.y,token.pos.x,token.pos.y):
                        print("Colliding with token " + token.shape + " Value is: " + str(token.value))
                        self.tokens_list.remove(token)
                        token.kill()
            
            #push
            if push:
                if self.isColliding(self.player.pos.x, self.player.pos.y, self.player2.pos.x, self.player2.pos.y):
                    if self.player.pos.x < self.player2.pos.x:
                        self.player2.pos.x += 8
                    elif self.player.pos.x >= self.player2.pos.x:
                        self.player2.pos.x -= 8

            if temp_platform:
                Platform(self,*PLATFORM_LIST[4],1,"second")
                
 
        if self.player.rect.bottom > HEIGHT:

            #for sprite in self.all_sprites:
            #sprite.rect.y -= max(self.player.vel.y,10)            
            if self.player.lives != 1:    
                self.player.lives -= 1
                self.player.pos = vec(600, 300)   
                self.player.vel = vec(0,0)
                self.player.acc = vec(0,0)                                                
            else:
                self.max_go_screen()
                self.playing = False
            


        if self.player2.vel.y > 0:
            hits2 = pg.sprite.spritecollide(self.player2,self.platforms,False)
            shots2 = pg.sprite.spritecollide(self.player,self.projectiles_samus,True)
            pwrpshots2 = pg.sprite.spritecollide(self.player2, self.powerup_shoot, True)
            shield2 = pg.sprite.spritecollide(self.player, self.powerup_shield, True)
            push2 = pg.sprite.spritecollide(self.player2, self.powerup_push, True)
            if hits2:
                lowest2 = hits2[0]
                for hit in hits2:
                    if hit.rect.bottom > lowest2.rect.bottom:
                        lowest2 = hit
                
                if self.player2.pos.y < lowest2.rect.centery:
                    self.player2.pos.y = lowest2.rect.top + 1
                    self.player2.vel.y = 0
                    self.player2.samus_jumping = False


            if shots2:
                self.player.activated = True #Futura condición para el power up 'shield'
                for shot in shots2: 
                    if self.player2.pos.x < self.player.pos.x: #En caso que el jugador 1 esté a la  izquierda del jugador 2
                        if shield2:
                            self.player.pos.x += 0  #Hitbox en caso de disparo
                            shot.kill()
                        elif pwrpshots2:
                            self.player.pos.x += 10  #Hitbox en caso de disparo
                            shot.kill()
                    elif self.player2.pos.x >= self.player.pos.x: #En caso que el jugador 1 esté a la derecha del jugador 2
                        if shield2:
                            self.player.pos.x -= 0  #Hitbox en caso de disparo
                            shot.kill()
                        elif pwrpshots2:
                            self.player.pos.x -= 10  #Hitbox en caso de disparo
                            shot.kill()
            
            #push
            if push2:
                if self.isColliding(self.player2.pos.x, self.player2.pos.y, self.player.pos.x, self.player.pos.y):
                    if self.player2.pos.x < self.player.pos.x:
                        self.player.pos.x += 8
                    elif self.player2.pos.x >= self.player.pos.x:
                        self.player.pos.x -= 8


            
            

        #si el jugador se cae de una plataforma 
        # añadir las vidas del jugador y descontar una vida cuando se cae de una plataforma
        if self.player2.rect.bottom > HEIGHT:
            #for sprite in self.all_sprites:
            #sprite.rect.y -= max(self.player.vel.y,10)            
            if self.player2.lives != 1:    
                self.player2.lives -= 1
                self.player2.pos = vec(600, 300)   
                self.player2.vel = vec(0,0)
                self.player2.acc = vec(0,0)                                                
            else:
                self.show_go_screen()
                self.playing = False
        
    #En este metodo se establecen las acciones de cada boton.
    def events(self):
        # Game Loop - eventos de pygame 
        for event in pg.event.get():
            # revisa si la ventana ha sido cerrada 
            airjump = pg.sprite.spritecollide(self.player,self.powerup_airjump,True)
            airjump2 = pg.sprite.spritecollide(self.player2,self.powerup_airjump,True)
            faster = pg.sprite.spritecollide(self.player, self.powerup_faster, True)
            faster2 = pg.sprite.spritecollide(self.player2, self.powerup_faster, True)
           
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
                                                     

            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jump(15)
                elif event.key == pg.K_w:
                    self.player2.jump(15)
                elif event.key == pg.K_s:
                    if self.player2.left:
                        facing2 = -1
                    elif self.player2.right:
                        facing2 = 1
                    
                    Projectiles(self,self.player2, facing2)

                elif event.key == pg.K_DOWN:
                    if self.player.left:
                        facing = -1
                    elif self.player.right:
                        facing = 1
                    
                    Projectiles(self,self.player, facing)

            
            if airjump:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        self.player.jump(20)


            if airjump2:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_w:
                        self.player2.jump(20)

            if faster:
                if event.type == pg.KEYUP:
                    if event.key == pg.K_RIGHT: 
                        self.player.vel.x += 15 
                    elif event.key == pg.K_LEFT:
                        self.player.vel.x -= 15 

            if faster2:
                if event.type == pg.KEYUP:
                    if event.key == pg.K_d: 
                        self.player2.vel.x += 15 
                    elif event.key == pg.K_a:
                        self.player2.vel.x -= 15 
                
                
                """        
                elif event.key == pg.K_v: #crea plataforma random
                    Platform(self,*PLATFORM_LIST[4],2)
                """
            
                
            
    #Es una funcion donde se crea un hitbox alternativo para cuando los dos jugadores agarren el power up 'push' 
    #y asi se puedan empujar en caso que choquen.
    def isColliding(self, player2x, player2y, playerx, playery):
        distance = sqrt((pow(player2x-playerx,2))+(pow(player2y-playery,2)))
        if distance < 80:
            return True
        else:
            return False         

    #Muestra en pantalla la imagen de fondo, puntajes y cantidad de vidas de ambos jugadores.
    def draw(self):
        #Game Loop - dibuja en la ventana 
        self.bg = pg.image.load(bgs[0])
        self.screen.blit(self.bg,(0,0))
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text("Megaman lives: " + str(self.player.lives), 20, (0,0,0), 80, 20)
        self.draw_text("Samus lives: " + str(self.player2.lives), 20, (0,0,0), 1100, 20)
        self.draw_text("Samus score: " + str(self.player2.score), 20, (0,0,0), 1100, 50)
        self.draw_text("Megaman score: " + str(self.player.score), 20, (0,0,0), 80, 50)
        # despues de dibujar o mostrar elementos en pantalla, actualiza la ventana
        pg.display.flip()

    def show_start_screen(self):
        # ventana de inicio 
        self.screen.fill(LIGHTBLUE)
        self.draw_text("Game Over",48, BLACK, WIDTH/2, HEIGHT/4)
        pass

    #Una vez que se hayan agotado las vidas del jugador 2(samus), 
    #se muestra en pantalla los puntajes finales y que el jugador 1(megaman) gano. 
    #Tambien si presiona una tecla, se inicia una nueva partida.
    def show_go_screen(self):
        # game over 
        if not self.running:
            return 
        self.screen.fill(LIGHTBLUE)
        self.draw_text("GAME OVER      Megaman wins!",48, WHITE, WIDTH/2, HEIGHT/8)
        self.draw_text("Samus Score: " + str(self.player2.score), 22,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("Megaman Score: " + str(self.player.score), 22,WHITE,WIDTH/2,HEIGHT/3)
        self.draw_text("Press a key to continue", 22,WHITE,WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()


        self.wait_for_key()
        #pass
    
    #Una vez que se hayan agotado las vidas del jugador 1(megaman),  
    #se muestra en pantalla los puntajes finales y que el jugador 2(samus) gano.
    #Tambien si presiona una tecla, se inicia una nueva partida.
    def max_go_screen(self):
        # game over 
        if not self.running:
            return 
        self.screen.fill(LIGHTBLUE)
        self.draw_text("GAME OVER      Samus wins!",48, WHITE, WIDTH/2, HEIGHT/8)
        self.draw_text("Samus Score: " + str(self.player2.score), 22,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("Megaman Score: " + str(self.player.score), 22,WHITE,WIDTH/2,HEIGHT/3)
        self.draw_text("Press a key to continue", 22,WHITE,WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()

        
        self.wait_for_key()
        #pass

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False 
                if event.type == pg.KEYUP:
                    waiting = False

                    
    def draw_text(self,text,size,color,x,y):
        font = pg.font.Font(self.font_name,size)
        text_surface = font.render(text,True,color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)


    def countdown(self):
        self.my_timer = 15 
        for x in range(15):
            self.my_timer -= 1
            sleep(1)


def main():
    player1_socket = PlayerSocket(1)
    player2_socket = PlayerSocket(2)
    g = Game(player1_socket,player2_socket)
    g.show_start_screen()

    while g.running:
        g.new()
    #g.show_go_screen()
    

if __name__ == "__main__":
    main()
print("Client closed....") 

"""
g = Game()
g.start()
g.show_start_screen()
while g.running:
    g.new()
    #g.show_go_screen()

"""
pg.quit()