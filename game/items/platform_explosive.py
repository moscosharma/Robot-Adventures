from game.base_entities import Tags, Layers, GameObject
from .item import Item
import pygame

class PlatformExplosive(Item):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, Tags.PlatformExplosive)

        self.targets.append(Layers.Foreground)
        self.surface = pygame.image.load("assets/Items/bomb.png").convert_alpha()
        rect = self.surface.get_rect()
        self.rect = pygame.Rect(position.x, position.y, rect.width * 0.6, rect.height * 0.6)
        self.rectOffset = pygame.Vector2(rect.width * 0.1, rect.height * 0.2) 
        self.surface.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)

        self.debugModeExists = False

    def onCollision(self, gameObject: GameObject, gameManager):
        match(gameObject.tag):
            case Tags.TileMap: 
                gameManager.gameOver()
                print(f"PlatformExplosive collided with {gameObject.tag}")
            case Tags.Player: self.destroy()

    def onUpdate(self, deltaTime: int, gameManager):
        super().onUpdate(deltaTime, gameManager)
        self.rect.x = self.position.x + self.rectOffset.x
        self.rect.y = self.position.y + self.rectOffset.y


    def destroy(self):
        self.isActive = False