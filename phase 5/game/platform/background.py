from game.core import GameObject, Layers, Tags, Resources
import pygame

class Background(GameObject):
    def __init__(self):
        super().__init__(Layers.Background, [], pygame.Vector2(), Tags.Background, Resources.Background)
