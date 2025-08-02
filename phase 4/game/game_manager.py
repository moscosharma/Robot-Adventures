from game.core import GameWorld, getSpawnDistribution, Tags, getRandomPosition
from game.platform import TileMap, Background
from game.characters import Player
from game.resources import Resources
from game.items import ItemTypes, PointItem, PlatformExplosive, PlayerExplosive, JumpItem, AttackItem
import pygame, random

TOP_LEFT_ITEM_SPAWNER = (100, -300)
BOTTOM_RIGHT_ITME_SPAWNER = (900, -100)

class GameStats:
    MAX_LEVEL = 4
    def __init__(self):
        self.level = 0
        self.score = 0
        self.highScore = 0
        self.timeElapsed = 0

    def reset(self):
        self.level = 0
        self.score = 0
        self.timeElapsed = 0

    def updateScore(self, scoreDelta):
        self.score += scoreDelta
        self.highScore = max(self.highScore, self.score)

    def levelUp(self):
        self.level = min(self.level + 1, GameStats.MAX_LEVEL)

class LevelItemConfig:
    def __init__(self, timeGap, distribution):
        self.timeGap = timeGap
        self.distribution = getSpawnDistribution(distribution)

class LevelEnemyConfig:
    def __init__(self, timeGap, distribution, maxEnemyAllowed):
        self.timeGap = timeGap,
        self.distribution = getSpawnDistribution(distribution)
        self.maxEnemyAllowed = maxEnemyAllowed

class LevelConfigs:
    Items = [
        LevelItemConfig(0, {}),
        LevelItemConfig(3, { ItemTypes.Point: 8, ItemTypes.PlatformExplosive: 2 }),
        LevelItemConfig(3, { ItemTypes.Point: 7, ItemTypes.PlatformExplosive: 2, ItemTypes.PlayerExplosive: 1 }),
        LevelItemConfig(2, { ItemTypes.Point: 5, ItemTypes.PlatformExplosive: 3, ItemTypes.PlayerExplosive: 2 }),
        LevelItemConfig(1, { ItemTypes.Point: 4, ItemTypes.PlatformExplosive: 3, ItemTypes.PlayerExplosive: 3 }),
        LevelItemConfig(3, { ItemTypes.Point: 6, ItemTypes.PlatformExplosive: 2, ItemTypes.PlayerExplosive: 1, ItemTypes.Jump: 1 }),
        LevelItemConfig(5, { ItemTypes.Point: 6, ItemTypes.PlatformExplosive: 1, ItemTypes.PlayerExplosive: 1, ItemTypes.Jump: 2 }),
        LevelItemConfig(5, { ItemTypes.Point: 5, ItemTypes.PlayerExplosive: 1, ItemTypes.Jump: 3, ItemTypes.Attack: 1 }),
        LevelItemConfig(5, { ItemTypes.Point: 5, ItemTypes.Jump: 3, ItemTypes.Attack: 2 }),
        LevelItemConfig(5, { ItemTypes.Point: 5, ItemTypes.Jump: 3, ItemTypes.Attack: 2 }),
    ]
    Enemy = [
        LevelEnemyConfig(0, {}, 0),
        LevelEnemyConfig(0, {}, 0),
        LevelEnemyConfig(0, {}, 0),
        LevelEnemyConfig(0, {}, 0),
        LevelEnemyConfig(0, {}, 0),
        # LevelEnemyConfig(4, { EnemyTypes.Adventurer: 10 }, 1),
        # LevelEnemyConfig(4, { EnemyTypes.Adventurer: 10 }, 2),
        # LevelEnemyConfig(4, { EnemyTypes.Adventurer: 10 }, 3),
        # LevelEnemyConfig(4, { EnemyTypes.Adventurer: 7, EnemyTypes.Zombie: 3 }, 3),
        # LevelEnemyConfig(4, { EnemyTypes.Adventurer: 5, EnemyTypes.Zombie: 5 }, 4),
    ]

