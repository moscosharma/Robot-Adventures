from game.core import PhysicsBody, Layers, Tags, GameWorld, Resources, Explosion
import pygame

class TileMapStates:
    Idle = 'idle'
    Destroy = 'destroy'

class TileMap(PhysicsBody):
    def __init__(self):
        surface = pygame.Surface(size = (2000, 100))
        surface.fill((255, 255, 255))
        rect = surface.get_rect()

        super().__init__(Layers.Foreground, [Layers.Player, Layers.Items, Layers.Enemies], pygame.Vector2(-500, 580), Tags.TileMap, surface, rect, pygame.Vector2(), pygame.Vector2(), 0)

        self.state = TileMapStates.Idle
        self.leftExplosion = pygame.Vector2()
        self.rightExplosion = pygame.Vector2()
        self.nextExplosionDelay = 0.05
        self.timeElapsed = 0

    def onUpdate(self, deltaTime):
        self.timeElapsed += deltaTime
        if self.state == TileMapStates.Destroy and self.timeElapsed > self.nextExplosionDelay:
            self.nextExplosionDelay += 0.02
            GameWorld.World.addGameObject(Explosion(self.leftExplosion))
            if self.rightExplosion != self.leftExplosion:
                GameWorld.World.addGameObject(Explosion(self.rightExplosion))

            self.leftExplosion -= pygame.Vector2(50, 0)
            self.rightExplosion += pygame.Vector2(50, 0)
            if self.leftExplosion.x < -100 and self.rightExplosion.x > 1100:
                self.destroy()

        super().onUpdate(deltaTime)

    def onCollision(self, gameObject):
        if (gameObject.tag in [Tags.Player, Tags.AdventurerEnemy, Tags.ZombieEnemy]):
            gameObject.standAt(self.rect.top)
    
        elif gameObject.tag == Tags.PlatformExplosive:
            self.state = TileMapStates.Destroy
            self.leftExplosion = pygame.Vector2(gameObject.position + pygame.Vector2(0, 50))
            self.rightExplosion = pygame.Vector2(gameObject.position + pygame.Vector2(0, 50))
            self.nextExplosionDelay = self.timeElapsed
            Resources.Sounds['boom'].stop()
            Resources.Sounds['boom'].play(-1)
