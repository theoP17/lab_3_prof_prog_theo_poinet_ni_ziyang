# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 11:24:15 2022

@author: agademer & tdrumond

Template for exercise 1
(genetic algorithm module specification)
"""

import mastermind as mm
import random


# def mutation(a):
#     valid_colors = mm.get_possible_colors()
#     new_gene = random.choice(valid_colors)
#     pos = random.randint(0,len(a.chromosome)-1)
#     new_chrom = a.chromosome[0:pos] + [new_gene] + a.chromosome[pos + 1:]
#     return Individual(new_chrom, MATCH.rate_guess(new_chrom))


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
        chromosome = MATCH.generate_random_guess()
        fitness = MATCH.rate_guess(chromosome)
        new_individual = Individual(chromosome, fitness)
        self._population.append(new_individual)

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
        #chose the best 20% individuals
        self._population.sort(reverse=True)
        # Calculate the index up to which you want to keep the elements (20% of the length of the list)
        keep_index = int(len(self._population) * self._selection_rate)
        # Slice the list to keep the first 20% of individuals
        first_20_percent = self._population[:keep_index]

        #reproduction
        len_first_20_percent = len(first_20_percent)
        r_stop = random.randrange(0,len_first_20_percent)
        a = first_20_percent[r_stop] #chose a parent at random in the first20percents
        b = first_20_percent[random.randrange(0,len_first_20_percent)]

        x_point = random.randrange(0, len(a.chromosome)) #take a crossing point at random
        new_chrom = a.chromosome[0:x_point] + b.chromosome[x_point:] #create a new chromosome
        new_individual = Individual(new_chrom, MATCH.rate_guess(new_chrom))
        

        #mutation
        valid_colors = mm.get_possible_colors()
        new_gene = random.choice(valid_colors)
        pos = random.randint(0,len(a.chromosome)-1)
        new_chrom = a.chromosome[0:pos] + [new_gene] + a.chromosome[pos + 1:]

    def show_generation_summary(self):
        """ Print some debug information on the current state of the population """
        pass  # REPLACE WITH YOUR CODE

    def get_best_individual(self):
        """ Return the best Individual of the population """
        self._population.sort(reverse=True)
        best_indiv = self[0]
        return best_indiv  # REPLACE WITH YOUR CODE

    def evolve_until(self, max_nb_of_generations=500, threshold_fitness=None):
        """ Launch the evolve_for_one_generation function until one of the two condition is achieved : 
            - Max nb of generation is achieved
            - The fitness of the best Individual is greater than or equal to
              threshold_fitness
        """
        for i in range(max_nb_of_generations):
            self.evolve_for_one_generation()
            if self._population[-1].fitness >= threshold_fitness:
                break

MATCH = mm.MastermindMatch(secret_size=4)
solver = GASolver()
solver.reset_population()
solver.evolve_until(threshold_fitness=MATCH.max_score())

