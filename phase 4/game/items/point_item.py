from game.core import getSpawnDistribution, Tags, Layers
from game.items.item import Item
from game.resources import Resources
import pygame, random

class PointItem(Item):
    POINT_TYPE_DISTRIBUTION = getSpawnDistribution({
        Tags.GoldPoint: 1,
        Tags.SilverPoint: 2,
        Tags.BronzePoint: 4,
        Tags.NormalPoint: 10
    })
    def __init__(self, position, itemCollected):
        tag = random.choice(PointItem.POINT_TYPE_DISTRIBUTION)
        match(tag):
            case Tags.GoldPoint: surface = Resources.Items['gold']
            case Tags.SilverPoint: surface = Resources.Items['silver']
            case Tags.BronzePoint: surface = Resources.Items['bronze']
            case Tags.NormalPoint: surface = Resources.Items['normal']
        surface = pygame.transform.smoothscale(surface, (40, 40))
        rect = surface.get_rect()
        super().__init__([Layers.Player], position, tag, surface, rect, pygame.Vector2(), itemCollected)
    
    def getPoints(self):
        match(self.tag):
            case Tags.GoldPoint: return 100
            case Tags.SilverPoint: return 50
            case Tags.BronzePoint: return 30
            case Tags.NormalPoint: return 10
