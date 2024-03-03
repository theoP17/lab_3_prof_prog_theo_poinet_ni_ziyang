# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2022

@author: tdrumond & agademer

Template file for your Exercise 3 submission 
(GA solving Mastermind example)
"""
from ga_solver import *
import mastermind as mm
import random

class MastermindProblem(GAProblem):
    """Implementation of GAProblem for the mastermind problem"""

    def __init__(self, match):
        super().__init__(self)
        self.match = match
        self.threshold_fitness = self.match.max_score()

    def how_to_generate_one_random_chromosome(self):
        return mm.generate_random_secret(size=self.match.secret_size())

    def how_to_compute_fitness(self, chromosome):
        return self.match.rate_guess(chromosome)

    def new_individual_from_2_parents(self, a, b):
        x_point = random.randrange(0, len(a.chromosome))
        new_chrom = a.chromosome[0:x_point] + b.chromosome[x_point:]
        return Individual(new_chrom, self.match.rate_guess(new_chrom))

    def mutation(self, a):
        valid_colors = mm.get_possible_colors()
        new_gene = random.choice(valid_colors)
        pos = random.randint(0, len(a.chromosome) - 1)
        new_chrom = a.chromosome[0:pos] + [new_gene] + a.chromosome[pos + 1:]
        return Individual(new_chrom, self.match.rate_guess(new_chrom))

if __name__ == '__main__':
    from ga_solver import GASolver
    match = mm.MastermindMatch(secret_size=6)
    problem = MastermindProblem(match)
    solver = GASolver(problem)
    solver.reset_population()
    solver.evolve_until()

    # print(
    # f"Best guess {mm.encode_guess(solver.getBestDNA())} {solver.get_best_individual()}")
    print(
        f"Best guess {solver.get_best_individual().chromosome} {solver.get_best_individual()}")
    print(
        f"Problem solved? {match.is_correct(solver.get_best_individual().chromosome)}")
