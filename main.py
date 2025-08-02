import setup
import pygame
from game import GameWorld, GameManager, GameUI, GAME_WINDOW, GAME_NAME

class Game:
    def __init__(self, dimensions, title):
        self.screen = setup.screen
        self.clock = setup.clock
        self.gameWorld = GameWorld()
        self.gameManager = GameManager(self.gameWorld)
        self.gameUI = GameUI() 
        self.running = True
        self.isFrozen = False

    def run(self):
        while self.running:
            if self.gameManager.isRunning == False: 
                print(self.gameManager.isRunning)
                self.running = False
            self.handleWindowEvents()
            deltaTime = self.clock.tick(60) / 1000.0  # Time in seconds since last frame
            if self.isFrozen:
                continue

            self.gameParameterCalculation(deltaTime)
            self.gameManager.update(deltaTime, self.gameWorld)
            self.gameWorld.update(deltaTime)
            self.gameWorld.handleCollisions(self.gameManager)
            self.gameWorld.animate(deltaTime)
            self.gameWorld.cleanUp()
            self.gameWorld.renderGameObjects(self.screen)
            self.gameUI.update(self)
            pygame.display.flip()

    def gameParameterCalculation(self, deltaTime: float):
        self.fps = int(1 / deltaTime)

    def handleWindowEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                self.isFrozen = not self.isFrozen
    
game = Game(GAME_WINDOW, GAME_NAME)
game.run()
