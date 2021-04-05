import genetic_algorithm.tsp_ga
import ant_colony_optimization.tsp_aco


def read_file():
    with open('Assignment 3 berlin52.tsp', 'r') as file:
        vectors = []
        num_vectors = -1
        start_data = False
        for line in file.readlines():
            if line == 'EOF\n':
                break
            if line.startswith('DIMENSION:'):
                num_vectors = int(line.split(' ')[1])
            if line.startswith('1'):
                start_data = True
            if start_data:
                x = line.split(' ')[1]
                y = line.split(' ')[2]
                vectors.append((float(x), float(y)))
        return num_vectors, vectors


if __name__ == '__main__':
    data = read_file()
    num_locations = data[0]
    locations = data[1]

    genetic_algorithm.tsp_ga.run_ga(locations)
    # ant_colony_optimization.tsp_aco.run_aco(num_locations, locations)
