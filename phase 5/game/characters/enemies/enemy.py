from game.characters.core.character import Character, CharacterAnimationStates, Direction
from game.characters.player.player import PlayerStates
from game.core import Tags, Layers, GameWorld, Explosion
import pygame

class EnemyAction:
    Idle = 'idle'
    Patrol = 'patrol'
    Follow = 'follow'

class EnemyStates:
    Idle = 'idle'
    Walk = 'walk'
    Patrol = 'patrol'

class EnemyTypes:
    Adventurer = "adventurer"
    Robot = "robot"
    Zombie = "zombie"

class Enemy(Character):
    WalkSpeed = 400
    PatrolRange = 700
    Bounds = (-100, 1100)
    ActionGap = [3, 5]
    def __init__(self, position, tag, animator, enemyKilled, playerKilled):
        surface = animator.getCurrentFrame()
        rect = surface.get_rect()
        rect.scale_by_ip(0.7)
        rectOffset = pygame.Vector2(rect.width * 0.22, rect.height * 0.43)
        super().__init__(Layers.Enemies, [Layers.Player, Layers.Foreground], position, tag, surface, rect, rectOffset, animator)

        self.timeElapsed = 0
        self.nextActionTime = 0
        self.enemyKilled = enemyKilled
        self.playerKilled = playerKilled

    def getPatrolPoints(self, x):
        left = x - Enemy.PatrolRange / 2
        right = x + Enemy.PatrolRange / 2
        if x > Enemy.Bounds[1]:
            return (Enemy.Bounds[1] - self.PatrolRange, Enemy.Bounds[1])
        if x < 0:
            return (Enemy.Bounds[0], Enemy.Bounds[0] + self.PatrolRange)
        return (left, right)

    def onCollision(self, gameObject):
        if gameObject.tag == Tags.TileMap:
            self.velocity.y = 0

        if gameObject.tag == Tags.Player:
            if gameObject.state == PlayerStates.Kick:
                self.enemyKilled(self)
                self.destroy()
            else:
                self.playerKilled()

    def idleActionDecision(self, delayForNextAction):
        self.action = EnemyAction.Patrol
        self.nextActionTime += delayForNextAction
        self.patrolPoints = self.getPatrolPoints(self.position.x)
    
    def patrolActionDecision(self):
        self.action = EnemyAction.Idle
        self.nextActionTime += 3

    def patrolActionExecution(self):
        match(self.direction):
            case Direction.Left | Direction.Idle:
                self.velocity.x = -Enemy.WalkSpeed
                if self.position.x <= self.patrolPoints[0]:
                    self.direction = Direction.Right
            case Direction.Right:
                self.velocity.x = Enemy.WalkSpeed
                if self.position.x >= self.patrolPoints[1]:
                    self.direction = Direction.Left
    
    def idleActionExecution(self):
        self.velocity.x = 0
        self.direction = Direction.Idle

    def handleAnimationState(self):
        if self.velocity.x != 0:
            self.animator.setState(CharacterAnimationStates.Walk)
        else:
            self.animator.setState(CharacterAnimationStates.Idle)

    def destroy(self):
        GameWorld.World.addGameObject(Explosion(pygame.Vector2(self.rect.center)))
        super().destroy()