
#from target.classes.cr.ac.tec.PythonClient.GameGui.sprites import Player
import pygame as pg
import random


#Game options / settings 
TITLE = "Build a Tree"
WIDTH = 1200
HEIGHT = 600
FPS = 60

#Propiedades del jugador 
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12 

#COLORS 
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

vec = pg.math.Vector2


#Sprites para el jugador

class Player(pg.sprite.Sprite):
    def __init__(self,game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def jump(self):
        # salta unicamente si el personaje esta sobre una plataforma
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self,self.game.platforms,False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

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



class Game:
    def __init__(self):
        # inicializa la ventana 
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # inicia un nuevo juego 
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        platform1 = Platform(350, 250, 400, 40)
        platform2 = Platform(650,450, 200,20)
        self.all_sprites.add(platform1)
        self.all_sprites.add(platform2)
        self.platforms.add(platform1)
        self.platforms.add(platform2)
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
        # después de dibujar o mostrar elementos en pantalla, actualiza la ventana
        pg.display.flip()

    def show_start_screen(self):
        # ventana de inicio 
        pass

    def show_go_screen(self):
        # game over 
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()