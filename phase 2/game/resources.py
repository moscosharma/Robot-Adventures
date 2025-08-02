import pygame

class Resources:
    ResourcesLoaded = False
    
    def __init__(self):
        if Resources.ResourcesLoaded: return

        Resources.Background = pygame.image.load('assets/background.jpg').convert()

        Resources.ResourcesLoaded = True
