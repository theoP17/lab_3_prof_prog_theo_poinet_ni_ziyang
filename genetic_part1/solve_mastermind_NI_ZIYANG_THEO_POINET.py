# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for Exercise 1
(Genetic Algorithm Module Specification)
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

class GASolver:
    def __init__(self, selection_rate=0.5, mutation_rate=0.1):
        """Initializes an instance of a GA solver for the Mastermind problem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): Mutation rate between 0 and 1.0. Defaults to 0.1.
        """
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals """
        chromosomes = [mm.generate_random_secret(size=4) for _ in range(pop_size)]
        self._population = [Individual(chromosome, MATCH.rate_guess(chromosome)) for chromosome in chromosomes]

    def evolve_for_one_generation(self):
        """ Apply the process for one generation :
            - Sort the population (Descending order)
            - Selection: Remove x% of population (less adapted)
            - Reproduction: Recreate the same quantity by crossing the surviving ones 
            - Mutation: For each new Individual, mutate with probability mutation_rate
        """
        # Sort our population ascending
        self._population.sort()

        # Removal of the weakest individuals // proportion 100*(1 - selection_rate)%
        proportion_to_delete = int((1 - self._selection_rate) * len(self._population))
        del self._population[:proportion_to_delete]

        # Reproduction of new individuals // Adding the same number of children as deleted parents
        for _ in range(proportion_to_delete):
            first_parent = self.select_random_parent()
            second_parent = self.select_random_parent()
            new_chrom = self.create_child_from_parents(first_parent, second_parent)
            self._population.append(new_chrom)

        # Mutation
        for i in range(len(self._population)):
            if random.random() < self._mutation_rate:
                self._population[i] = self.mutation(self._population[i])

        self._population.sort()

    def create_child_from_parents(self, a, b):
        """ Generate a new individual from two parents """
        x_point = random.randrange(0, len(a.chromosome))
        new_chrom = a.chromosome[0:x_point] + b.chromosome[x_point:]
        return Individual(new_chrom, MATCH.rate_guess(new_chrom))

    def mutation(self, a):
        """ Perform mutation on an individual """
        valid_colors = mm.get_possible_colors()
        new_gene = random.choice(valid_colors)
        pos = random.randint(0, len(a.chromosome) - 1)
        new_chrom = a.chromosome[:pos] + [new_gene] + a.chromosome[pos + 1:]
        return Individual(new_chrom, MATCH.rate_guess(new_chrom))

    def select_random_parent(self):
        """ Select a random parent from the population """
        return random.choice(self._population)

    def get_best_individual(self):
        """ Return the best Individual of the population """
        self._population.sort()
        return self._population[-1]

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two conditions is achieved: 
            - Max nb of generations is achieved
            - The fitness of the best Individual is greater than or equal to threshold_fitness
        """
        for _ in range(max_nb_of_generations):
            self.evolve_for_one_generation()
            if threshold_fitness and self.get_best_individual().fitness >= threshold_fitness:
                break

if __name__ == '__main__':
    # Initialize the Mastermind match
    MATCH = mm.MastermindMatch(secret_size=4)

    # Create a genetic algorithm solver
    solver = GASolver()

    # Reset the population and evolve until a threshold fitness is reached
    solver.reset_population()
    solver.evolve_until(threshold_fitness=MATCH.max_score())

    # Get the best individual and check if the problem is solved
    best = solver.get_best_individual()
    print(f"Best guess: {best.chromosome}")
    print(f"Problem solved? {MATCH.is_correct(best.chromosome)}")
