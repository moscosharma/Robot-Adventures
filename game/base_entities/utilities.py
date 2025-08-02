import pygame, random

def getSpawnDistribution(distribution: dict):
    spawnDistribution = []
    for item, frequency in distribution.items():
        spawnDistribution.extend([item] * frequency)

    return tuple(spawnDistribution)

def getRandomPosition(topLeftVector, bottomRightVector) -> pygame.Vector2:
    x = random.randint(topLeftVector[0], bottomRightVector[0])
    y = random.randint(topLeftVector[1], bottomRightVector[1])
    return pygame.Vector2(x, y)