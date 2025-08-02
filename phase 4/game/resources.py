import pygame

class Resources:
    ResourcesLoaded = False
    
    def __init__(self):
        if Resources.ResourcesLoaded: return

        Resources.Adventurer = {
            'idle': pygame.image.load("assets/adventurer/idle.png").convert_alpha(),
            'walk0': pygame.image.load("assets/adventurer/walk0.png").convert_alpha(),
            'walk1': pygame.image.load("assets/adventurer/walk1.png").convert_alpha(),
            'walk2': pygame.image.load("assets/adventurer/walk2.png").convert_alpha(),
            'walk3': pygame.image.load("assets/adventurer/walk3.png").convert_alpha(),
            'walk4': pygame.image.load("assets/adventurer/walk4.png").convert_alpha(),
            'walk5': pygame.image.load("assets/adventurer/walk5.png").convert_alpha(),
            'walk6': pygame.image.load("assets/adventurer/walk6.png").convert_alpha(),
            'walk7': pygame.image.load("assets/adventurer/walk7.png").convert_alpha()
        }

        Resources.Items = {
            'gold': pygame.image.load("assets/items/gold.png").convert_alpha(),
            'silver': pygame.image.load("assets/items/silver.png").convert_alpha(),
            'bronze': pygame.image.load("assets/items/bronze.png").convert_alpha(),
            'normal': pygame.image.load("assets/items/normal.png").convert_alpha(),
            'poison': pygame.image.load("assets/items/poison.png").convert_alpha(),
            'bomb': pygame.image.load("assets/items/bomb.png").convert_alpha(),
            'jump': pygame.image.load("assets/items/jump.png").convert_alpha(),
            'attack': pygame.image.load("assets/items/attack.png").convert_alpha()
        }

        Resources.Effects = {
            'explosion': pygame.image.load("assets/explosion.gif")
        }

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

        Resources.Zombie = {
            'idle': pygame.image.load("assets/zombie/idle.png").convert_alpha(),
            'walk0': pygame.image.load("assets/zombie/walk0.png").convert_alpha(),
            'walk1': pygame.image.load("assets/zombie/walk1.png").convert_alpha(),
            'walk2': pygame.image.load("assets/zombie/walk2.png").convert_alpha(),
            'walk3': pygame.image.load("assets/zombie/walk3.png").convert_alpha(),
            'walk4': pygame.image.load("assets/zombie/walk4.png").convert_alpha(),
            'walk5': pygame.image.load("assets/zombie/walk5.png").convert_alpha(),
            'walk6': pygame.image.load("assets/zombie/walk6.png").convert_alpha(),
            'walk7': pygame.image.load("assets/zombie/walk7.png").convert_alpha()
        }

        Resources.Background = pygame.image.load('assets/background.jpg').convert()

        Resources.ResourcesLoaded = True
