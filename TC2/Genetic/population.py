from Genetic.individual import Individual
from random import shuffle,sample
from tqdm import trange
from math import ceil
import parameters as c

class Population:
    def __init__(self,goal):
        self.population = [Individual() for _ in range(c.POPULATION)] # new random population
        self.goal = goal

    # Calculate every individual fitness and then sort it
    def fitness(self):
        for individual in self.population:
            individual.calculate_fitness(self.goal)
        self.population.sort()

    # Tournament for selection, improve exploration without sacrificing exploitation
    def tournament(self):
        tournament_size = int(c.POPULATION*c.TOURNAMENT_PERCENTAGE)
        tournament = sample(self.population,tournament_size)
        tournament.sort()

        return tournament[0]
            
    # Tournament Selection for the fittest of the population
    def selection(self):
        fittest = []
        fittest_amount = int(c.POPULATION*c.FITTEST_PERCENT)
        while(len(fittest)<fittest_amount):
            fittest.append(self.tournament())
        fittest.sort()
        return fittest

    def new_gen(self):
        self.fitness()

        mutated_amount = int(c.POPULATION*c.MUTATED_PERCENT)

        crossed_amount = int(c.POPULATION*c.CROSSED_PERCENT)
        
        fittest = self.selection()

        mutated = [indiv.mutate() for indiv in (fittest*ceil(mutated_amount/10))[:mutated_amount]]

        pre_crossed = (fittest*ceil(crossed_amount/10))[:crossed_amount] 
        shuffle_crossed = pre_crossed.copy()
        shuffle(shuffle_crossed)
        crossed = [indiv1.crossover(indiv2.DNA) for indiv1,indiv2 in zip(pre_crossed,shuffle_crossed)]
        
        self.population = fittest + mutated + crossed

    # Generation process
    def process_generations(self):
        best_fitness = None
        for generation in trange(c.NUM_GENERATIONS):
            self.new_gen()
            best_fitness = self.population[0]
            print(f"\nGeneration #{generation+1}: Best fitness: {best_fitness.fitness}")
        return best_fitness.img # We return the best result at the end
            
