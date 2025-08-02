from .base_entities import TOP_LEFT_ITEM_SPAWNER, BOTTOM_RIGHT_ITME_SPAWNER, getSpawnDistribution, ENEMY_SPAWN_EXTREMES, Tags
from .items.item_spawner import ItemTypes, ItemSpawner, Item
from .enemies.enemy_spawner import EnemySpawner, EnemyTypes
from .world import TileMap, Background
from .game_world import GameWorld
from .characters import Player
import random, pygame

class GameManager:
    JUMP_ENABLE_TIME = 1 * 60
    ATTACK_ENABLE_TIME = 1 * 60
    MAX_LEVEL = 9
    TIME_BETWEEN_LEVELS = 7  # seconds
    def __init__(self, gameWorld):
        self.itemSpawner = ItemSpawner(TOP_LEFT_ITEM_SPAWNER, BOTTOM_RIGHT_ITME_SPAWNER)
        self.level = 8
        self.highScore = 0
        self.isRunning = False
        self.start_game(gameWorld)

    def start_game(self, gameWorld: GameWorld):
        self.timeElapsed = 0.0
        self.nextItemSpawnTime = 1.0
        self.score = 0
        self.isRunning = True
        self.jumpTimer = 0
        self.attackTimer = 0

        self.nextEnemyTime = 1
        self.maxEnemyCount = 1
        self.enemyCount = 0

        gameWorld.addGameObject(Background())
        gameWorld.addGameObject(TileMap())
        self.player = Player(pygame.Vector2(110, 110), self.updateScore)
        gameWorld.addGameObject(self.player)
        self.enemySpawner = EnemySpawner(self.player, ENEMY_SPAWN_EXTREMES)
        self.levelUp()

    def updateScore(self, scoreDelta):
        self.score += scoreDelta

    def gameOver(self):
        self.isRunning = False
        pass

    def levelUp(self):
        if not hasattr(self, 'level'): self.level = 1
        else: self.level = min(self.level + 1, GameManager.MAX_LEVEL)
        if not hasattr(self, 'nextLevelTime'): self.nextLevelTime = 0
        if self.timeElapsed < self.nextLevelTime: return

        match(self.level):
            case 1:
                self.SpawnItemTimeGap = 3 # 3 sec
                self.ItemSpawnDistribution = getSpawnDistribution({
                    ItemTypes.Point: 8,
                    ItemTypes.PlatformExplosive: 2
                })
                self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS
            case 2:
                self.SpawnItemTimeGap = 3 # 3 sec
                self.ItemSpawnDistribution = getSpawnDistribution({
                    ItemTypes.Point: 7,
                    ItemTypes.PlatformExplosive: 2,
                    ItemTypes.PlayerExplosive: 1
                })
                self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS
            case 3:
                self.SpawnItemTimeGap = 2 # 3 sec
                self.ItemSpawnDistribution = getSpawnDistribution({
                    ItemTypes.Point: 5,
                    ItemTypes.PlatformExplosive: 3,
                    ItemTypes.PlayerExplosive: 2
                })
                self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS
            case 4: 
                self.SpawnItemTimeGap = 1 # 3 sec
                self.ItemSpawnDistribution = getSpawnDistribution({
                    ItemTypes.Point: 4,
                    ItemTypes.PlatformExplosive: 3,
                    ItemTypes.PlayerExplosive: 3
                })
                self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS
            case 5:
                self.SpawnItemTimeGap = 3
                self.ItemSpawnDistribution = getSpawnDistribution({
                    ItemTypes.Point: 6,
                    ItemTypes.PlatformExplosive: 2,
                    ItemTypes.PlayerExplosive: 1,
                    ItemTypes.Jump: 1
                })
                self.SpawnEnemyTimeGap = 4
                self.EnemySpawnDistribution = getSpawnDistribution({
                    EnemyTypes.Adventurer: 10
                })
                self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS
            case 6:
                self.SpawnItemTimeGap = 5
                self.ItemSpawnDistribution = getSpawnDistribution({
                    ItemTypes.Point: 6,
                    ItemTypes.PlatformExplosive: 1,
                    ItemTypes.PlayerExplosive: 1,
                    ItemTypes.Jump: 2
                })
                self.SpawnEnemyTimeGap = 4
                self.EnemySpawnDistribution = getSpawnDistribution({
                    EnemyTypes.Adventurer: 10
                })
                self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS
                self.maxEnemyCount = 2
            case 7:
                self.SpawnItemTimeGap = 5
                self.ItemSpawnDistribution = getSpawnDistribution({
                    ItemTypes.Point: 5,
                    ItemTypes.PlayerExplosive: 1,
                    ItemTypes.Jump: 3,
                    ItemTypes.Attack: 1
                })
                self.SpawnEnemyTimeGap = 4
                self.EnemySpawnDistribution = getSpawnDistribution({
                    EnemyTypes.Adventurer: 10
                })
                self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS
                self.maxEnemyCount = 3
            case 8:
                self.SpawnItemTimeGap = 5
                self.ItemSpawnDistribution = getSpawnDistribution({
                    ItemTypes.Point: 5,
                    ItemTypes.Jump: 3,
                    ItemTypes.Attack: 2
                })
                self.SpawnEnemyTimeGap = 4
                self.EnemySpawnDistribution = getSpawnDistribution({
                    EnemyTypes.Adventurer: 7,
                    EnemyTypes.Zombie: 3
                })
                self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS
                self.maxEnemyCount = 3
            case 9:
                self.SpawnItemTimeGap = 5
                self.ItemSpawnDistribution = getSpawnDistribution({
                    ItemTypes.Point: 5,
                    ItemTypes.Jump: 3,
                    ItemTypes.Attack: 2
                })
                self.SpawnEnemyTimeGap = 4
                self.EnemySpawnDistribution = getSpawnDistribution({
                    EnemyTypes.Adventurer: 5,
                    EnemyTypes.Zombie: 5
                })
                self.nextLevelTime += GameManager.TIME_BETWEEN_LEVELS
                self.maxEnemyCount = 4

    def update(self, deltaTime: float, gameWorld: GameWorld):
        self.timeElapsed += deltaTime
        self.handleLevel(gameWorld)
        self.handlePlayerCapabilities(deltaTime)

    def handlePlayerCapabilities(self, deltaTime: float):
        self.jumpTimer -= deltaTime
        self.attackTimer -= deltaTime
        if self.jumpTimer <= 0: self.player.canJump = False
        if self.attackTimer <= 0: self.player.canAttack = False

    def handleLevel(self, gameWorld: GameWorld):
        if not hasattr(self, 'level'): return

        if self.timeElapsed > self.nextLevelTime:
            self.levelUp()

        match(self.level):
            case 1 | 2 | 3 | 4: self.handlePhase1Levels(gameWorld)
            case 5 | 6 | 7 | 8 | 9: self.handlePhase2Levels(gameWorld)
            case _: self.handlePhase1Levels(gameWorld)

    def handlePhase1Levels(self, gameWorld: GameWorld):
        self.handleItemSpawning(gameWorld)

    def handlePhase2Levels(self, gameWorld: GameWorld):
        self.handleItemSpawning(gameWorld)
        self.handleEnemySpawning(gameWorld)
        
    def handleItemSpawning(self, gameWorld: GameWorld):
        if self.timeElapsed < self.nextItemSpawnTime: return

        self.nextItemSpawnTime += self.SpawnItemTimeGap
        itemType = random.choice(self.ItemSpawnDistribution)
        item = self.itemSpawner.spawnItem(itemType)
        gameWorld.addGameObject(item)

    def handleEnemySpawning(self, gameWorld: GameWorld):
        if self.timeElapsed > self.nextEnemyTime and self.enemyCount < self.maxEnemyCount:
            enemyType = random.choice(self.EnemySpawnDistribution)
            enemy = self.enemySpawner.spawnEnemy(enemyType)
            self.nextEnemyTime += self.SpawnEnemyTimeGap
            
            if not enemy: return

            gameWorld.addGameObject(enemy)
            self.enemyCount += 1

    def enableJump(self):
        self.jumpTimer = GameManager.JUMP_ENABLE_TIME
        self.player.canJump = True

    def enableAttack(self):
        self.player.canAttack = True
        self.attackTimer = GameManager.ATTACK_ENABLE_TIME

    def itemCollected(self, item: Item):
        match(item.tag):
            case Tags.GoldPoint | Tags.SilverPoint | Tags.BronzePoint | Tags.NormalPoint:
                self.updateScore(item.getPoints())
            case Tags.PlayerExplosive:
                self.gameOver()
            case Tags.JumpItem:
                self.enableJump()
            case Tags.AttackItem:
                self.enableAttack()

    def enemyKilled(self, enemy):
        self.enemyCount -= 1
        if self.enemyCount < 0: self.enemyCount = 0

        match(enemy.tag):
            case Tags.AdventurerEnemy:
                self.updateScore(100)
            case Tags.ZombieEnemy:
                self.updateScore(200)
            case _:
                pass
    
