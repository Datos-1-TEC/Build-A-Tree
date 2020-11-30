
from typing import Text
import pygame as pg
import random
import pygame
from sprites import *
from settings import *

class Game:
    def __init__(self):
        # inicializa la ventana 
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    def new(self):
        # inicia un nuevo juego 
        self.player_lives = 10
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
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
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        if self.player.rect.top >= 590:
            self.player.pos.y += abs(self.player.vel.y)
            self.player_lives -= 1
            print(self.player_lives)

        #si el jugador se cae de una plataforma 
        # añadir las vidas del jugador y descontar una vida cuando se cae de una plataforma
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y,10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
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
                if event.key == pg.K_SPACE:
                    self.player.jump()


    def draw(self):
        # Game Loop - dibuja en la ventana 
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        #self.draw_text(str(self.player_lives),22,WHITE,WIDTH/2,15)
        # después de dibujar o mostrar elementos en pantalla, actualiza la ventana
        pg.display.flip()

    def show_start_screen(self):
        # ventana de inicio 
        self.screen.fill(LIGHTBLUE)
        self.draw_text("Game Over",48, WHITE, WIDTH/2, HEIGHT/4)

        pass

    def show_go_screen(self):
        # game over 
        if not self.running:
            return 
        self.screen.fill(LIGHTBLUE)
        self.draw_text("GAME OVER",48, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Score: ", 22,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("Press a key to exit", 22,WHITE,WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()


        self.wait_for_key()
        pass

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
    g.show_go_screen()

pg.quit()