from math import sqrt, pow
from random import randint, random
import sys
from termcolor import colored

CITY_COUNT = 0
RANDOM_CITY_FACTOR = 0.1
ALPHA = 4
BETA = 7
ANTS_FACTOR = 0.5
TOTAL_TRIPS = 100
EVAPORATION_RATE = 0.4

distances = [[]]


class Ant:

    def __init__(self):
        self.visited_cities = []
        self.visited_cities.append(randint(0, CITY_COUNT - 1))
        self.all_cities = set(range(0, CITY_COUNT))

    def visit_city(self, pheromones):
        if random() < RANDOM_CITY_FACTOR:
            self.visited_cities.append(self.visit_random_city())
        else:
            self.visited_cities.append(
                self.roulette_wheel(self.visit_probabilistic_city(pheromones)))

    def visit_random_city(self):
        possible_cities = self.all_cities - set(self.visited_cities)

        return randint(0, len(possible_cities) - 1)

    def visit_probabilistic_city(self, pheromones):
        current = self.visited_cities[-1]
        possible_cities = self.all_cities - set(self.visited_cities)
        possible_indexes = []
        possible_probabilities = []
        total_probabilities = 0
        for city in possible_cities:
            possible_indexes.append(city)
            pheromones_on_path = pow(pheromones[current][city], ALPHA)
            heuristics_on_path = pow(1 / distances[current][city], BETA)
            probability = pheromones_on_path * heuristics_on_path
            possible_probabilities.append(probability)
            total_probabilities += probability
        possible_probabilities = [probability / total_probabilities for probability in possible_probabilities]

        return [possible_indexes, possible_probabilities, len(possible_cities)]

    @staticmethod
    def roulette_wheel(data):
        total = 0
        slices = []
        indexes = data[0]
        probabilities = data[1]
        city_count = data[2]
        for i in range(0, city_count):
            slices.append([indexes[i], total, total + probabilities[i]])
            total += probabilities[i]
        r = random()
        return [s[0] for s in slices if s[1] < r <= s[2]][0]

    def get_distance(self):
        total = 0
        for city in range(len(self.visited_cities) - 1):
            total += distances[self.visited_cities[city]][self.visited_cities[city + 1]]
        total += distances[self.visited_cities[len(self.visited_cities) - 1]][self.visited_cities[0]]

        return total

    def print_ant(self):
        print('I am ant ', self.__hash__())
        print('Number of visited cities: ', len(self.visited_cities))
        print('My path distance is: ', self.get_distance())


class ACO:

    def __init__(self, factor):
        self.ants_factor = factor
        self.ant_colony = []
        self.pheromones = []
        self.best_solution = sys.maxsize
        self.best_ant = None

    def init_ants(self, factor):
        ants_no = round(CITY_COUNT * factor)
        self.ant_colony.clear()
        for i in range(ants_no):
            self.ant_colony.append(Ant())

    def init_pheromones(self):
        for i in range(len(distances)):
            pheromones_list = []
            for j in range(len(distances)):
                pheromones_list.append(1)
            self.pheromones.append(pheromones_list)

    def move_ants(self, population):
        for ant in population:
            ant.visit_city(self.pheromones)

    def get_best(self, population):
        for ant in population:
            distance = ant.get_distance()
            if distance < self.best_solution:
                self.best_solution = distance
                self.best_ant = ant

        return self.best_ant

    def update_pheromones(self, evaporation_rate):
        for i in range(CITY_COUNT):
            for j in range(CITY_COUNT):
                self.pheromones[i][j] = self.pheromones[i][j] * evaporation_rate
                for ant in self.ant_colony:
                    if i in ant.visited_cities and j in ant.visited_cities:
                        self.pheromones[i][j] += 1 / ant.get_distance()

    def solve(self, trips, evaporation_rate):
        self.init_pheromones()
        for i in range(trips):
            self.init_ants(ANTS_FACTOR)
            for j in range(CITY_COUNT - 1):
                self.move_ants(self.ant_colony)
            self.update_pheromones(evaporation_rate)
            self.best_ant = self.get_best(self.ant_colony)
            print('Trip #' + str(i) + ' Best distance: ', colored(round(self.best_ant.get_distance(), 2), 'blue'))


def run_aco(n, locations):
    global CITY_COUNT, distances
    CITY_COUNT = n

    for i in range(CITY_COUNT):
        distances.append([])
        for j in range(CITY_COUNT):
            if i == j:
                distances[i].append(0)
            else:
                distances[i]\
                    .append(sqrt((locations[i][0] - locations[j][0]) ** 2 + (locations[i][1] - locations[j][1]) ** 2))
    aco = ACO(ANTS_FACTOR)
    aco.solve(TOTAL_TRIPS, EVAPORATION_RATE)
