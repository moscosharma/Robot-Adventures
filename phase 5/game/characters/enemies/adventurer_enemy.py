from game.characters.enemies.enemy import Enemy, EnemyAction
from game.characters.core.character import CharacterAnimationStates
from game.core import Animator, AnimationFrame, Tags, Resources
import random

class AdventurerEnemy(Enemy):
    def __init__(self, position, enemyKilled, playerKilled):
        animator = Animator(
            CharacterAnimationStates.Idle,
            {
                CharacterAnimationStates.Idle: [
                    AnimationFrame(0.1, Resources.Adventurer['idle'])
                ],
                CharacterAnimationStates.Walk: [
                    AnimationFrame(0.1, Resources.Adventurer['walk0']),
                    AnimationFrame(0.2, Resources.Adventurer['walk1']),
                    AnimationFrame(0.3, Resources.Adventurer['walk2']),
                    AnimationFrame(0.4, Resources.Adventurer['walk3']),
                    AnimationFrame(0.5, Resources.Adventurer['walk4']),
                    AnimationFrame(0.6, Resources.Adventurer['walk5']),
                    AnimationFrame(0.7, Resources.Adventurer['walk6']),
                    AnimationFrame(0.8, Resources.Adventurer['walk7'])
                ],
            },
            {}
        )
        super().__init__(position, Tags.AdventurerEnemy, animator, enemyKilled, playerKilled)

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
        delayForNextAction = random.uniform(*AdventurerEnemy.ActionGap)
        match(self.action):
            case EnemyAction.Idle: self.idleActionDecision(delayForNextAction)
            case EnemyAction.Patrol: self.patrolActionDecision()
    
    def handleDecisionExecution(self):
        match(self.action):
            case EnemyAction.Patrol: self.patrolActionExecution()
            case EnemyAction.Idle: self.idleActionExecution()
