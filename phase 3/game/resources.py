import pygame

class Resources:
    ResourcesLoaded = False
    
    def __init__(self):
        if Resources.ResourcesLoaded: return

        Resources.Robot = {
            'idle': pygame.image.load("assets/robot/idle.png").convert_alpha(),
            'walk0': pygame.image.load("assets/robot/walk0.png").convert_alpha(),
            'walk1': pygame.image.load("assets/robot/walk1.png").convert_alpha(),
            'walk2': pygame.image.load("assets/robot/walk2.png").convert_alpha(),
            'walk3': pygame.image.load("assets/robot/walk3.png").convert_alpha(),
            'walk4': pygame.image.load("assets/robot/walk4.png").convert_alpha(),
            'walk5': pygame.image.load("assets/robot/walk5.png").convert_alpha(),
            'walk6': pygame.image.load("assets/robot/walk6.png").convert_alpha(),
            'walk7': pygame.image.load("assets/robot/walk7.png").convert_alpha(),
            'jump': pygame.image.load("assets/robot/jump.png").convert_alpha(),
            'fall': pygame.image.load("assets/robot/fall.png").convert_alpha(),
            'kick': pygame.image.load("assets/robot/kick.png").convert_alpha()
        }

        Resources.Background = pygame.image.load('assets/background.jpg').convert()

        Resources.ResourcesLoaded = True
