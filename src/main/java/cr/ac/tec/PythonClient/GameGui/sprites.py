
from settings import *
import pygame as pg
import sys
vec = pg.math.Vector2


#Sprites para el jugador

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.lives = 10
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        #salta unicamente si esta tocando una plataforma 
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self,self.game.platforms,False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP


    def update(self):
        self.acc = vec(0,0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # se aplica fricción al personaje 
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #control del movimiento 
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        #limites para el personaje 
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        
        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        #parametros de la clase 
        # x = posicion en x 
        # y = posicion en y 
        # w = ancho de la plataforma 
        # h = altura de la plataforma
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y