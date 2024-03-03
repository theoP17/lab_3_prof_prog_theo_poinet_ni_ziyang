# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import mastermind as mm
import random

class Individual:
    """Represents an Individual for a genetic algorithm"""

    def __init__(self, chromosome: list, fitness: float):
        """Initializes an Individual for a genetic algorithm 

        Args:
            chromosome (list[]): a list representing the individual's chromosome
            fitness (float): the individual's fitness (the higher, the better the fitness)
        """
        self.chromosome = chromosome
        self.fitness = fitness

    def __lt__(self, other):
        """Implementation of the less_than comparator operator"""
        return self.fitness < other.fitness

    def __repr__(self):
        """Representation of the object for print calls"""
        return f'Indiv({self.fitness:.1f},{self.chromosome})'


class GASolver:
    def __init__(self, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a ga_solver for a given GAProblem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): mutation_rate between 0 and 1.0. Defaults to 0.1.
        """
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals """
        chrom_initial = mm.get_possible_colors()
        for _ in range(pop_size):
            chromosome = [random.choice(chrom_initial) for _ in range(len(chrom_initial))]
            fitness = mm.MastermindMatch().rate_guess(chromosome)
            self._population.append(Individual(chromosome, fitness))

    def evolve_for_one_generation(self):
        """ Apply the process for one generation : 
            -	Sort the population (Descending order)
            -	Selection: Remove x% of population (less adapted)
            -   Reproduction: Recreate the same quantity by crossing the 
                surviving ones 
            -	Mutation: For each new Individual, mutate with probability 
                mutation_rate i.e., mutate it if a random value is below   
                mutation_rate
        """
        self._population.sort(reverse=True)  # Sort by fitness in descending order

        # Selection
        num_to_keep = int(len(self._population) * self._selection_rate)
        self._population = self._population[:num_to_keep]

        # Reproduction
        while len(self._population) < num_to_keep:
            parent1 = random.choice(self._population)
            parent2 = random.choice(self._population)
            x_point = random.randrange(0, len(parent1.chromosome))
            new_chrom = parent1.chromosome[:x_point] + parent2.chromosome[x_point:]
            new_fitness = mm.MastermindMatch().rate_guess(new_chrom)
            self._population.append(Individual(new_chrom, new_fitness))

        # Mutation
        for individual in self._population:
            if random.random() < self._mutation_rate:
                mutation_point = random.randint(0, len(individual.chromosome) - 1)
                new_gene = random.choice(mm.get_possible_colors())
                individual.chromosome[mutation_point] = new_gene
                individual.fitness = mm.MastermindMatch().rate_guess(individual.chromosome)

        self._population.sort(reverse=True)  # Sort again after mutation

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        print("Generation summary:")
        print(f"Current population: {self._population}")
        print(f"Population size: {len(self._population)}")
        print(f"Best individual: {self.get_best_individual()}")
        print(f"Best fitness score: {self.get_best_individual().fitness}")

    def get_best_individual(self):
        """ Return the best Individual of the population """
        return self._population[0]  # Since it's sorted in descending order, the first one has the highest fitness

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        for _ in range(max_nb_of_generations):
            if threshold_fitness and self.get_best_individual().fitness >= threshold_fitness:
                break
            self.evolve_for_one_generation()

city_dict = mm.MastermindMatch().generate_random_guess()
solver = GASolver()
solver.reset_population()
solver.evolve_until(threshold_fitness=mm.MastermindMatch().max_score())

best = solver.get_best_individual()
print(f"Best guess {best.chromosome}")
print(f"Problem solved? {mm.MastermindMatch().is_correct(best.chromosome)}")
