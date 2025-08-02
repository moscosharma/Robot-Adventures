from game.core import PhysicsBody, Layers, Tags
import pygame

class ItemTypes:
    Point = 'point'
    PlatformExplosive = 'platformExplosive'
    PlayerExplosive = 'playerExplosive'
    Jump = 'jump'
    Attack = 'attack'

LAVA_Y = 1000

class Item(PhysicsBody):
    def __init__(self, interactsWith, position, tag, surface, rect, rectOffset, itemCollected):
        super().__init__(Layers.Items, [Layers.Player, *interactsWith], position, tag, surface, rect, rectOffset, pygame.Vector2(0, 200), 0)
        self.itemCollected = itemCollected

    def onUpdate(self, deltaTime):
        super().onUpdate(deltaTime)

        if self.position.y > LAVA_Y: self.destroy()

    def onCollision(self, gameObject):
        if gameObject.tag == Tags.Player:
            self.destroy()
            self.itemCollected(self)
