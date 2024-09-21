import pygame
import os

pygame.init()

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800

info = False

run_imgs = [pygame.image.load(os.path.join("Images/Dino", "DinoRun1.png")), pygame.image.load(os.path.join("Images/Dino", "DinoRun2.png"))]
jump_img = pygame.image.load(os.path.join("Images/Dino", "DinoJump.png"))
background = pygame.image.load(os.path.join("Images/Other", "Track.png"))
small_cactus = [pygame.image.load(os.path.join("Images/Cactus", "SmallCactus1.png")),
pygame.image.load(os.path.join("Images/Cactus", "SmallCactus2.png")),
pygame.image.load(os.path.join("Images/Cactus", "SmallCactus3.png"))]

large_cactus = [pygame.image.load(os.path.join("Images/Cactus", "LargeCactus1.png")),
pygame.image.load(os.path.join("Images/Cactus", "LargeCactus2.png")),
pygame.image.load(os.path.join("Images/Cactus", "LargeCactus3.png"))]

obstacles = []

font = pygame.font.Font("freesansbold.ttf", 20)