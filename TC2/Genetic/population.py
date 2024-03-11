from Genetic.individual import Individual
import parameters as c
from tqdm import trange
from math import ceil
from random import shuffle
import matplotlib.pyplot as plt

class Population:
    def __init__(self,goal):
        self.population = [Individual() for _ in range(c.POPULATION)]
        self.goal = goal

    def fitness(self):
        for individual in self.population:
            individual.calculate_fitness(self.goal)
        self.population.sort()

    def new_gen(self):
        self.fitness()

        mutated_amount = int(c.POPULATION*c.MUTATED_PERCENT)

        crossed_amount = int(c.POPULATION*c.CROSSED_PERCENT)
        
        fittest = self.population[:int(c.POPULATION*c.FITTEST_PERCENT)]

        mutated = [indiv.mutate() for indiv in (fittest*ceil(mutated_amount/10))[:mutated_amount]]

        pre_crossed = (fittest*ceil(crossed_amount/10))[:crossed_amount]
        shuffle_crossed = pre_crossed.copy()
        shuffle(shuffle_crossed)
        crossed = [indiv1.crossover(indiv2.DNA) for indiv1,indiv2 in zip(pre_crossed,shuffle_crossed)]
        
        self.population = fittest + mutated + crossed

    def process_generations(self):
        best_fitness = None
        for generation in trange(c.NUM_GENERATIONS):
            self.new_gen()
            best_fitness = self.population[0]
            print(f"\nGeneration #{generation+1}: Best fitness: {best_fitness.fitness}")
        return best_fitness.img
            
