import pygame
import time
from mainGameScreen import *

pygame.init()

displayWidth = 750
displayHeight = 600


def main():
    displayFlag = True

    game_display = pygame.display.set_mode((displayWidth, displayHeight)) 
    pygame.display.set_caption("Build a Tree")
    clock = pygame.time.Clock()

    #Pantalla
    gameScreen = mainGameScreen(game_display)

    #Loop del juego
    while displayFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                displayFlag = False

        #Para cuando ventana esté abierta
            if mainGameScreen.flag:
                mainGameScreen.events(event)

        if mainGameScreen.flag:
            mainGameScreen.__update__()
            mainGameScreen.__draw__()

        pygame.display.flip()

font_name = pygame.font.match_font("arial")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


main()

pygame.quit()
quit()

