from game.game_manager import GameManager
import pygame

BlackColor = (0, 0, 0)
WhiteColor = (255, 255, 255)

class GameUI:
    def __init__(self):
        if hasattr(GameUI, 'UI'): return
        GameUI.UI = self

    def update(self, deltaTime, screen):
        self.handleInput()
        if hasattr(GameManager.Manager, 'isRunning') and not GameManager.Manager.isRunning:
            self.gameOverUI(screen)
        else:
            self.duringGameUI(screen, deltaTime)

    def renderText(self, screen, text, fontSize, color, position):
        font = pygame.font.Font(None, fontSize)
        textSurface = font.render(text, True, color)
        screen.blit(textSurface, position)

    def duringGameUI(self, screen, deltaTime):
        fps = int(1 / deltaTime)
        self.renderText(screen, f'FPS: {fps}', 36, WhiteColor, (10, 10))

        if hasattr(GameManager.Manager.gameStats, 'level'):
            level = int(GameManager.Manager.gameStats.level)
            self.renderText(screen, f'Level: {level}', 36, WhiteColor, (10, 40))

        if hasattr(GameManager.Manager.gameStats, 'score'):
            score = int(GameManager.Manager.gameStats.score)
            self.renderText(screen, f'Score: {score}', 36, WhiteColor, (10, 70))

        if hasattr(GameManager.Manager, 'jumpTimer'):
            jumpTimer = max(int(GameManager.Manager.jumpTimer), 0)
            self.renderText(screen, f'Jump: {jumpTimer}', 36, WhiteColor, (10, 100))
            
        if hasattr(GameManager.Manager, 'attackTimer'):
            attackTimer = max(int(GameManager.Manager.attackTimer), 0)
            self.renderText(screen, f'Attack: {attackTimer}', 36, WhiteColor, (10, 130))

        if hasattr(GameManager.Manager, 'enemyCount'):
            enemyCount = max(int(GameManager.Manager.enemyCount), 0)
            self.renderText(screen, f'Enemy: {enemyCount}', 36, WhiteColor, (10, 160))

        if hasattr(GameManager.Manager, 'nextLevelTime') and hasattr(GameManager.Manager, 'timeElapsed'):
            timeRemaining = int(GameManager.Manager.nextLevelTime - GameManager.Manager.timeElapsed)
            self.renderText(screen, f'Next Level Timer: {timeRemaining}', 36, BlackColor, (10, 580))

    def gameOverUI(self, screen):
        canvas = pygame.Surface((1000, 600))
        canvas.fill(WhiteColor)
        screen.blit(canvas, (0, 0))
        if hasattr(GameManager.Manager.gameStats, 'score'):
            score = int(GameManager.Manager.gameStats.score)
            self.renderText(screen, f'Score: {score}', 80, BlackColor, (350, 200))

        if hasattr(GameManager.Manager.gameStats, 'highScore'):
            highScore = int(GameManager.Manager.gameStats.highScore)
            self.renderText(screen, f'High Score: {highScore}', 36, BlackColor, (380, 280))

        self.renderText(screen, 'Press enter to restart game', 36, BlackColor, (310, 350))

    def handleInput(self):
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_RETURN] and not GameManager.Manager.isRunning:
            GameManager.Manager.start_game()
