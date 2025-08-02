from .enemy import Enemy, EnemyAction, EnemyStates
from game.base_entities import GameObject, Layers, DebugMode, Animator, Tags, Direction
from game.characters.player import Player
import pygame, random

class ZombieEnemy(Enemy):
    ActionGap = [3, 5]
    TargetRange = 500

    def __init__(self, position: pygame.Vector2, player: Player):
        super().__init__(position, Tags.ZombieEnemy)
        self.animator = Animator(
            'idle',
            True,
            idle = [
                {
                    'nextFrameTime': 0.1,
                    'frame': pygame.image.load("assets/Zombie/PNG/Poses/character_zombie_idle.png").convert_alpha()
                }
            ],
            walk = [
                {
                    'nextFrameTime': 0.1,
                    'frame': pygame.image.load("assets/Zombie/PNG/Poses/character_zombie_walk0.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.2,
                    'frame': pygame.image.load("assets/Zombie/PNG/Poses/character_zombie_walk1.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.3,
                    'frame': pygame.image.load("assets/Zombie/PNG/Poses/character_zombie_walk2.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.4,
                    'frame': pygame.image.load("assets/Zombie/PNG/Poses/character_zombie_walk3.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.5,
                    'frame': pygame.image.load("assets/Zombie/PNG/Poses/character_zombie_walk4.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.6,
                    'frame': pygame.image.load("assets/Zombie/PNG/Poses/character_zombie_walk5.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.7,
                    'frame': pygame.image.load("assets/Zombie/PNG/Poses/character_zombie_walk6.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.8,
                    'frame': pygame.image.load("assets/Zombie/PNG/Poses/character_zombie_walk7.png").convert_alpha()
                }
            ],
        )
        rect = self.animator.getCurrentFrame().get_rect()
        self.rect = pygame.Rect(0, 0, rect.width * 0.7, rect.height * 0.7)
        self.rectOffset = pygame.Vector2(rect.width * 0.15, rect.height * 0.3)  # Offset for the rect to align with the feet
        self.playerTarget = player
        self.nextActionTime = 0

    def onCreate(self):
        self.action = EnemyAction.Patrol
        self.patrolPoints = self.getPatrolPoints(self.position.x)
        
    def onUpdate(self, deltaTime: float, gameManager):
        # super().onUpdate()
        self.timeElapsed += deltaTime

        self.handleDecisions()
        self.handlePhysics(deltaTime)  # Handle physics updates
        self.handleRect()
        self.handleAnimationState()  # Update animation state based on speed

    def handleDecisions(self):
        if self.timeElapsed < self.nextActionTime: return
        delayForNextAction = random.uniform(*ZombieEnemy.ActionGap)

        if abs(self.playerTarget.position.x - self.position.x) < ZombieEnemy.TargetRange:
            self.targetPosition = self.playerTarget.position.x
            self.action = EnemyAction.Follow

        match(self.action):
            case EnemyAction.Idle:
                self.action = EnemyAction.Patrol
                self.nextActionTime += delayForNextAction
                self.patrolPoints = self.getPatrolPoints(self.position.x)
            case EnemyAction.Patrol:
                self.action = EnemyAction.Idle
                self.nextActionTime += 3
            case EnemyAction.Follow:
                if abs(self.targetPosition - self.position.x) < 5:
                    self.action = EnemyAction.Patrol
                    self.nextActionTime += 1
                else:
                    self.nextActionTime += delayForNextAction

    def handlePhysics(self, deltaTime: float):
        match(self.action):
            case EnemyAction.Patrol:
                match(self.direction):
                    case Direction.Left | Direction.Idle:
                        self.speed.x = -Enemy.SlowWalkSpeed
                        if self.position.x <= self.patrolPoints[0]:
                            self.direction = Direction.Right
                    case Direction.Right:
                        self.speed.x = Enemy.SlowWalkSpeed
                        if self.position.x >= self.patrolPoints[1]:
                            self.direction = Direction.Left
            case EnemyAction.Idle:
                self.speed.x = 0  # Stop moving when idle
                self.direction = Direction.Idle
            case EnemyAction.Follow:
                self.speed.x = Enemy.WalkSpeed if self.position.x < self.targetPosition else -Enemy.WalkSpeed
                if abs(self.position.x - self.targetPosition) < 5:
                    self.speed.x = 0  # Stop moving when close enough to the target

        super().handlePhysics(deltaTime)

    def handleAnimationState(self):
        if self.speed.x != 0:
            self.animator.setState('walk', loop=True)
        else:
            self.animator.setState('idle', loop=True)
