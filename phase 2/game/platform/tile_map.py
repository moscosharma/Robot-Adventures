from game.core import PhysicsBody, Layers, Tags
import pygame

class TileMap(PhysicsBody):
    def __init__(self):
        surface = pygame.Surface(size = (2000, 100))
        surface.fill((255, 255, 255))
        rect = surface.get_rect()

        super().__init__(Layers.Foreground, [Layers.Player, Layers.Items, Layers.Enemies], pygame.Vector2(-500, 580), Tags.TileMap, surface, rect, pygame.Vector2(), pygame.Vector2(), 0)

    def onCollision(self, gameObject):
        if (gameObject.tag in [Tags.Player]):
            gameObject.standAt(self.rect.top)
