import pygame
import os
import random
import sys
from constants import *
from dinosaur import Dino
from obstacle import SmallCactus, LargeCactus
import neat
import math
import pickle

pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def remove(index):
    dinos.pop(index)
    dino_genomes.pop(index)
    dino_networks.pop(index)

def distance(pos1, pos2):
    x = pos1[0] - pos2[0]
    y = pos1[1] - pos2[1]
    return math.sqrt(x**2 + y**2)


def eval_genomes(genomes, config):
    global background_x, background_y, points, obstacles, dinos, dino_genomes, dino_networks, game_speed
    game_speed = 20
    clock = pygame.time.Clock()
    points = 0

    dinos = []
    dino_genomes = []
    dino_networks = []

    
    background_x = 0
    background_y = 380
    
    #Fill the dino, genome, and network lists with data
    for genome_id, genome in genomes:
        dinos.append(Dino())
        dino_genomes.append(genome)
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        dino_networks.append(network)
        genome.fitness = 0

    def score():
        global points, game_speed, dino_genomes
        points+=1
        for dino in dino_genomes:
            dino.fitness += 0.1
        if points % 100 == 0:
            game_speed+=1
        text = font.render(f"Points: {str(points)}", True, (0,0,0))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 50))

    def stats():
        global dinos, game_speed, dino_genomes
        alive_text = font.render(f"Dinosaurs Alive: {str(len(dinos))}", True, (0,0,0))
        generation_text = font.render(f"Generation: {population.generation+1}", True, (0,0,0))
        speed_text = font.render(f"Game Speed: {str(game_speed)}", True, (0,0,0))

        screen.blit(alive_text, (50, 450))
        screen.blit(generation_text, (50, 480))
        screen.blit(speed_text, (50, 510))

    def move_background():
        global background_x, background_y
        image_width = background.get_width()
        screen.blit(background, (background_x, background_y))
        screen.blit(background, (image_width + background_x, background_y))

        if background_x <= -image_width:
            background_x = 0
        background_x -= game_speed

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((255, 255, 255))

        for dino in dinos:
            dino.update()
            dino.draw(screen)
        
        if len(dinos) == 0:
            break
            
        if len(obstacles) == 0:
            randnum = random.randint(0, 1)
            if randnum == 0:
                obstacles.append(SmallCactus(small_cactus, random.randint(0, 2)))
            elif randnum == 1:
                obstacles.append(LargeCactus(large_cactus, random.randint(0, 2)))
        
        for obs in obstacles:
            obs.draw(screen)
            obs.update(game_speed)

            for i, dino in enumerate(dinos):
                if dino.rect.colliderect(obs.rect):
                    dino_genomes[i].fitness -= 5
                    remove(i)
        

        for i, dino in enumerate(dinos):
            output = dino_networks[i].activate((dino.rect.y, distance((dino.rect.x, dino.rect.y), obs.rect.midtop)))

            if output[0] > 0.5 and dino.rect.y == dino.y:
                dino.jumping = True
                dino.running = False

        stats()
        score()
        move_background()
        clock.tick(30)
        

        pygame.display.update()

def main(genome, config):
    global background_x, background_y, points, obstacles2, game_speed
    game_speed = 20
    clock = pygame.time.Clock()
    points = 0

    network = neat.nn.FeedForwardNetwork.create(genome, config)

    obstacles2 = []
    dinos = [Dino()]

    background_x = 0
    background_y = 380
    

    def score():
        global points, game_speed, dino_genomes
        points+=1
        if points % 100 == 0:
            game_speed+=1
        text = font.render(f"Points: {str(points)}", True, (0,0,0))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 50))

    def move_background():
        global background_x, background_y
        image_width = background.get_width()
        screen.blit(background, (background_x, background_y))
        screen.blit(background, (image_width + background_x, background_y))

        if background_x <= -image_width:
            background_x = 0
        background_x -= game_speed

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((255, 255, 255))

        dinos[0].update()
        dinos[0].draw(screen)
        
        if len(dinos) == 0:
            break
            
        if len(obstacles) == 0:
            randnum = random.randint(0, 1)
            if randnum == 0:
                obstacles.append(SmallCactus(small_cactus, random.randint(0, 2)))
            elif randnum == 1:
                obstacles.append(LargeCactus(large_cactus, random.randint(0, 2)))
        
        for obs in obstacles:
            obs.draw(screen)
            obs.update(game_speed)

            for i, dino in enumerate(dinos):
                if dino.rect.colliderect(obs.rect):
                    dino_genomes[i].fitness -= 5
                    remove(i)
        

        
        output = network.activate((dino.rect.y, distance((dino.rect.x, dino.rect.y), obs.rect.midtop)))

        for i, dino in enumerate(dinos):
            output = network.activate((dino.rect.y, distance((dino.rect.x, dino.rect.y), obs.rect.midtop)))
            if output[0] > 0.5 and dino.rect.y == dino.y:
                dino.jumping = True
                dino.running = False

        score()
        move_background()
        clock.tick(30)
        
        pygame.display.update()

#Setup AI
def run():
    
    global population

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    best = population.run(eval_genomes, 50)
    with open("best.pickle", "wb") as file:
        pickle.dump(best, file)

def run_ai():
    with open("best.pickle", "rb") as file:
        best = pickle.load(file)
        main(best, config)
    


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEATConfigFile.txt")

    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    run()
