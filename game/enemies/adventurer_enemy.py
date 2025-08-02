from .enemy import Enemy, EnemyAction
from game.base_entities import Animator, Tags, Direction
from game.characters.player import Player
import pygame, random

class AdventurerEnemy(Enemy):
    ActionGap = [3, 5]

    def __init__(self, position: pygame.Vector2):
        super().__init__(position, Tags.AdventurerEnemy)
        self.animator = Animator(
            'idle',
            True,
            idle = [
                {
                    'nextFrameTime': 0.1,
                    'frame': pygame.image.load("assets/Male adventurer/PNG/Poses/character_maleAdventurer_idle.png").convert_alpha()
                }
            ],
            walk = [
                {
                    'nextFrameTime': 0.1,
                    'frame': pygame.image.load("assets/Male adventurer/PNG/Poses/character_maleAdventurer_walk0.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.2,
                    'frame': pygame.image.load("assets/Male adventurer/PNG/Poses/character_maleAdventurer_walk1.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.3,
                    'frame': pygame.image.load("assets/Male adventurer/PNG/Poses/character_maleAdventurer_walk2.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.4,
                    'frame': pygame.image.load("assets/Male adventurer/PNG/Poses/character_maleAdventurer_walk3.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.5,
                    'frame': pygame.image.load("assets/Male adventurer/PNG/Poses/character_maleAdventurer_walk4.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.6,
                    'frame': pygame.image.load("assets/Male adventurer/PNG/Poses/character_maleAdventurer_walk5.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.7,
                    'frame': pygame.image.load("assets/Male adventurer/PNG/Poses/character_maleAdventurer_walk6.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.8,
                    'frame': pygame.image.load("assets/Male adventurer/PNG/Poses/character_maleAdventurer_walk7.png").convert_alpha()
                }
            ],
        )
        rect = self.animator.getCurrentFrame().get_rect()
        self.rect = pygame.Rect(0, 0, rect.width * 0.7, rect.height * 0.7)
        self.rectOffset = pygame.Vector2(rect.width * 0.15, rect.height * 0.3)
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

        delayForNextAction = random.uniform(*AdventurerEnemy.ActionGap)

        match(self.action):
            case EnemyAction.Idle:
                self.action = EnemyAction.Patrol
                self.nextActionTime += delayForNextAction
                self.patrolPoints = self.getPatrolPoints(self.position.x)
            case EnemyAction.Patrol:
                self.action = EnemyAction.Idle
                self.nextActionTime += 3

    def handlePhysics(self, deltaTime: float):
        match(self.action):
            case EnemyAction.Patrol:
                match(self.direction):
                    case Direction.Left | Direction.Idle:
                        self.speed.x = -Enemy.WalkSpeed
                        if self.position.x <= self.patrolPoints[0]:
                            self.direction = Direction.Right
                    case Direction.Right:
                        self.speed.x = Enemy.WalkSpeed
                        if self.position.x >= self.patrolPoints[1]:
                            self.direction = Direction.Left
            case EnemyAction.Idle:
                self.speed.x = 0  # Stop moving when idle
                self.direction = Direction.Idle
        super().handlePhysics(deltaTime)

    def handleAnimationState(self):
        if self.speed.x != 0:
            self.animator.setState('walk', loop=True)  # Set walk state
        else:
            self.animator.setState('idle', loop=True)  # Set idle state