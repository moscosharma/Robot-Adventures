from .item import Item
from game.base_entities import Tags, GameObject
import pygame

class PlayerExplosive(Item):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, Tags.PlayerExplosive)

        surface = pygame.image.load("assets/Items/poison.png").convert_alpha()
        self.surface = pygame.transform.smoothscale(surface, (40, 40))
        rect = self.surface.get_rect()
        self.rect = pygame.Rect(position.x, position.y, rect.width, rect.height)
        # self.rectOffset = pygame.Vector2(rect.width * 0.1, rect.height * 0.2) 
        self.surface.fill((0, 200, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)

        self.debugModeExists = False

    def onCollision(self, gameObject: GameObject, gameManager):
        if gameObject.tag == Tags.Player: self.destroy() 

    def destroy(self):
        self.isActive = False