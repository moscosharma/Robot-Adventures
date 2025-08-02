from game.base_entities import Tags, Layers, GameObject
from .item import Item
import pygame

class AttackItem(Item):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, Tags.AttackItem)

        surface = pygame.image.load("assets/Items/attack.png").convert_alpha()
        self.surface = pygame.transform.smoothscale(surface, (40, 40))
        self.rect = self.surface.get_rect()
        # self.rect = pygame.Rect(position.x, position.y, rect.width * 0.6, rect.height * 0.6)
        # self.rectOffset = pygame.Vector2(rect.width * 0.1, rect.height * 0.2) 
        self.surface.fill((255, 0, 255, 255), special_flags=pygame.BLEND_RGBA_MULT)

        self.debugModeExists = False

    def onCollision(self, gameObject: GameObject, gameManager):
        if gameObject.tag == Tags.Player:
            self.destroy()
            gameManager.itemCollected(self)

    def destroy(self):
        self.isActive = False