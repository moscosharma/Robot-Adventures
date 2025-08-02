from game.core.game_object import GameObject, Layers, Tags
from game.resources import Resources
import pygame

class Background(GameObject):
    def __init__(self):
        super().__init__(Layers.Background, [], pygame.Vector2(), Tags.Background, Resources.Background)
