import pygame
from game import GameWorld, GameManager, GameUI

GAME_NAME = 'Robot Adventures'
GAME_WINDOW = (1000, 600)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(GAME_WINDOW)
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()
        GameWorld()
        GameManager()
        GameUI() 
        self.isRunning = True
        self.isFrozen = False

    def run(self):
        while self.isRunning:
            self.handleWindowEvents()

            deltaTime = self.clock.tick(60) / 1000
            if self.isFrozen: continue

            GameManager.Manager.update(deltaTime)
            GameWorld.World.update(deltaTime)
            GameWorld.World.handleCollisions()
            GameWorld.World.cleanUp()
            GameWorld.World.animate(deltaTime)
            GameWorld.World.draw(self.screen)
            GameUI.UI.update(deltaTime, self.screen)
            pygame.display.flip()

    def handleWindowEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.isRunning = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                self.isFrozen = not self.isFrozen
    
game = Game()
game.run()
