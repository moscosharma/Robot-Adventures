from game.base_entities import GameObject, Layers, Tags
from .constants import LAVA_Y
import pygame, math

class Item(GameObject):
    SPEED = 200
    AMPLITUDE = 50
    WAVE_SPEED = 2
    
    def __init__(self, position: pygame.Vector2, tag: Tags):
        super().__init__(Layers.Items, [Layers.Player], position, tag)

        self.timeElapsed = 0
        self.centerPosition = position.x

    def onUpdate(self, deltaTime: float, gameWorld):
        self.timeElapsed += deltaTime
        self.position.y += Item.SPEED * deltaTime
        self.position.x = self.centerPosition + Item.AMPLITUDE * math.sin(self.timeElapsed * Item.WAVE_SPEED)

        self.rect.x = self.position.x
        self.rect.y = self.position.y

        if self.position.y > LAVA_Y:
            self.destroy()

    def onAnimation(self, deltaTime):
        pass

    def destroy(self):
        self.isActive = False

