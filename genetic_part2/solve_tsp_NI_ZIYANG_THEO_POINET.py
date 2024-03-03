# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for Exercise 1
(Genetic Algorithm Module Specification)
"""
import matplotlib.pyplot as plt
import cities
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
        """Initializes an instance of a GA solver for the TSP problem

        Args:
            selection_rate (float, optional): Selection rate between 0 and 1.0. Defaults to 0.5.
            mutation_rate (float, optional): Mutation rate between 0 and 1.0. Defaults to 0.1.
        """
        self._selection_rate = selection_rate
        self._mutation_rate = mutation_rate
        self._population = []

    def reset_population(self, pop_size=50):
        """ Initialize the population with pop_size random Individuals """
        chromosomes = [cities.default_road(city_dict).copy() for _ in range(pop_size)]
        for chromosome in chromosomes:
            random.shuffle(chromosome)
        self._population = [Individual(chromosome, -cities.road_length(city_dict, chromosome)) for chromosome in chromosomes]

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
        proportion_to_delete = (1 - self._selection_rate) * len(self._population)
        del self._population[:int(proportion_to_delete)]

        # Reproduction of new individuals // Adding the same number of children as deleted parents
        for _ in range(int(proportion_to_delete)):
            first_parent = random.choice(self._population)
            second_parent = random.choice(self._population)
            new_chrom = self.new_individual_from_2_parents(first_parent, second_parent)
            self._population.append(new_chrom)

        # Mutation
        for i in range(len(self._population)):
            if random.random() < self._mutation_rate:
                self._population[i] = self.mutation(self._population[i])

        self._population.sort()

    def new_individual_from_2_parents(self, a, b):
        new_chrom = a.chromosome[:len(a.chromosome)//2]
        for city in b.chromosome:
            if city not in new_chrom:
                new_chrom.append(city)
        return Individual(new_chrom, -cities.road_length(city_dict, new_chrom))

    def mutation(self, a):
        pos_1 = random.randint(0, len(a.chromosome)-1)
        pos_2 = random.randint(0, len(a.chromosome) - 1)
        new_chrom = a.chromosome.copy()
        new_chrom[pos_1], new_chrom[pos_2] = new_chrom[pos_2], new_chrom[pos_1]
        return Individual(new_chrom, -cities.road_length(city_dict, new_chrom))

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
    # Load cities
    city_dict = cities.load_cities("cities.txt")

    # Create GASolver instance
    solver = GASolver()

    # Initialize population
    solver.reset_population()

    # Evolve until solution is found
    solver.evolve_until()

    # Get the best individual
    best = solver.get_best_individual()

    # Draw the cities with the best path found
    cities.draw_cities(city_dict, best.chromosome)

    plt.savefig('best_path.png')
