from .base_entities import Layers, DebugMode, GameObject
import pygame

class GameWorld:
    def __init__(self):
        self.gameObjectsByLayer: dict[Layers, list[GameObject]] = {
            Layers.Background: [],
            Layers.Foreground: [],
            Layers.Enemies: [],
            Layers.Items: [],
            Layers.Player: [],
            Layers.Particles: [],
        }
        
        # self.drawBuffer = []

    def addGameObject(self, gameObject: GameObject):
        if not hasattr(gameObject, 'layer'):
            raise ValueError("GameObject must have a 'layer' attribute.")
        if gameObject.layer not in self.gameObjectsByLayer: 
            raise ValueError(f"Layer '{gameObject.layer}' is not defined in GameWorld.Layers.")
        
        self.gameObjectsByLayer[gameObject.layer].append(gameObject)
        gameObject.onCreate()
    
    def update(self, deltaTime: float):
        for layer in self.gameObjectsByLayer:
            for gameObject in self.gameObjectsByLayer[layer]:
                if gameObject.isActive:
                    gameObject.onUpdate(deltaTime, self)
    
    def animate(self, deltaTime: float):
        for layer in self.gameObjectsByLayer:
            for gameObject in self.gameObjectsByLayer[layer]:
                if gameObject.isActive:
                    gameObject.onAnimation(deltaTime)

    def handleCollisions(self, gameManager):
        count = 0
        for layer in self.gameObjectsByLayer:
            for currentGameObject in self.gameObjectsByLayer[layer]:
                count += 1
                if not currentGameObject.isActive: continue

                for target in currentGameObject.targets:
                    for otherGameObject in self.gameObjectsByLayer[target]:
                        if not otherGameObject.isActive: continue
                        if otherGameObject == currentGameObject: continue
                        if currentGameObject.rect.colliderect(otherGameObject.rect):
                            currentGameObject.onCollision(otherGameObject, gameManager)
                            otherGameObject.onCollision(currentGameObject, gameManager)
        # print(count)

    def cleanUp(self):
        for layer in self.gameObjectsByLayer:
            self.gameObjectsByLayer[layer] = [obj for obj in self.gameObjectsByLayer[layer] if obj.isActive]

    def renderGameObjects(self, screen: pygame.Surface):
        for layer in self.gameObjectsByLayer:
            for gameObject in self.gameObjectsByLayer[layer]:
                if gameObject.isActive and gameObject.surface:
                    screen.blit(gameObject.surface, gameObject.position)
                    if (DebugMode):
                        self.drawDebugRect(screen, gameObject)
        
        # for item in self.drawBuffer:
        #     pygame.draw.rect(screen, **item)
        # self.drawBuffer = []

    def drawDebugRect(self, screen, gameObject: GameObject):
        if not hasattr(gameObject, 'debugModeExists') or not gameObject.debugModeExists: return
        # Draw position vector with x and y direction arrows
        pygame.draw.line(screen, (255, 0, 0), gameObject.position, gameObject.position + pygame.Vector2(100, 0), 2)
        pygame.draw.line(screen, (0, 255, 0), gameObject.position, gameObject.position + pygame.Vector2(0, 100), 2)

        # Draw rectangle around the gameObject
        pygame.draw.rect(screen, (255, 255, 255), gameObject.rect, 1)

        font = pygame.font.Font(None, 24)
        text = font.render(f'{gameObject.tag}{(gameObject.rect.w, gameObject.rect.h)}', True, (0, 0, 0))
        screen.blit(text, (gameObject.rect.x + 5, gameObject.rect.y + 5))
        
    def getGameObjectsByLayer(self, layer: Layers) -> [GameObject]:
        return self.gameObjectsByLayer[layer]
    # def appendDrawCommand(self, drawCommand):
    #     self.drawBuffer.append(drawCommand)