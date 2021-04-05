import numpy as np
import random
from termcolor import colored

ITERATIONS = 10
GENERATION_SIZE = 800
POPULATION_SIZE = 400
MUTATION_RATE = 0.025
ELITE_SIZE = POPULATION_SIZE // 3


class City:
    def __init__(self, coord):
        self.x = coord[0]
        self.y = coord[1]

    def distance(self, city):
        return np.sqrt((self.x - city.x) ** 2 + (self.y - city.y) ** 2)

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'


class Route:
    def __init__(self, path):
        self.path = path
        self.distance = self.route_distance()
        self.fitness = self.route_fitness()
        self.probability = 0

    def route_distance(self):
        path_distance = 0
        for i in range(0, len(self.path)):
            city_a = self.path[i]
            city_b = None
            if i + 1 < len(self.path):
                city_b = self.path[i + 1]
            else:
                city_b = self.path[0]
            path_distance += city_a.distance(city_b)
        return path_distance

    def route_fitness(self):
        return 1 / (float(self.distance) + 1)

    def __repr__(self):
        return colored(f'D: {self.distance}\t\t', 'green') + \
                colored(f'F: {self.fitness}\t\t', 'magenta') + \
                colored(f'P: {self.probability}\t\t', 'yellow') + \
                colored(f'{self.path}', 'red')


def mutate(chromosome):
    if MUTATION_RATE - random.random() > 0:
        index_a = random.randint(0, len(chromosome.path) - 1)
        index_b = random.randint(0, len(chromosome.path) - 1)
        chromosome.path[index_a], chromosome.path[index_b] = \
            chromosome.path[index_b], chromosome.path[index_a]
    return chromosome


def mutate_population(population):
    mutated_population = []
    for i in range(len(population)):
        mutated = mutate(population[i])
        mutated_population.append(mutated)
    return mutated_population


def crossover(parent1, parent2):
    part_one = []
    part_two = []
    start_ind, end_ind = sorted([random.randrange(len(parent1.path)) for _ in range(2)])
    for i in range(start_ind, end_ind):
        part_one.append(parent1.path[i])
    part_two = [item for item in parent2.path if item not in part_one]
    return Route(part_one + part_two)


def next_population(old_population):
    new_population = []
    for i in range(ELITE_SIZE):
        new_population.append(old_population[i])
    for i in range(ELITE_SIZE, len(old_population)):
        new_population.append(crossover(old_population[i - 1], old_population[i]))
    return new_population


def roulette_wheel(ranked_population):
    selection = []
    for i in range(ELITE_SIZE):
        selection.append(ranked_population[i])
    for i in range(ELITE_SIZE, POPULATION_SIZE):
        r = random.random()
        index = 0
        while r > 0:
            r -= ranked_population[index].probability
            index += 1
        index -= 1
        selection.append(ranked_population[index])
    return selection


def ranked(population):
    ranked_population = []
    _sum = 0
    for i in range(len(population)):
        _sum += population[i].fitness
    for i in range(len(population)):
        route = population[i]
        route.probability = route.fitness / _sum
        ranked_population.append(route)
    sorted_ranked_population = sorted(ranked_population, key=lambda p: p.fitness, reverse=True)
    return sorted_ranked_population


def next_generation(generation):
    ranked_population = ranked(generation)
    selected = roulette_wheel(ranked_population)
    children = next_population(selected)
    return_population = mutate_population(children)
    re_ranked_population = ranked(return_population)
    return re_ranked_population


def initialize_population(city_list):
    initial_population = []
    for i in range(POPULATION_SIZE):
        initial_population.append(Route(random.sample(city_list, len(city_list))))
    return initial_population


def run_ga(vectors):
    cities = [City(cords) for cords in vectors]
    pop = initialize_population(cities)
    for i in range(GENERATION_SIZE):
        pop = next_generation(pop)
        print('Current best:\t', pop[0])
        best_route = pop[0]
    print('\nGlobal best:\t', colored(best_route, 'cyan'))
