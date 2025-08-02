from .item import Item
from game.base_entities import Tags, GameObject, getSpawnDistribution
import pygame, random

class PointItemSurfaces:
    GoldPoint = pygame.image.load("assets/Items/gold.png").convert_alpha()
    SilverPoint = pygame.image.load("assets/Items/silver.png").convert_alpha()
    BronzePoint = pygame.image.load("assets/Items/bronze.png").convert_alpha()
    NormalPoint = pygame.image.load("assets/Items/normal.png").convert_alpha()

class PointItem(Item):
    
    POINT_TYPE_DISTRIBUTION = getSpawnDistribution({
        Tags.GoldPoint: 1,
        Tags.SilverPoint: 2,
        Tags.BronzePoint: 4,
        Tags.NormalPoint: 10
    })
    def __init__(self, position: pygame.Vector2):
        tag = random.choice(PointItem.POINT_TYPE_DISTRIBUTION)
        super().__init__(position, tag)

        match(self.tag):
            case Tags.GoldPoint: self.surface = PointItemSurfaces.GoldPoint
            case Tags.SilverPoint: self.surface = PointItemSurfaces.SilverPoint
            case Tags.BronzePoint: self.surface = PointItemSurfaces.BronzePoint
            case Tags.NormalPoint: self.surface = PointItemSurfaces.NormalPoint
        self.surface = pygame.transform.smoothscale(self.surface, (40, 40))
        self.rect = self.surface.get_rect()

        self.debugModeExists = False

    
    def getPoints(self):
        match(self.tag):
            case Tags.GoldPoint: return 100
            case Tags.SilverPoint: return 50
            case Tags.BronzePoint: return 30
            case Tags.NormalPoint: return 10

    def onCollision(self, gameObject: GameObject, gameManager):
        if gameObject.tag == Tags.Player:
            gameManager.updateScore(self.getPoints())
            self.destroy()

    def destroy(self):
        self.isActive = False