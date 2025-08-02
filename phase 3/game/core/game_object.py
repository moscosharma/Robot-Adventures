class Layers:
    Background = "Background"
    Foreground = "Foreground"
    Player = "Player"
    Enemies = "Enemies"
    Items = "Items"
    Particles = "Particles"

class Tags:
    # Item Tags
    PlatformExplosive = 'platformExplosive'
    PlayerExplosive = 'playerExplosive'
    GoldPoint = 'goldPoint'
    SilverPoint = 'silverPoint'
    BronzePoint = 'bronzePoint'
    NormalPoint = 'normalPoint'
    JumpItem = 'jumpItem'
    AttackItem = 'attackItem'

    # Character Tags
    Player = 'player'

    # Enemy Tags
    AdventurerEnemy = 'adventurerEnemy'
    ZombieEnemy = 'zombieEnemy'

    # Other Tags
    TileMap = 'tileMap'
    Background = 'background'
    Particles = 'particles'

class GameObject:
    def __init__(self, layer, interactsWith, position, tag, surface):
        self.isActive = True
        self.layer = layer
        self.interactsWith = interactsWith
        self.position = position
        self.tag = tag
        self.surface = surface
        self.debugMode = False

    def onUpdate(self, deltaTime): pass

    def onCollision(self, gameObject): pass

    def onAnimation(self, deltaTime): pass

    def destroy(self): self.isActive = False
