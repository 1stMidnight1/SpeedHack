import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
def menu(state):
    if state == "restart":
        menuoverlay = pygame.image.load("pausemenurestart.png").convert_alpha()
        screen.blit(menuoverlay, (0, 0))
    if state == "exit":
        menuoverlay = pygame.image.load("pausemenuexit.png").convert_alpha()
        screen.blit(menuoverlay, (0, 0))