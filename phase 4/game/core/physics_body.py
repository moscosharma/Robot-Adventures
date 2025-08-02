from game.core.game_object import GameObject

class PhysicsBody(GameObject):
    def __init__(self, layer, interactsWith, position, tag, surface, rect, rectOffset, velocity, gravity):
        super().__init__(layer, interactsWith, position, tag, surface)
        self.rect = rect
        self.velocity = velocity
        self.gravity = gravity
        self.rectOffset = rectOffset

    def onUpdate(self, deltaTime):
        self.velocity.y = min(self.velocity.y + self.gravity * deltaTime, 1000)
        self.position += self.velocity * deltaTime

        rectPosition = self.position + self.rectOffset
        self.rect.x = rectPosition.x
        self.rect.y = rectPosition.y
        
