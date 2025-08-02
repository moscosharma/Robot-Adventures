from game.core import Tags, Layers, Animator, AnimationFrame, Resources, GameWorld, Explosion
from game.characters.core.character import Character, CharacterAnimationStates, Direction
import pygame

GAME_WORLD_WRAP = (-50, 1050)

class PlayerStates:
    Idle = 'idle'
    Kick = 'kick'
    Jump = 'jump'
    Walk = 'walk'

class Player(Character):
    WalkSpeed = 400    
    JumpSpeed = 500
    KickSpeed = 800
    KickCoolDownTime = 0.3
    AirTimeDetectionThreshold = 0.1
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
                CharacterAnimationStates.Kick: self.handleKickEnd,
            }
        )
        surface = animator.getCurrentFrame()
        rect = surface.get_rect()
        rect.scale_by_ip(0.7)
        rectOffset = pygame.Vector2(rect.width * 0.22, rect.height * 0.43)
        super().__init__(Layers.Player, [Layers.Enemies, Layers.Items, Layers.Foreground], position, Tags.Player, surface, rect, rectOffset, animator)

        self.kickCoolDownTimer = Player.KickCoolDownTime
        self.state = PlayerStates.Idle
        self.airTime = 0
        self.canJump = False
        self.canAttack = False
        self.direction = Direction.Idle
        self.lastDirection = Direction.Idle

    def onUpdate(self, deltaTime):
        self.handleCoolDowns(deltaTime)
        self.handleInput()
        super().onUpdate(deltaTime)
        self.handleWorldWrapping()
        self.handleAnimationState()
        self.airTime += deltaTime

    def handleCoolDowns(self, deltaTime): 
        if self.kickCoolDownTimer > 0:
            self.kickCoolDownTimer = max(0, self.kickCoolDownTimer - deltaTime)

    def handleInput(self):
        keyState = pygame.key.get_pressed()        

        if keyState[pygame.K_UP] and self.canJump and self.airTime < Player.AirTimeDetectionThreshold and self.state != PlayerStates.Jump:
            self.state = PlayerStates.Jump
            Resources.Sounds['jump'].stop()
            Resources.Sounds['jump'].play().set_volume(0.5)
            self.velocity.y = -Player.JumpSpeed
        elif keyState[pygame.K_a] and self.canAttack and self.state != PlayerStates.Kick and self.kickCoolDownTimer <= 0:
            self.state = PlayerStates.Kick
            Resources.Sounds['kick'].stop()
            Resources.Sounds['kick'].play()
        elif self.state != PlayerStates.Kick:
            self.state = PlayerStates.Idle

        if self.direction != Direction.Idle: self.lastDirection = self.direction

        if keyState[pygame.K_LEFT]:
            self.direction = Direction.Left
            if self.state == PlayerStates.Idle: self.state = PlayerStates.Walk
        elif keyState[pygame.K_RIGHT]:
            self.direction = Direction.Right
            if self.state == PlayerStates.Idle: self.state = PlayerStates.Walk
        else: self.direction = Direction.Idle

        directionMultiplier = -1 if self.lastDirection == Direction.Left else 1
        match(self.state):
            case PlayerStates.Kick: self.velocity.x = Player.KickSpeed * directionMultiplier
            case PlayerStates.Walk: self.velocity.x = Player.WalkSpeed * directionMultiplier
            case PlayerStates.Idle: self.velocity.x = 0

    def handleWorldWrapping(self):
        if self.position.x < GAME_WORLD_WRAP[0]: self.position.x = GAME_WORLD_WRAP[1]
        if self.position.x > GAME_WORLD_WRAP[1]: self.position.x = GAME_WORLD_WRAP[0]

    def handleAnimationState(self):
        if self.state == PlayerStates.Kick:
            self.animator.setState(CharacterAnimationStates.Kick)
        elif self.velocity.y < 0:
            self.animator.setState(CharacterAnimationStates.Jump)
        elif self.velocity.y > 0 and self.airTime > Player.AirTimeDetectionThreshold:
            self.animator.setState(CharacterAnimationStates.Fall)
        elif self.velocity.x != 0:
            self.animator.setState(CharacterAnimationStates.Walk)
        else:
            self.animator.setState(CharacterAnimationStates.Idle)

    def handleKickEnd(self):
        self.state = PlayerStates.Idle
        self.animator.setState(CharacterAnimationStates.Idle)
        self.kickCoolDownTimer = Player.KickCoolDownTime

    def onCollision(self, gameObject):
        if gameObject.tag == Tags.TileMap:
            self.airTime = 0
            self.velocity.y = 0
