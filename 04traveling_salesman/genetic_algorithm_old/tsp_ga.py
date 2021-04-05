import random
from math import sqrt
from termcolor import colored
import sys
import copy

TOTAL_CITIES = 0
POPULATION_SIZE = 100
GENERATIONS = 25000
MUTATION_RATE = 0.30

fitness = []
population = []
best_distance = sys.maxsize
best_chromosome = None
mutation_sum = 0


def shuffle(arr):
    temp = copy.copy(arr)

    for i in range(len(temp)):
        j = random.randint(0, len(arr) - 1)
        temp[i], temp[j] = temp[j], temp[i]

    return temp


def pick_one(arr, prob):
    index = 0
    r = random.random()
    while r > 0:
        r -= prob[index]
        index += 1
    index -= 1

    return arr[index]

    # total = 0
    # slices = []
    # for i in range(POPULATION_SIZE):
    #     slices.append([arr[i], total, total + prob[i]])
    #     total += prob[i]
    # r = random()
    # return [s[0] for s in slices if s[1] < r <= s[2]][0]


def calculate_distance(points):
    distance = 0
    last_city = None

    for i in range(len(points) - 1):
        city_a = points[i]
        city_b = points[i + 1]
        d = sqrt((city_a[0] - city_b[0]) ** 2 + (city_a[1] - city_b[1]) ** 2)
        distance += d
        last_city = city_b
    distance += sqrt((last_city[0] - points[0][0]) ** 2 + (last_city[1] - points[0][1]) ** 2)

    return distance


def calculate_fitness():
    global best_chromosome, best_distance, fitness
    sum_fitness = 0
    fitness.clear()
    for i in range(len(population)):
        distance = calculate_distance(population[i])
        if distance < best_distance:
            best_distance = distance
            best_chromosome = population[i]
        assert distance > 0
        fitness.append(distance)
        sum_fitness += distance
    fitness = [f / sum_fitness for f in fitness]


def mutate(x):
    r = random.random()
    order = copy.copy(x)
    global mutation_sum
    if MUTATION_RATE - r > 0:

        mutation_sum += 1
        index_a = random.randint(0, len(order) - 1)
        index_b = random.randint(0, len(order) - 1)
        order[index_a], order[index_b] = order[index_b], order[index_a]

        # print(index_a, index_b, order)
        # print(colored(order[index_a], 'green'))
        # print(colored(order[index_b], 'green'))
        # print(colored(order, 'blue'))
    return order


def cross_over(order_a, order_b):

    # random one point crossover
    # start = randint(0, len(order_a))
    # end = randint(start, len(order_a))
    # print(start, end)
    # new_order = order_a[start:end]
    # for i in range(len(order_b)):
    #     city = order_b[i]
    #     if city not in new_order:
    #         new_order.append(city)

    # single point crossover
    new_order = order_a[:len(order_a)//2] + order_b[len(order_b)//2:]

    # two point crossover
    # part1 = order_a[:len(order_a) // 4]
    # part2 = order_b[len(order_b) // 4:len(order_b) // 2]
    # part3 = order_a[len(order_a) // 2:len(order_a) - len(order_a) // 4]
    # part4 = order_b[len(order_b) - len(order_b) // 4:]
    # new_order = part1 + part2 + part3 + part4

    # split = random.randint(0, len(order_a))
    # new_order = order_a[:split] + order_b[split:]

    # debug the child
    # print(colored(order_a, 'red'))
    # print(colored(order_b, 'red'))
    # print(colored(new_order, 'blue'))

    return new_order


def order_cross_over(order_a, order_b):
    size = len(order_a)
    alice, bob = [-1] * size, [-1] * size
    start, end = sorted([random.randrange(size) for _ in range(2)])
    alice_inherited = []
    bob_inherited = []
    for i in range(start, end + 1):
        alice[i] = order_a[i]
        bob[i] = order_b[i]
        alice_inherited.append(order_a[i])
        bob_inherited.append(order_b[i])
    current_dad_position, current_mum_position = 0, 0

    fixed_pos = list(range(start, end + 1))
    i = 0
    while i < size:
        if i in fixed_pos:
            i += 1
            continue
        test_alice = alice[i]
        if test_alice == -1:
            dad_trait = order_b[current_dad_position]
            while dad_trait in alice_inherited:
                current_dad_position += 1
                dad_trait = order_b[current_dad_position]
            alice[i] = dad_trait
            alice_inherited.append(dad_trait)

        test_bob = bob[i]
        if test_bob == -1:
            mom_trait = order_a[current_mum_position]
            while mom_trait in bob_inherited:
                current_mum_position += 1
                mom_trait = order_a[current_mum_position]
            bob[i] = mom_trait
            bob_inherited.append(mom_trait)

        i += 1

    return alice, bob


def next_generation():
    global population, POPULATION_SIZE, fitness
    new_population = []
    fitness.sort()
    while len(new_population) < POPULATION_SIZE:
        p = copy.copy(population)
        order_a = pick_one(p, fitness)
        order_b = pick_one(p, fitness)
        child = cross_over(order_a, order_b)
        child = mutate(child)
        # child1, child2 = order_cross_over(order_a, order_b)
        # child1 = mutate(child1)
        # child2 = mutate(child2)
        new_population.append(child)
        # new_population.append(child1)
        # new_population.append(child2)
    population = new_population
    POPULATION_SIZE = len(population)


def run_ga(n, locations):
    global TOTAL_CITIES, mutation_sum, MUTATION_RATE
    TOTAL_CITIES = n

    for i in range(POPULATION_SIZE):
        shuffled = shuffle(locations)
        population.append(shuffled)

    for i in range(GENERATIONS):
        calculate_fitness()
        mutation_sum = 0
        next_generation()
        print(colored('Mutation rate: ' + str(mutation_sum/POPULATION_SIZE), 'red'))
        print('Generation #' + str(i+1), '\nBest distance:', colored(round(best_distance, 2), 'green'),
              '\nPopulation size:', POPULATION_SIZE, '\nFitness size:', len(fitness))

    # population crossover debug
    # arr1 = [1, 2, 3, 4, 5]
    # arr2 = [0, 9, 8, 7, 6]
    # arr3 = [1, 1, 1, 1, 1]
    # arr4 = [2, 3, 2, 3, 2]
    # arr5 = [8, 9, 0, 8, 9]
    # arr = [arr1, arr2, arr3, arr4, arr5]
    # for i in arr:
    #     print(i)
    # print()
    # new_arr = []
    # for i in range(len(arr)):
    #     one = arr[random.randint(0, len(arr) - 1)]
    #     two = arr[random.randint(0, len(arr) - 1)]
    #
    #     print(one, two)
    #     child = cross_over(one, two)
    #     child = mutate(child)
    #     new_arr.append(child)
    # print()
    # for i in new_arr:
    #     print(i)
