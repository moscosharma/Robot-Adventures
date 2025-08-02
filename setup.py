import pygame
GAME_NAME = 'My Game'
GAME_WINDOW = (1000, 600)

pygame.init()
screen = pygame.display.set_mode(GAME_WINDOW)
pygame.display.set_caption(GAME_NAME)
clock = pygame.time.Clock()