class GameManager:
    JUMP_ENABLE_TIME = 1 * 60
    ATTACK_ENABLE_TIME = 1 * 60
    TIME_BETWEEN_LEVELS = 1 * 3

    def __init__(self):
        if hasattr(GameManager, 'Manager'): return
        GameManager.Manager = self
        Resources()
        self.gameStats = GameStats()
        self.isRunning = False
        self.start_game()

    def start_game(self):
        GameWorld.World.clear()
        self.isRunning = True
        self.gameStats.reset()

        self.nextLevelTime = 0
        self.nextItemSpawnTime = 1.0
        
        self.jumpTimer = 0
        self.attackTimer = 0

        GameWorld.World.addGameObject(Background())
        GameWorld.World.addGameObject(TileMap())
        self.player = Player(pygame.Vector2(110, 110))
        GameWorld.World.addGameObject(self.player)
        self.levelUp()

    def setItemSpawnConfigs(self, itemConfig):
        self.SpawnItemTimeGap = itemConfig.timeGap
        self.ItemSpawnDistribution = itemConfig.distribution

    def setEnemySpawnConfigs(self, enemyConfig):
        self.SpawnEnemyTimeGap = enemyConfig.timeGap
        self.EnemySpawnDistribution = enemyConfig.distribution
        self.maxEnemyAllowed = enemyConfig.maxEnemyAllowed

    def levelUp(self):
        if self.gameStats.timeElapsed < self.nextLevelTime: return
        self.gameStats.levelUp()
        self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS

        self.setItemSpawnConfigs(LevelConfigs.Items[self.gameStats.level])
        self.setEnemySpawnConfigs(LevelConfigs.Enemy[self.gameStats.level])

    def update(self, deltaTime):
        if self.isRunning == False: return

        self.gameStats.timeElapsed += deltaTime
        self.handleLevel()
        self.handlePlayerCapabilities(deltaTime)
        if self.player.position.y > 800: self.playerKilled()

    def handleLevel(self):
        if self.gameStats.timeElapsed > self.nextLevelTime:
            self.levelUp()

        self.handleItemSpawning()

    def handlePlayerCapabilities(self, deltaTime):
        self.jumpTimer -= deltaTime
        self.attackTimer -= deltaTime
        if self.jumpTimer <= 0: self.player.canJump = False
        if self.attackTimer <= 0: self.player.canAttack = False

    def enableJump(self):
        self.jumpTimer = GameManager.JUMP_ENABLE_TIME
        self.player.canJump = True

    def enableAttack(self):
        self.player.canAttack = True
        self.attackTimer = GameManager.ATTACK_ENABLE_TIME

    def playerKilled(self):
        self.player.destroy()
        self.gameOver()

    def itemCollected(self, item):
        match(item.tag):
            case Tags.GoldPoint | Tags.SilverPoint | Tags.BronzePoint | Tags.NormalPoint:
                self.gameStats.updateScore(item.getPoints())
            case Tags.PlayerExplosive:
                self.playerKilled()
            case Tags.JumpItem:
                self.enableJump()
            case Tags.AttackItem:
                self.enableAttack()

    def handleItemSpawning(self):
        if self.gameStats.timeElapsed < self.nextItemSpawnTime: return
        self.nextItemSpawnTime += self.SpawnItemTimeGap
        itemType = random.choice(self.ItemSpawnDistribution)
        item = self.spawnItem(itemType)
        GameWorld.World.addGameObject(item)

    def spawnItem(self, item):
        position = getRandomPosition(TOP_LEFT_ITEM_SPAWNER, BOTTOM_RIGHT_ITME_SPAWNER)
        match(item):
            case ItemTypes.Point: return PointItem(position, self.itemCollected)
            case ItemTypes.PlatformExplosive: return PlatformExplosive(position)
            case ItemTypes.PlayerExplosive: return PlayerExplosive(position, self.itemCollected)
            case ItemTypes.Jump: return JumpItem(position, self.itemCollected)
            case ItemTypes.Attack: return AttackItem(position, self.itemCollected)

    def gameOver(self):
        self.isRunning = False



