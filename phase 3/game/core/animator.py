class AnimationFrame:
    def __init__(self, nextFrameTime, frame):
        self.frame = frame
        self.nextFrameTime = nextFrameTime

class Animator:
    def __init__(self, state, frames, stateEndCallbacks):
        self.frames = frames
        self.current_frame = 0
        self.time_elapsed = 0.0
        self.state = state
        self.stateEndCallbacks = stateEndCallbacks
        self.isActive = True

    def update(self, deltaTime):
        if not self.isActive: return
        self.time_elapsed += deltaTime
        if self.time_elapsed >= self.frames[self.state][self.current_frame].nextFrameTime:
            self.nextFrame()

    def loop(self):
        self.current_frame = 0
        self.isActive = True
        self.time_elapsed = 0.0

    def setState(self, state):
        if state in self.frames and state != self.state:
            self.state = state
            self.current_frame = 0
            self.isActive = True
            self.time_elapsed = 0.0

    def nextFrame(self):
        if self.current_frame < len(self.frames[self.state]) - 1:
            self.current_frame += 1
        else: 
            self.isActive = False
            callback = self.stateEndCallbacks.get(self.state)

            if callback and callable(callback): callback()
            else: self.loop()

    def getCurrentFrame(self):
        return self.frames[self.state][self.current_frame].frame