from game.base_entities import getRandomPosition
from .constants import ItemTypes
from .point_item import PointItem
from .platform_explosive import PlatformExplosive
from .player_explosive import PlayerExplosive
from .jump_item import JumpItem
from .attack_item import AttackItem
from .item import Item
import pygame

class ItemSpawner:
    def __init__(self, spawnAreaTopLeft, spawnAreaBottomRight):
        self.spawnAreaTopLeft = spawnAreaTopLeft
        self.spawnAreaBottomRight = spawnAreaBottomRight

    def spawnItem(self, item: ItemTypes, position: pygame.Vector2 = None) -> Item:
        if not position: position = getRandomPosition(self.spawnAreaTopLeft, self.spawnAreaBottomRight)
        match(item):
            case ItemTypes.Point: return PointItem(position)
            case ItemTypes.PlatformExplosive: return PlatformExplosive(position)
            case ItemTypes.PlayerExplosive: return PlayerExplosive(position)
            case ItemTypes.Jump: return JumpItem(position)
            case ItemTypes.Attack: return AttackItem(position)
