# -*- coding: utf-8 -*-
'''
    Run
    ===

    Provides
      * Orchestrates the game execution and the evolution logic
'''

import numpy as np

from brain import Brain
from classes import Bird
from game import FlappyBirdGame

def create_birds(n=10):
    ''' Creates a list of n Birds with random weights

    Arguments
    ---------
    n - int, number of birds to create

    Returns
    -------
    Returns a list of Birds
    '''

    birds = []
    for count in range(n):

        w1 = np.random.rand(6,2)
        w2 = np.random.rand(1,6)
        brain = Brain(w1,w2)

        new_bird = Bird(x=230,y=350,brain=brain)
        birds.append(new_bird)

    return birds

def evolve(birds, fitness):

    #Sort birds by fitness
    birds_and_fitness = list(zip(birds, fitness))
    birds_and_fitness = sorted(birds_and_fitness, key=lambda x: x[1],reverse=True)
    sorted_birds = [bird for bird,_ in birds_and_fitness]

    new_birds = []

    #Pass the winners to the next generation
    for bird in sorted_birds[:4]:
        w1 = bird.brain.weights1
        w2 = bird.brain.weights2
        new_brain = Brain(w1, w2)
        bird_replica = Bird(x=230,y=350, brain=new_brain)
        new_birds.append(bird_replica)

    #Breed the winners
    new_birds.append(sorted_birds[0]+sorted_birds[1])
    new_birds.append(sorted_birds[0]+sorted_birds[2])
    new_birds.append(sorted_birds[1]+sorted_birds[2])

    #Mutate the winners (add gaussian noise to weights)
    new_birds.append(sorted_birds[0]+sorted_birds[0])
    new_birds.append(sorted_birds[1]+sorted_birds[1])
    new_birds.append(sorted_birds[2]+sorted_birds[2])

    return new_birds

birds = create_birds()
flappy_bird_game = FlappyBirdGame()

for generation in range(50):

    birds_fitness = flappy_bird_game.run(birds)
    birds = evolve(birds, birds_fitness)

    flappy_bird_game.reset(title=f'GEN {generation}')

flappy_bird_game.quit()
