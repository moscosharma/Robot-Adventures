from game.characters.enemies.enemy import Enemy, EnemyAction
from game.characters.core.character import CharacterAnimationStates
from game.core import Animator, AnimationFrame, Tags, Resources
import random

class ZombieEnemy(Enemy):
    TargetRange = 500

    def __init__(self, position, player, enemyKilled, playerKilled):
        animator = Animator(
            CharacterAnimationStates.Idle,
            {
                CharacterAnimationStates.Idle: [
                    AnimationFrame(0.1, Resources.Zombie['idle'])
                ],
                CharacterAnimationStates.Walk: [
                    AnimationFrame(0.1, Resources.Zombie['walk0']),
                    AnimationFrame(0.2, Resources.Zombie['walk1']),
                    AnimationFrame(0.3, Resources.Zombie['walk2']),
                    AnimationFrame(0.4, Resources.Zombie['walk3']),
                    AnimationFrame(0.5, Resources.Zombie['walk4']),
                    AnimationFrame(0.6, Resources.Zombie['walk5']),
                    AnimationFrame(0.7, Resources.Zombie['walk6']),
                    AnimationFrame(0.8, Resources.Zombie['walk7'])
                ],
            },
            {}
        )
        super().__init__(position, Tags.ZombieEnemy, animator, enemyKilled, playerKilled)

        self.playerTarget = player
        self.action = EnemyAction.Patrol
        self.patrolPoints = self.getPatrolPoints(self.position.x)

    def onUpdate(self, deltaTime):
        self.timeElapsed += deltaTime
        self.handleDecisions()
        self.handleDecisionExecution()
        self.handleAnimationState()
        super().onUpdate(deltaTime)

    def handleDecisions(self):
        if self.timeElapsed < self.nextActionTime: return
        delayForNextAction = random.uniform(*ZombieEnemy.ActionGap)

        if abs(self.playerTarget.position.x - self.position.x) < ZombieEnemy.TargetRange:
            self.targetPosition = self.playerTarget.position.x
            self.action = EnemyAction.Follow

        match(self.action):
            case EnemyAction.Idle: self.idleActionDecision(delayForNextAction)
            case EnemyAction.Patrol: self.patrolActionDecision()
            case EnemyAction.Follow: self.followActionDecision(delayForNextAction)

    def handleDecisionExecution(self):
        match(self.action):
            case EnemyAction.Patrol: self.patrolActionExecution()
            case EnemyAction.Idle: self.idleActionExecution()
            case EnemyAction.Follow: self.followActionExecution()

    def followActionDecision(self, delayForNextAction):
        if abs(self.targetPosition - self.position.x) < 5:
            self.action = EnemyAction.Patrol
            self.nextActionTime += 1
        else:
            self.nextActionTime += delayForNextAction

    def followActionExecution(self):
        self.velocity.x = Enemy.WalkSpeed if self.position.x < self.targetPosition else -Enemy.WalkSpeed
        if abs(self.position.x - self.targetPosition) < 5:
            self.velocity.x = 0


