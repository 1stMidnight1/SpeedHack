import pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
def menu():
    menuback = pygame.Surface((1280, 720))
    menuback.fill((0,0,0))
    menuback.set_alpha(128)
    screen.blit(menuback, (0, 0))