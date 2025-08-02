from ..base_entities import GameObject, Layers, Tags
import pygame

class TileMap(GameObject):
    def __init__(self):
        super().__init__(Layers.Foreground, [Layers.Player, Layers.Items, Layers.Enemies], pygame.Vector2(-500, 580), Tags.TileMap)
        self.surface = pygame.Surface(size = (2000, 100))
        self.surface.fill((255, 255, 255))
        self.rect = self.surface.get_rect()
        print('TileMap position', self.position)
        # self.rectDebugColor = (150, 255, 0, 0.3)
        # self.debugModeExists = True
        
    def onUpdate(self, deltaTime, gameManager):
        self.rect.x = self.position.x
        self.rect.y = self.position.y
        pass

    def onCollision(self, gameObject: GameObject, gameManager):
        if (gameObject.tag in [Tags.Player, Tags.AdventurerEnemy, Tags.ZombieEnemy]):
            gameObject.standAt(self.rect.top)
    