import pygame
from constants import *

class Obstacle():
    
    def __init__(self, image, cactus_type):
        self.image = image
        self.type = cactus_type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
    
    def update(self, game_speed):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
    
    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)
    

class SmallCactus(Obstacle):
    def __init__(self, image, cactus_type):
        super().__init__(image, cactus_type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image, cactus_type):
        super().__init__(image, cactus_type)
        self.rect.y = 300