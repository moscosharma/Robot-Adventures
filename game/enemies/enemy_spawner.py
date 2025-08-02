from game.characters import Player
from .constants import EnemyTypes
from .adventurer_enemy import AdventurerEnemy
from .zombie_enemy import ZombieEnemy
import pygame

class EnemySpawner:
    def __init__(self, player: Player, extremes: tuple[int, int]):
        self.playerTarget = player
        self.extremes = extremes

    def spawnEnemy(self, enemy: EnemyTypes):
        if not hasattr(self, 'playerTarget'): return

        spawnPosition = self.getPositionToSpawn()
        match(enemy):
            case EnemyTypes.Adventurer: return AdventurerEnemy(spawnPosition)
            case EnemyTypes.Zombie: return ZombieEnemy(spawnPosition, self.playerTarget)

    def getPositionToSpawn(self):
        diffFromFirstExtreme = abs(self.playerTarget.position.x - self.extremes[0])
        diffFromSecondExtreme = abs(self.playerTarget.position.x - self.extremes[1])
        if diffFromFirstExtreme < diffFromSecondExtreme:
            return pygame.Vector2(self.extremes[1], self.playerTarget.position.y)
        else:
            return pygame.Vector2(self.extremes[0], self.playerTarget.position.y)