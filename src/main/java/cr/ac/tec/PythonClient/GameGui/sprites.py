


from settings import *
import pygame as pg
from random import choice
vec = pg.math.Vector2


class Spritesheet:
    #clase de utilidades para convertir imagenes en sprites para representar objetos o personajes en el juego 
    def __init__(self,img_name):
        self.spritesheet = pg.image.load(img_name)

    def get_image(self, img):
        self.loaded_image = pg.image.load(img)
        h = self.loaded_image.get_height()
        w = self.loaded_image.get_width()
        image = pg.Surface((w,h), pg.SRCALPHA, 32)
        image = image.convert_alpha()
        image.blit(self.loaded_image,(0,0))
        return image
        

#Sprites para el jugador
class Player(pg.sprite.Sprite):
    def __init__(self,game,playerID):
        pg.sprite.Sprite.__init__(self)
        self.playerID = playerID
        self.game = game
        self.load_images()
        if self.playerID == 1:
            self.image = self.game.spritesheet.get_image("resources/megamanstand.png")
            self.walking = False #para mostrar la animación cuando camina 
            self.jumping = False  #para mostrar la animación cuando salta 
            self.current_frame = 0
            self.last_update = 0
        else:
            self.image = self.game.spritesheet.get_image("resources/samusstand.png")
            self.samus_walking = False 
            self.samus_jumping = False
            self.samus_current_frame = 0
            self.samus_last_update = 0
        #self.image.set_colorkey(BLACK)
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2) #ubicación inicial del jugador
        self.pos = vec(WIDTH / 2, HEIGHT / 2) #posicion inicial del jugador 
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def load_images(self):
        self.samus_standing_frame = [self.game.spritesheet.get_image("resources/samusstand.png"),
                                    self.game.spritesheet.get_image("resources/samusstand.png")]

        self.samus_walk_frames_r = [self.game.spritesheet.get_image("resources/samus1.png"),
                                    self.game.spritesheet.get_image("resources/samus2.png"),
                                    self.game.spritesheet.get_image("resources/samus3.png"),
                                    self.game.spritesheet.get_image("resources/samus4.png"),
                                    self.game.spritesheet.get_image("resources/samus5.png"),
                                    self.game.spritesheet.get_image("resources/samus6.png"),
                                    self.game.spritesheet.get_image("resources/samus7.png"),
                                    self.game.spritesheet.get_image("resources/samus8.png"),
                                    self.game.spritesheet.get_image("resources/samus9.png"),
                                    self.game.spritesheet.get_image("resources/samus91.png")]
        
        self.samus_walk_frames_l = [self.game.spritesheet.get_image("resources/samus_1.png"),
                                    self.game.spritesheet.get_image("resources/samus_2.png"),
                                    self.game.spritesheet.get_image("resources/samus_3.png"),
                                    self.game.spritesheet.get_image("resources/samus_4.png"),
                                    self.game.spritesheet.get_image("resources/samus_5.png"),
                                    self.game.spritesheet.get_image("resources/samus_6.png"),
                                    self.game.spritesheet.get_image("resources/samus_7.png"),
                                    self.game.spritesheet.get_image("resources/samus_8.png"),
                                    self.game.spritesheet.get_image("resources/samus_9.png"),
                                    self.game.spritesheet.get_image("resources/samus_91.png")]

        self.samus_jump = self.game.spritesheet.get_image("resources/samusstand.png")


        self.standing_frame = [self.game.spritesheet.get_image("resources/megamanstand.png"),
                                self.game.spritesheet.get_image("resources/megamanstand.png")]

        self.walk_frames_r = [self.game.spritesheet.get_image("resources/megaman1.png"),
                            self.game.spritesheet.get_image("resources/megaman2.png"),
                            self.game.spritesheet.get_image("resources/megaman3.png"),
                            self.game.spritesheet.get_image("resources/megaman4.png")]

        self.walk_frames_l = [self.game.spritesheet.get_image("resources/megaman_1.png"),
                            self.game.spritesheet.get_image("resources/megaman_2.png"),
                            self.game.spritesheet.get_image("resources/megaman_3.png"),
                            self.game.spritesheet.get_image("resources/megaman_4.png")]

        self.jump_frame = self.game.spritesheet.get_image("resources/megamanstand.png")
        

    def jump_cut(self):
        if self.playerID == 1:
            if self.jumping:
                if self.vel.y < -3:
                    self.vel.y = -3
        else:
            if self.samus_jumping:
                if self.vel.y < -3:
                    self.vel.y = -3

    def jump(self):
        #salta unicamente si esta tocando una plataforma 
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self,self.game.platforms,False)
        self.rect.x -= 2
        if self.playerID == 1:
            if hits and not self.jumping:
                self.jumping = True
                self.vel.y = -PLAYER_JUMP
        else:
            if hits and not self.samus_jumping:
                self.samus_jumping = True
                self.vel.y = -PLAYER_JUMP


    def update(self):
        self.animate()
        self.acc = vec(0,0.5)
        keys = pg.key.get_pressed()

        if self.playerID == 1:

            if keys[pg.K_LEFT]:
                self.acc.x = -PLAYER_ACC
            if keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACC
        else:
            if keys[pg.K_a]:
                self.acc.x = -PLAYER_ACC
            if keys[pg.K_d]:
                self.acc.x = PLAYER_ACC

        # se aplica fricción al personaje 
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #control del movimiento 
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        #limites para el personaje 
        if self.pos.x > WIDTH + self.rect.width/2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width/2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        samus_now = pg.time.get_ticks()
        if self.playerID == 1:
            if self.vel.x != 0:
                self.walking = True
            else:
                self.walking = False
        else:
            if self.vel.x != 0:
                self.samus_walking = True
            else:
                self.samus_walking = True


        if self.vel.x != 0:
            self.samus_walking = True
        else:
            self.samus_walking = False
        
        if self.playerID == 1:
            if self.walking:
                if now - self.last_update > 200:
                    self.last_update = now 
                    self.current_frame = (self.current_frame + 1)% len(self.walk_frames_l)
                    if self.vel.x > 0:
                        self.image = self.walk_frames_r[self.current_frame]
                    else:
                        self.image = self.walk_frames_l[self.current_frame]
                    self.rect = self.image.get_rect()
        else:
            if self.samus_walking:
                if samus_now - self.samus_last_update> 200:
                    self.samus_last_update = samus_now
                    self.samus_current_frame = (self.samus_current_frame + 1) % len(self.samus_walk_frames_l)
                    if self.vel.x > 0:
                        self.image = self.samus_walk_frames_r[self.samus_current_frame]
                    else:
                        self.image = self.samus_walk_frames_l[self.samus_current_frame]


        if self.playerID == 1:
            if not self.jumping and not self.walking:
                if now - self.last_update > 350:
                    self.last_update = now
                    self.current_frame = (self.current_frame+1) % len(self.standing_frame)
                    self.image = self.standing_frame[self.current_frame]
        else:
            if not self.samus_jumping and not self.samus_walking:
                if samus_now - self.samus_last_update > 350:
                    self.samus_last_update = samus_now
                    self.samus_current_frame = (self.samus_current_frame + 1) % len(self.samus_standing_frame)
                    self.image = self.samus_standing_frame[self.samus_current_frame]

class Projectile(pg.sprite.Sprite):
    def __init__(self,x, y, radius, color):
        self.x = x 
        self.y = y 
        self.radius = radius
        self.color = color 
        
class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        #parametros de la clase 
        # x = posicion en x 
        # y = posicion en y 
        pg.sprite.Sprite.__init__(self)
        self.game = game
        images = [self.game.spritesheet.get_image("resources/platform_4.png"),
                    self.game.spritesheet.get_image("resources/platform_2.png"),
                    self.game.spritesheet.get_image("resources/platform_5.png")]
        self.image = choice(images)
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y



    

