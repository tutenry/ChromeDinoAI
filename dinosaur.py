import pygame
import random
from constants import *

class Dino():
    
    def __init__(self, img=run_imgs[0]):
        self.image = img
        self.running = True
        self.jumping = False
        self.jump_power = 8.5
        self.jump_vel = 8.5
        self.x = 80
        self.y = 310
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

       
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.steps = 0
        
        
    
    def update(self):
        if self.running:
            self.run()
        if self.jumping:
            self.jump()
        if self.steps >= 10:
            self.steps = 0
    
    def jump(self):
        self.image = jump_img
        if self.jumping:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.jump_power:
            self.jumping = False
            self.running = True
            self.jump_vel = self.jump_power
    
    def run(self):
        self.image = run_imgs[self.steps // 5]
        self.rect.x = self.x
        self.rect.y = self.y
        self.steps += 1
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        if info:
            pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
            
            for obs in obstacles:
                pygame.draw.line(screen, self.color, (self.rect.x + 54, self.rect.y + 12), obs.rect.center, 2)