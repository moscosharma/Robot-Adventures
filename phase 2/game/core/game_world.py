from game.core.game_object import Layers
import pygame

class GameWorld:
    UpdatingLayers = [Layers.Enemies, Layers.Items, Layers.Player, Layers.Particles, Layers.Foreground]
    CollidingLayers = [Layers.Foreground, Layers.Player, Layers.Enemies, Layers.Items]

    def __init__(self):
        if hasattr(GameWorld, 'World'): return
        GameWorld.World = self

        self.gameObjectsByLayer = {
            Layers.Background: [],
            Layers.Foreground: [],
            Layers.Enemies: [],
            Layers.Items: [],
            Layers.Player: [],
            Layers.Particles: [],
        }

    def addGameObject(self, gameObject):
        self.gameObjectsByLayer[gameObject.layer].append(gameObject)
    
    def update(self, deltaTime):
        for layer in GameWorld.UpdatingLayers:
            for gameObject in self.gameObjectsByLayer[layer]:
                if gameObject.isActive: gameObject.onUpdate(deltaTime)
    
    def animate(self, deltaTime):
        for layer in self.gameObjectsByLayer:
            for gameObject in self.gameObjectsByLayer[layer]:
                if gameObject.isActive: gameObject.onAnimation(deltaTime)

    def handleCollisions(self):
        for layer in GameWorld.CollidingLayers:
            for currentCollider in self.gameObjectsByLayer[layer]:
                if not currentCollider.isActive or not hasattr(currentCollider, 'rect'): continue

                for targetLayer in currentCollider.interactsWith:
                    for otherCollider in self.gameObjectsByLayer[targetLayer]:
                        if not otherCollider.isActive or otherCollider == currentCollider or not hasattr(otherCollider, 'rect'): continue
                        if currentCollider.rect.colliderect(otherCollider.rect):
                            currentCollider.onCollision(otherCollider)
                            otherCollider.onCollision(currentCollider)

    def cleanUp(self):
        for layer in self.gameObjectsByLayer:
            self.gameObjectsByLayer[layer] = [obj for obj in self.gameObjectsByLayer[layer] if obj.isActive]

    def draw(self, screen):
        for layer in self.gameObjectsByLayer:
            for gameObject in self.gameObjectsByLayer[layer]:
                if gameObject.isActive:
                    screen.blit(gameObject.surface, gameObject.position)
                    self.drawDebugRect(screen, gameObject)

    def drawDebugRect(self, screen, gameObject):
        if not gameObject.debugMode: return
        font = pygame.font.Font(None, 24)
        # Draw position vector with x and y direction arrows
        pygame.draw.line(screen, (255, 0, 0), gameObject.position, gameObject.position + pygame.Vector2(50, 0), 2)
        pygame.draw.line(screen, (255, 0, 0), gameObject.position, gameObject.position + pygame.Vector2(0, 50), 2)
        text = font.render(f'{gameObject.tag}{(int(gameObject.position.x), int(gameObject.position.y))}', True, (0, 0, 0))
        screen.blit(text, (gameObject.position.x + 5, gameObject.position.y + 5))

        # Draw rectangle around the gameObject
        if hasattr(gameObject, 'rect'):
            pygame.draw.rect(screen, (0, 255, 0), gameObject.rect, 2)
            text = font.render(f'{(gameObject.rect.w, gameObject.rect.h)}', True, (0, 0, 0))
            screen.blit(text, (gameObject.rect.x + 5, gameObject.rect.y + 5))


    def clear(self):
        for layer in self.gameObjectsByLayer:
            self.gameObjectsByLayer[layer].clear()