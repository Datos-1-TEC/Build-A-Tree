

from settings import *
import pygame as pg
from random import choice, randrange
vec = pg.math.Vector2
vec2 = pg.math.Vector2


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
        self.groups = game.all_sprites, game.playerslist
        pg.sprite.Sprite.__init__(self,self.groups)
        self.playerID = playerID
        self.game = game
        self.load_images()
        self.left = False
        self.right = False
        self.activated = False
        self.lives = 3
        self.score = 0
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

    def jump(self, PLAYER_JUMP):
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
                self.acc.x = -PLAYER_ACC #print("Izquierda " + str(self.acc.x))               
                self.left = True
                self.right = False
            if keys[pg.K_RIGHT]:
                self.acc.x = PLAYER_ACC #print("Derecha: " + str(self.acc.x))
                self.left = False
                self.right = True
        else:
            if keys[pg.K_a]:
                self.acc.x = -PLAYER_ACC
                self.left = True
                self.right = False
            if keys[pg.K_d]:
                self.acc.x = PLAYER_ACC
                self.left = False
                self.right = True

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

 
class Platform(pg.sprite.Sprite):
    def __init__(self,game,x,y,platform_index):
        self.groups = game.all_sprites, game.platforms
        #parametros de la clase 
        # x = posicion en x 
        # y = posicion en y 
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        images = [self.game.spritesheet.get_image("resources/platform_6.png"),
                    self.game.spritesheet.get_image("resources/platform_2.png"),
                    self.game.spritesheet.get_image("resources/platform_5.png")]
        self.image = images[platform_index]
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            PowerUp(self.game,self)


class PowerUp(pg.sprite.Sprite):    
    def __init__(self,game,platform):
        #self.groups = game.all_sprites, game.powerups
        self.type = choice(['shoot', 'shield', 'airjump', 'push']) #'extrapoints',, 'faster', 'tempplatform'
        if self.type == 'shield':
            self.groups = game.all_sprites, game.powerup_shield
        elif self.type == 'shoot':
            self.groups = game.all_sprites, game.powerup_shoot
        elif self.type == 'push':
            self.groups = game.all_sprites, game.powerup_push
        elif self.type == 'airjump':
            self.groups = game.all_sprites, game.powerup_airjump
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game 
        self.game.powerupslist.append(self)
        self.platform = platform
           
        #self.type = choice(['airjump'])
        #self.type = choice(['push'])
        #self.type = choice(['shoot'])
        self.image = self.game.spritesheet.get_image("resources/star_1.png")
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx =  self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5
        

    def update(self):
        self.rect.bottom = self.platform.rect.top - 5
        if not self.game.platforms.has(self.platform):
            self.kill()

class Token(pg.sprite.Sprite):
    def __init__(self,game,value,shape):
        self.groups = game.all_sprites, game.tokens
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game 
        self.value = value 
        self.shape = shape 
        self.image = pg.Surface((30,30))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2,HEIGHT/2)
        self.pos = vec2(WIDTH/2,HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.update()

    def update(self):
        self.acc = vec(0,1)
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc 
        self.pos += self.vel + 0.5 * self.acc

        self.rect.center = self.pos



class Projectiles(pg.sprite.Sprite):
    def __init__(self,game,player, facing):
        self.player = player 
        self.game = game
        if player.playerID == 1:
            self.groups = game.all_sprites, game.projectiles_megaman
            self.image_up = self.game.spritesheet.get_image("resources/shine1.png")
            self.image_down = self.game.spritesheet.get_image("resources/shine2.png")
        else:
            self.groups = game.all_sprites, game.projectiles_samus
            self.image_up = self.game.spritesheet.get_image("resources/tesla_ball1.png")
            self.image_down = self.game.spritesheet.get_image("resources/tesla_ball2.png")
        pg.sprite.Sprite.__init__(self,self.groups)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = self.player.pos.x 
        self.facing = facing
        self.vx = 10 * self.facing
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = self.player.pos.y - 50 
        self.vy = 0
        self.dy = 0.01
        self.update()

    def update(self):
        self.rect.x += self.vx
        self.vy +=  self.dy 
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1 
        center = self.rect.center 
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

