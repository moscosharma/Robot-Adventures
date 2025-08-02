from .game_manager import GameManager
import pygame

class GameUI:
    def __init__(self):
        pass

    def update(self, game):
        # Draw FPS on the screen
        if hasattr(game, 'fps'):
            font = pygame.font.Font(None, 36)
            fps_text = font.render(f"FPS: {int(game.fps)}", True, (255, 255, 255))
            game.screen.blit(fps_text, (10, 10))
        
        if not hasattr(game, 'gameManager'): return
        gameManager: GameManager = game.gameManager

        if hasattr(gameManager, 'level'):
            levelText = font.render(f"Level: {int(gameManager.level)}", True, (255, 255, 255))
            game.screen.blit(levelText, (10, 40))

        if hasattr(gameManager, 'score'):
            scoreText = font.render(f"Score: {int(gameManager.score)}", True, (255, 255, 255))
            game.screen.blit(scoreText, (10, 70))

        if hasattr(gameManager, 'jumpTimer'):
            jumpTimerText = font.render(f"Jump Timer: {max(int(gameManager.jumpTimer), 0)}", True, (255, 255, 255))
            game.screen.blit(jumpTimerText, (10, 100))
        if hasattr(gameManager, 'attackTimer'):
            attackTimerText = font.render(f"Attack Timer: {max(int(gameManager.attackTimer), 0)}", True, (255, 255, 255))
            game.screen.blit(attackTimerText, (10, 130))

        if hasattr(gameManager, 'nextLevelTime') and hasattr(gameManager, 'timeElapsed'):
            timeRemaining = gameManager.nextLevelTime - gameManager.timeElapsed
            timeRemainingText = font.render(f"Next Level Timer: {int(timeRemaining)}", True, (0, 0, 0))
            game.screen.blit(timeRemainingText, (10, 580))
