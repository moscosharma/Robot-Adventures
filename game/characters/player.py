from ..base_entities import Layers, DebugMode, Tags, GAME_WORLD_WRAP, GameObject, Animator, Direction
import pygame

class PlayerStates:
    Idle = 'idle'
    Kick = 'kick'
    Jump = 'jump'
    Walk = 'walk'


class Player(GameObject):
    Gravity = 1000
    WalkSpeed = 400
    JumpSpeed = 500
    RunningSpeed = 300
    Friction = 100
    AirTimeDetectionThreshold = 0.1  # Threshold to detect if the player is in the air
    KickSpeed = 800
    KickCoolDownTime = 0.3
    def __init__(self, position: pygame.Vector2, updateScore):
        super().__init__(
            Layers.Player,
            [ Layers.Enemies, Layers.Items, Layers.Foreground ],
            position,
            Tags.Player
        )

        self.updateScore = updateScore
        self.speed = pygame.Vector2(Player.RunningSpeed, 0)  # Speed in pixels per second
        self.animator = Animator(
            'idle',
            True,
            idle = [
                {
                    'nextFrameTime': 0.1,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_idle.png").convert_alpha()
                }
            ],
            walk = [
                {
                    'nextFrameTime': 0.1,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_walk0.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.2,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_walk1.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.3,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_walk2.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.4,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_walk3.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.5,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_walk4.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.6,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_walk5.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.7,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_walk6.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.8,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_walk7.png").convert_alpha()
                }
            ],
            jump = [
                {
                    'nextFrameTime': 0.1,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_jump.png").convert_alpha()
                }
            ],
            fall = [
                {
                    'nextFrameTime': 0.1,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_fall.png").convert_alpha()
                }
            ],
            attack = [
                {
                    'nextFrameTime': 0.05,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_attack0.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.2,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_attack1.png").convert_alpha()
                },
                {
                    'nextFrameTime': 0.3,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_attack2.png").convert_alpha()
                }
            ],
            kick = [
                {
                    'nextFrameTime': 0.2,
                    'frame': pygame.image.load("assets/Robot/PNG/Poses/character_robot_kick.png").convert_alpha()
                }
            ]
        )
        rect = self.animator.getCurrentFrame().get_rect()  # Get the rect of the first frame
        self.rect = pygame.Rect(0, 0, rect.width * 0.7, rect.height * 0.7)
        self.rectOffset = pygame.Vector2(rect.width * 0.15, rect.height * 0.3)  # Offset for the rect to align with the feet
        self.airTime = 0  # Time spent in the air
        self.kickCoolDownTimer = Player.KickCoolDownTime
        self.rectDebugColor = (0, 255, 0, 0.3)  # Semi-transparent green for player debug rect
        self.debugModeExists = False  # Enable debug mode for this game object
        self.state = PlayerStates.Idle
        self.direction = Direction.Idle
        self.lastDirection = Direction.Idle

        self.canJump = False
        self.canAttack = False


    def onUpdate(self, deltaTime, gameWorld):
        self.handleCoolDowns(deltaTime)
        self.handleInput()  # Handle player input
        self.handlePhysics(deltaTime, gameWorld)  # Handle physics updates
        self.handleWorldWrapping()
        self.handlePlayerRect()
        self.handleAnimationState()  # Update animation state based on speed
        self.airTime += deltaTime

    def handleCoolDowns(self, deltaTime): 
        if self.kickCoolDownTimer > 0:
            self.kickCoolDownTimer = max(0, self.kickCoolDownTimer - deltaTime)

    def handleWorldWrapping(self):
        if self.position.x < GAME_WORLD_WRAP[0]: self.position.x = GAME_WORLD_WRAP[1]
        if self.position.x > GAME_WORLD_WRAP[1]: self.position.x = GAME_WORLD_WRAP[0]

    def handlePlayerRect(self):
        self.rect.x = self.rectOffset.x + self.position.x
        self.rect.y = self.rectOffset.y + self.position.y

    def isAnyActionInProgress(self):
        return self.state in [PlayerStates.Kick]

    def handleInput(self):
        keyState = pygame.key.get_pressed()        
        if keyState[pygame.K_UP] and self.airTime < Player.AirTimeDetectionThreshold and self.state != PlayerStates.Jump and self.canJump:
            self.state = PlayerStates.Jump
            self.speed.y = -Player.JumpSpeed  # Move up
        elif keyState[pygame.K_k] and not self.isAnyActionInProgress() and self.kickCoolDownTimer == 0 and self.canAttack:
            self.state = PlayerStates.Kick
        elif not self.isAnyActionInProgress():
            self.state = PlayerStates.Idle

        if self.direction != Direction.Idle: self.lastDirection = self.direction

        if keyState[pygame.K_LEFT]:
            self.direction = Direction.Left
            if self.state == PlayerStates.Idle: self.state = PlayerStates.Walk
        elif keyState[pygame.K_RIGHT]:
            self.direction = Direction.Right
            if self.state == PlayerStates.Idle: self.state = PlayerStates.Walk
        else: self.direction = Direction.Idle

        # print(self.state, self.direction)

    def handlePhysics(self, deltaTime, gameWorld):
    
        match(self.state):
            case PlayerStates.Kick: self.speed.x = Player.KickSpeed * (-1 if self.lastDirection == 'left' else 1)
            case PlayerStates.Walk: self.speed.x = Player.WalkSpeed * (-1 if self.lastDirection == 'left' else 1)
            case PlayerStates.Idle: self.speed.x = 0

        self.speed.y = min(self.speed.y + Player.Gravity * deltaTime, 1000)
        self.position.x += self.speed.x * deltaTime
        self.position.y = self.position.y + self.speed.y * deltaTime


    def handleAttackEnd(self):
        self.attack = False
        self.state = PlayerStates.Idle
        self.animator.setState('idle')  # Reset to idle state after attack

    def handleKickEnd(self):
        self.kick = False
        self.state = PlayerStates.Idle
        self.animator.setState('idle')
        self.kickCoolDownTimer = Player.KickCoolDownTime

    def handleAnimationState(self):
        if self.state == PlayerStates.Kick:
            self.animator.setState('kick', loop=False)
            self.animator.setAnimationEndCallback(self.handleKickEnd)
        elif self.speed.y < 0:
            self.animator.setState('jump', loop=True)  # Set jump state
        elif self.speed.y > 0 and self.airTime > Player.AirTimeDetectionThreshold:
            self.animator.setState('fall', loop=True)  # Set fall state
        elif self.speed.x != 0:
            self.animator.setState('walk', loop=True)  # Set walk state
        else:
            self.animator.setState('idle', loop=True)  # Set idle state

    def standAt(self, y):
        self.position.y = y - self.surface.get_height()
        self.airTime = 0
        self.speed.y = 0

    def onAnimation(self, deltaTime):
        self.animator.update(deltaTime)
        self.surface = self.animator.getCurrentFrame()
        # self.currentFrame = self.surface 
        # if hasattr(self, 'lastFrame') and self.lastFrame is not self.currentFrame:
        #     print('Animation frame changed', self.game.getTotalTimeElapsed())
        # self.lastFrame = self.currentFrame
        if self.speed.x < 0:
            self.surface = pygame.transform.flip(self.surface, True, False)

    def onCollision(self, gameObject: GameObject, gameManager):
        if gameObject.tag == Tags.TileMap:
            self.airTime = 0
            self.speed.y = 0

        # if isinstance(otherGameObject, Enemy):
        #     self.health -= 10
        #     print(f"Player collided with enemy! Health: {self.health}")
