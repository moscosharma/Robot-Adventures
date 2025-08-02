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
    Default = 'default'
    Background = 'background'

class Direction:
    Left = 'left'
    Right = 'right'
    Idle = 'idle'

DebugMode = True

GAME_NAME = 'My Game'
GAME_WINDOW = (1000, 600)
TOP_LEFT_ITEM_SPAWNER = (100, -300)
BOTTOM_RIGHT_ITME_SPAWNER = (900, -100)
GAME_WORLD_WRAP = (-50, GAME_WINDOW[0] + 50)
ENEMY_SPAWN_EXTREMES = (-200, 1200)
