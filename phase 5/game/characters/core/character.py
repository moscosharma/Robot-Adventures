from game.core import PhysicsBody
import pygame

class CharacterAnimationStates:
    Idle = 'idle'
    Walk = 'walk'
    Jump = 'jump'
    Fall = 'fall'
    Kick = 'kick'

class Direction:
    Left = 'left'
    Right = 'right'
    Idle = 'idle'

class Character(PhysicsBody):
    def __init__(self, layer, interactsWith, position, tag, surface, rect, rectOffset, animator):
        super().__init__(layer, interactsWith, position, tag, surface, rect, rectOffset, pygame.Vector2(), 1000)
        self.animator = animator

    def standAt(self, y):
        self.position.y = y - self.surface.get_height()
        self.velocity.y = 0

    def onAnimation(self, deltaTime):
        self.animator.update(deltaTime)
        self.surface = self.animator.getCurrentFrame()
        if self.velocity.x < 0:
            self.surface = pygame.transform.flip(self.surface, True, False)
