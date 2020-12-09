
from typing import Text
import pygame as pg
import random
import pygame
from math import *
from pygame.constants import K_w
from sprites import *
from settings import *
vec = pg.math.Vector2
bgs = ['resources/bg.jpg', 'resources/background2.jpg']



class Game:
    """********************************************************************************
                        Instituto Tecnologico de Costa Rica
                                Ing. en computadores
        @method __init__(self): Se encarga de iniciar la ventana del juego y cargar los datos pertenecientes a este.
        
        @method new(self): Se encarga de cargar los sprites de los componentes importantes del juego(proyectiles, jugadores, plataformas, entre otros) y se llama al metodo run().
        
        @method run(self): Llama a otros metodos que se encargan de la parte funcional del juego.
        
        @method update(self): En este metodo se crean los hitbox para los dos jugadores(toma en cuenta los power ups).
        
        @method events(self): En este metodo se establecen las acciones de cada boton.
        
        @method isColliding(self, player2x, player2y, playerx, playery): Es una funcion donde se crea un hitbox alternativo para cuando los dos jugadores agarren el power up 'push' y asi se puedan empujar en caso que choquen.

        @method draw(self): Muestra en pantalla la imagen de fondo, puntajes y cantidad de vidas de ambos jugadores.

        @method show_go_screen(self): Una vez que se hayan agotado las vidas del jugador 2(samus), se muestra en pantalla los puntajes finales y que el jugador 1(megaman) gano. Tambien si presiona una tecla, se inicia una nueva partida.

        @method max_go_screen(self): Una vez que se hayan agotado las vidas del jugador 1(megaman), se muestra en pantalla los puntajes finales y que el jugador 2(samus) gano. Tambien si presiona una tecla, se inicia una nueva partida.

    ********************************************************************************"""
    def __init__(self):
        # inicializa la ventana 
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.spritesheet = Spritesheet("resources/megamanstand.png")

    def new(self):
        # inicia un nuevo juego 
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.projectiles_megaman = pg.sprite.Group()
        self.projectiles_samus = pg.sprite.Group()
        self.tokens = pg.sprite.Group()
        self.playerslist = pg.sprite.Group()
        self.powerupslist = [] 
        self.player = Player(self,1)
        self.player2 = Player(self,2)
        self.token = Token(self,2,"Diamond")
        #self.draw_text("Vidas: " + str(self.player.lives), 10, (0,0,0), 40, 20)
        #self.all_sprites.add(self.player2)
        #self.all_sprites.add(self.player)
        Platform(self,*PLATFORM_LIST[0],0)
        Platform(self,*PLATFORM_LIST[1],1)
        Platform(self,*PLATFORM_LIST[2],1)
        Platform(self,*PLATFORM_LIST[3],1)
        Platform(self,*PLATFORM_LIST[5],1)
        Platform(self,*PLATFORM_LIST[6],2)
        Platform(self,*PLATFORM_LIST[7],2)
        self.run()

    def run(self):
        # Game Loop para la partida 
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # actualiza los sprites 
        self.all_sprites.update()
        #revisa si el jugador colisiona con una plataforma, solo si esta cayendo
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)
            shots = pg.sprite.spritecollide(self.player2, self.projectiles_megaman, True)
            push = pg.sprite.spritecollide(self.player, self.playerslist, False)
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
                for powerup in self.powerupslist:
                    if self.isColliding(powerup.rect.centerx, powerup.rect.bottom, self.player2.pos.x, self.player2.pos.y):
                        powerup.kill()
                        self.player2.activated = True #Futura condición para el power up 'shield'
                        for shot in shots:
                            if self.player.pos.x < self.player2.pos.x: #En caso que el jugador 1 este a la  izquierda del jugador 2
                                if self.player2.activated:
                                    self.player2.pos.x += 0  #Hitbox en caso de disparo
                                    shot.kill()
                                else:
                                    self.player2.pos.x += 10  #Hitbox en caso de disparo
                                    shot.kill()
                            elif self.player.pos.x >= self.player2.pos.x: #En caso que el jugador 1 este a la derecha del jugador 2
                                if self.player2.activated:
                                    self.player2.pos.x -= 0  #Hitbox en caso de disparo
                                    shot.kill()
                                else:
                                    self.player2.pos.x -= 10  #Hitbox en caso de disparo
                                    shot.kill()
            """
            #push
            if self.isColliding(self.player.pos.x, self.player.pos.y, self.player2.pos.x, self.player2.pos.y):
                if self.player.pos.x < self.player2.pos.x:
                    self.player2.pos.x += 8
                elif self.player.pos.x >= self.player2.pos.x:
                    self.player2.pos.x -= 8
            """
            



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
                        if self.player.activated:
                            self.player.pos.x += 0  #Hitbox en caso de disparo
                            shot.kill()
                        else:
                            self.player.pos.x += 10  #Hitbox en caso de disparo
                            shot.kill()
                    elif self.player2.pos.x >= self.player.pos.x: #En caso que el jugador 1 esté a la derecha del jugador 2
                        if self.player.activated:
                            self.player.pos.x -= 0  #Hitbox en caso de disparo
                            shot.kill()
                        else:
                            self.player.pos.x -= 10  #Hitbox en caso de disparo
                            shot.kill()
            """
            #push
            if self.isColliding(self.player2.pos.x, self.player2.pos.y, self.player.pos.x, self.player.pos.y):
                if self.player2.pos.x < self.player.pos.x:
                    self.player.pos.x += 8
                elif self.player2.pos.x >= self.player.pos.x:
                    self.player.pos.x -= 8
            """


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
        

    def events(self):
        # Game Loop - eventos de pygame 
        for event in pg.event.get():
            # revisa si la ventana ha sido cerrada 
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    self.player.jump()
                elif event.key == pg.K_w:
                    self.player2.jump()
                elif event.key == pg.K_v: #crea plataforma random
                    Platform(self,*PLATFORM_LIST[4],2)
                elif event.key == pg.K_DOWN:
                    if self.player.left:
                        facing = -1
                    elif self.player.right:
                        facing = 1
                    
                    Projectiles(self,self.player, facing)

            if event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.player.jump_cut()
                elif event.key == pg.K_w:
                    self.player2.jump_cut()
                elif event.key == pg.K_p: #Prueba para power up "shoot", se debe cambiar
                    if self.player.left == True:
                        self.player.vel.x -= 10 
                    else:
                        self.player.vel.x += 10 
                elif event.key == pg.K_s:
                    if self.player2.left:
                        facing2 = -1
                    elif self.player2.right:
                        facing2 = 1
                    
                    Projectiles(self,self.player2, facing2)

    def isColliding(self, player2x, player2y, playerx, playery):
        distance = sqrt((pow(player2x-playerx,2))+(pow(player2y-playery,2)))
        if distance < 20:
            return True
        else:
            return False         

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


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    #g.show_go_screen()

pg.quit()