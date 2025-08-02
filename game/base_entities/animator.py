import pygame

class Animator:
    def __init__(self, state, loop = False, **frames):
        self.frames = frames
        self.current_frame = 0
        self.time_elapsed = 0.0
        self.state = state
        self.loop = loop
        self.isActive = True

    def update(self, deltaTime: int):
        if not self.isActive:
            return
        self.time_elapsed += deltaTime
        if self.time_elapsed >= self.frames.get(self.state)[self.current_frame].get('nextFrameTime'):
            self.nextFrame()

    def setState(self, state, loop = False):
        if state in self.frames and state != self.state:
            self.state = state
            self.current_frame = 0
            self.isActive = True
            self.loop = loop
            self.time_elapsed = 0.0

    def nextFrame(self):
        # print(self.state, self.current_frame, self.time_elapsed)
        if self.current_frame < len(self.frames.get(self.state)) - 1:
            self.current_frame += 1
        elif self.loop:
            self.time_elapsed -= self.frames.get(self.state)[self.current_frame].get('nextFrameTime')
            self.current_frame = 0
        else: 
            if hasattr(self, 'callback') and callable(self.callback):
                # print(self.state, self.current_frame, self.time_elapsed, 'callback called')
                self.isActive = False
                self.callback()

    def getCurrentFrame(self) -> pygame.Surface:
        # print(self.state, self.current_frame, self.time_elapsed)
        return self.frames.get(self.state)[self.current_frame].get('frame')
    
    def setAnimationEndCallback(self, callback):
        self.callback = callback