from game.core.game_object import GameObject, Layers, Tags
from game.core.animator import AnimationFrame, Animator
from game.core.resources import Resources
import pygame

class Effect(GameObject):
    def __init__(self, position, surface, animator):
        super().__init__(Layers.Particles, [], position, Tags.Particles, surface)
        self.animator = animator

    def onAnimation(self, deltaTime):
        self.animator.update(deltaTime)

class ExplosionStates:
    Idle = 'idle'

class Explosion(Effect):
    def __init__(self, position):
        animator = Animator(
            ExplosionStates.Idle,
            {
                ExplosionStates.Idle: [AnimationFrame(0.1, Resources.Effects['explosion'])]
            },
            {
                ExplosionStates.Idle: self.destroy
            }
        )
        surface = animator.getCurrentFrame()
        finalPosition = position - pygame.Vector2(surface.get_rect().w / 2, surface.get_rect().h / 2)
        super().__init__(finalPosition, surface, animator)
