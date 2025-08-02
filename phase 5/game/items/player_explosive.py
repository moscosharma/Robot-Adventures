from game.core import Tags, Resources
from game.items.item import Item
import pygame

class PlayerExplosive(Item):
    def __init__(self, position, itemCollected):
        surface = Resources.Items['poison']
        surface = pygame.transform.smoothscale(surface, (40, 40))
        surface.fill((0, 200, 0, 255), special_flags = pygame.BLEND_RGBA_MULT)
        rect = surface.get_rect()
        super().__init__([], position, Tags.PlayerExplosive, surface, rect, pygame.Vector2(), itemCollected)
