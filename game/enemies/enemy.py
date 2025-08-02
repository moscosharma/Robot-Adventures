from game.base_entities import GameObject, Layers, DebugMode, Animator, Tags, Direction
from game.characters.player import PlayerStates
import pygame

class EnemyStates: 
    Idle = 'idle'
    Patrol = 'patrol'

class EnemyAction:
    Idle = 'idle'
    Patrol = 'patrol'
    Follow = 'follow'

class Enemy(GameObject):
    Gravity = 1000
    SlowWalkSpeed = 300
    WalkSpeed = 400
    JumpSpeed = 500
    AirTimeDetectionThreshold = 0.1
    KickSpeed = 800
    KickCoolDownTime = 1
    PatrolRange = 700
    Bounds = (-100, 1100)
    def __init__(self, position: pygame.Vector2, tag: Tags):
        super().__init__(Layers.Enemies, [Layers.Player, Layers.Foreground], position, tag)

        self.speed = pygame.Vector2(Enemy.WalkSpeed, 0)  # Speed in pixels per second
        
        self.debugModeExists = True  # Enable debug mode for this game object
        self.state = EnemyStates.Idle
        self.direction = Direction.Idle
        self.lastDirection = Direction.Idle

        self.timeElapsed = 0
                        
    def handleRect(self):
        self.rect.x = self.rectOffset.x + self.position.x
        self.rect.y = self.rectOffset.y + self.position.y

    def standAt(self, y: int):
        self.position.y = y - self.surface.get_height()
        self.airTime = 0
        self.speed.y = 0

    def getPatrolPoints(self, x: int):
        left = x - Enemy.PatrolRange / 2
        right = x + Enemy.PatrolRange / 2
        if x > Enemy.Bounds[1]:
            return (Enemy.Bounds[1] - self.PatrolRange, Enemy.Bounds[1])
        if x < 0:
            return (Enemy.Bounds[0], Enemy.Bounds[0] + self.PatrolRange)
        return (left, right)

    def onAnimation(self, deltaTime: int):
        self.animator.update(deltaTime)
        self.surface = self.animator.getCurrentFrame()

        if self.speed.x < 0:
            self.surface = pygame.transform.flip(self.surface, True, False)

    def onCollision(self, gameObject: GameObject, gameManager):
        if gameObject.tag == Tags.TileMap:
            self.speed.y = 0

        if gameObject.tag == Tags.Player and gameObject.state == PlayerStates.Kick:
            gameManager.enemyKilled(self)
            self.destroy()

    def onUpdate(self, deltaTime: float, gameManager):
        if DebugMode and (self.position.x < 0 or self.position.x > 1000):
            print(self.tag, self.position.x, self.patrolPoints)

    def handlePhysics(self, deltaTime: float):
        self.speed.y = min(self.speed.y + Enemy.Gravity * deltaTime, 1000)  # Apply gravity
        self.position.x += self.speed.x * deltaTime
        self.position.y += self.speed.y * deltaTime


    def destroy(self):
        self.isActive = False