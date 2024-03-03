# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving TSP example)
"""
import random
import cities
from ga_solver import GAProblem, GASolver, Individual
import matplotlib.pyplot as plt

class TSProblem(GAProblem):
    """Implementation of GAProblem for the traveling salesperson problem"""

    def __init__(self, city_dict, threshold_fitness=None):
        super().__init__(threshold_fitness)
        self.city_dict = city_dict

    def how_to_generate_one_random_chromosome(self):
        chromosome = list(self.city_dict.keys())  # Get a list of city names
        random.shuffle(chromosome)
        return chromosome

    def how_to_compute_fitness(self, chromosome):
        return -cities.road_length(self.city_dict, chromosome)

    def new_individual_from_2_parents(self, a, b):
        x_point = len(a.chromosome) // 2
        new_chrom = a.chromosome[:x_point]
        for city in b.chromosome:
            if city not in new_chrom:
                new_chrom.append(city)
        return Individual(new_chrom, self.how_to_compute_fitness(new_chrom))

    def mutation(self, a):
        pos1 = random.randint(0, len(a.chromosome) - 1)
        pos2 = random.randint(0, len(a.chromosome) - 1)
        a.chromosome[pos1], a.chromosome[pos2] = a.chromosome[pos2], a.chromosome[pos1]
        return a


if __name__ == '__main__':
    city_dict = cities.load_cities("cities.txt")
    problem = TSProblem(city_dict)
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until()
    best_individual = solver.get_best_individual()
    cities.draw_cities(city_dict, best_individual.chromosome)
    plt.savefig('best_path2.png')
