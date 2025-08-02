from game.core import Tags, Layers, Animator, AnimationFrame
from game.characters.core.character import Character, CharacterAnimationStates
from game.resources import Resources
import pygame

GAME_WORLD_WRAP = (-50, 1050)

class Player(Character):
    WalkSpeed = 400    
    def __init__(self, position):
        animator = Animator(
            CharacterAnimationStates.Idle,
            {
                CharacterAnimationStates.Idle: [
                    AnimationFrame(0.1, Resources.Robot['idle'])
                ],
                CharacterAnimationStates.Walk: [
                    AnimationFrame(0.1, Resources.Robot['walk0']),
                    AnimationFrame(0.2, Resources.Robot['walk1']),
                    AnimationFrame(0.3, Resources.Robot['walk2']),
                    AnimationFrame(0.4, Resources.Robot['walk3']),
                    AnimationFrame(0.5, Resources.Robot['walk4']),
                    AnimationFrame(0.6, Resources.Robot['walk5']),
                    AnimationFrame(0.7, Resources.Robot['walk6']),
                    AnimationFrame(0.8, Resources.Robot['walk7'])
                ],
                CharacterAnimationStates.Jump: [
                    AnimationFrame(0.1, Resources.Robot['jump'])
                ],
                CharacterAnimationStates.Fall: [
                    AnimationFrame(0.1, Resources.Robot['fall'])
                ],
                CharacterAnimationStates.Kick: [
                    AnimationFrame(0.2, Resources.Robot['kick'])
                ]
            },
            {
                # CharacterAnimationStates.Kick: self.handleKickEnd,
            }
        )
        surface = animator.getCurrentFrame()
        rect = surface.get_rect()
        rect.scale_by_ip(0.7)
        rectOffset = pygame.Vector2(rect.width * 0.22, rect.height * 0.43)
        super().__init__(Layers.Player, [Layers.Enemies, Layers.Items, Layers.Foreground], position, Tags.Player, surface, rect, rectOffset, animator)

        # self.kickCoolDownTimer = Player.KickCoolDownTime
        # self.state = CharacterStates.Idle
        # self.airTime = 0
        # self.debugMode = True
        
    def onUpdate(self, deltaTime):
        self.handleInput()
        super().onUpdate(deltaTime)
        self.handleWorldWrapping()
        self.handleAnimationState()

    def handleInput(self):
        keyState = pygame.key.get_pressed()        

        if keyState[pygame.K_LEFT]:
            self.velocity.x = -Player.WalkSpeed
        elif keyState[pygame.K_RIGHT]:
            self.velocity.x = Player.WalkSpeed
        else: self.velocity.x = 0

    def handleWorldWrapping(self):
        if self.position.x < GAME_WORLD_WRAP[0]: self.position.x = GAME_WORLD_WRAP[1]
        if self.position.x > GAME_WORLD_WRAP[1]: self.position.x = GAME_WORLD_WRAP[0]

    def handleAnimationState(self):
        if self.velocity.x != 0:
            self.animator.setState(CharacterAnimationStates.Walk)
        else:
            self.animator.setState(CharacterAnimationStates.Idle)
