from game.core import Tags, Layers
from game.items.item import Item
from game.resources import Resources
import pygame

class PlatformExplosive(Item):
    def __init__(self, position):
        surface = Resources.Items['bomb']
        surface.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
        rect = surface.get_rect()
        rect = pygame.Rect(position.x, position.y, rect.width * 0.6, rect.height * 0.6)
        rectOffset = pygame.Vector2(rect.width * 0.1, rect.height * 0.2) 

        super().__init__([Layers.Foreground], position, Tags.PlatformExplosive, surface, rect, rectOffset, None)

    def onCollision(self, gameObject):
        match(gameObject.tag):
            case Tags.TileMap | Tags.Player: self.destroy()
