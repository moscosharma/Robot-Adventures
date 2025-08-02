import pygame
from .constants import Layers, Tags

class GameObject:
    def __init__(self: "GameObject",
            layer: Layers = Layers.Foreground,
            target: list[Layers] = [],
            position: pygame.Vector2 = pygame.Vector2(0, 0),
            tag: Tags = Tags.Default
        ):
        self.isActive = True
        self.layer = layer
        self.targets = target
        self.position = position
        self.tag = tag
        self.surface = pygame.Surface((1, 1))
        self.rect = self.surface.get_rect()

    def onCreate(self):
        # print(f"GameObject created with tag: {self.tag}")
        pass

    def onUpdate(self, deltaTime: int, gameWorld):
        # print(f"GameObject updated with tag: {self.tag if self.tag else 'no tag'}")
        pass

    def onCollision(self, gameObject: "GameObject"):
        # print(f"No collision logic defined for {self.tag if self.tag else 'no tag'}.")
        pass

    def onAnimation(self, deltaTime: int):
        # print(f"No animation logic defined for {self.tag if self.tag else 'no tag'}.")
        pass
