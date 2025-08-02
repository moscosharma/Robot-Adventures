from game.core import GameWorld
from game.platform import TileMap, Background
from game.resources import Resources

class GameManager:
    def __init__(self):
        if hasattr(GameManager, 'Manager'): return
        GameManager.Manager = self
        Resources()
        self.isRunning = False
        self.start_game()

    def start_game(self):
        GameWorld.World.clear()
        self.isRunning = True

        GameWorld.World.addGameObject(Background())
        GameWorld.World.addGameObject(TileMap())

    def update(self, deltaTime): pass