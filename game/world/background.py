from ..base_entities import GameObject, Layers, Tags
import pygame

class Background(GameObject):
    def __init__(self):
        super().__init__(Layers.Background, tag=Tags.Background)

        self.surface = pygame.image.load('assets/background.jpg').convert()
        self.rect = self.surface.get_rect()

    
