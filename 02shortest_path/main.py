import sys
from termcolor import colored

nodes_count = 0
city_start = ''
city_finish = ''
stl = {}


class Vertex:
    def __init__(self, n):
        self.name = n
        self.neighbors = list()

    def add_neighbor(self, v, weight):
        if v not in self.neighbors:
            self.neighbors.append((v, weight))
            self.neighbors.sort()


class Graph:
    vertices = {}

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            return True
        else:
            return False

    def add_edge(self, a, b, distance=0):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].add_neighbor(b, distance)
            self.vertices[b].add_neighbor(a, distance)
            return True
        else:
            return False

    def print_graph(self):
        for key in list(self.vertices.keys()):
            print(key + str(self.vertices[key].neighbors))


def create_graph(line, graph):
    parts = line.split(' ')
    city_a = parts[0]
    city_b = parts[1]
    distance = int(parts[2])
    graph.add_vertex(Vertex(city_a))
    graph.add_vertex(Vertex(city_b))
    graph.add_edge(city_a, city_b, distance)


def create_heuristic(line):
    global stl
    parts = line.split(' ')
    if len(parts) == 2:
        stl[parts[0]] = int(parts[1])


def read_file(filename, spain):
    with open(filename, 'r') as file:
        distances = False
        straight_line_distances = False
        global city_start, city_finish
        for line in file.readlines():
            if line.startswith('Start:'):
                city_start = line.split(' ')[1].strip()
                continue
            if line.startswith('Finish: '):
                city_finish = line.split(' ')[1].strip()
                continue
            if line.startswith('COMMENT:'):
                global nodes_count
                nodes_count = int(line.split(' ')[1])
            if line == 'A B Distance\n':
                distances = True
                continue
            if distances:
                if line.startswith('Straight line Distances'):
                    straight_line_distances = True
                    distances = False
                    continue
                else:
                    if len(line.split()) == 3:
                        create_graph(line, spain)
            if straight_line_distances:
                if line == 'EOF':
                    break
                else:
                    create_heuristic(line)


def best_first_search(graph, a, b, heuristic):
    path_cost = 0
    visited = []
    city_node_a = graph.vertices[a]
    city_node_b = graph.vertices[b]
    stack = [city_node_a]

    print(city_node_a.name)
    while stack:
        current = stack.pop()
        if current not in visited:
            visited.append(current)
            neighbors = graph.vertices[current.name].neighbors
            neighbors.sort(key=lambda x: x[1])
            closest = sys.maxsize
            closest_city = ''
            for n in neighbors:
                closest = min(closest, heuristic[n[0]])
                closest_city = get_key(closest)
            for n in neighbors:
                if n[0] == closest_city:
                    print(closest_city)
                    path_cost += n[1]
                    break
            if closest_city == city_node_b.name:
                return path_cost
            stack.append(graph.vertices[closest_city])


def a_star_search(graph, a, b, heuristic):
    path_cost = 0
    visited = []
    city_node_a = graph.vertices[a]
    city_node_b = graph.vertices[b]
    stack = [city_node_a]

    print(city_node_a.name)
    while stack:
        current = stack.pop()
        if current not in visited:
            visited.append(current)
            neighbors = graph.vertices[current.name].neighbors
            neighbors.sort(key=lambda x: x[1])
            optimal = sys.maxsize
            index = -1
            for i in range(len(neighbors)):
                print(colored(neighbors[i], 'red') + ' ' + colored(heuristic[neighbors[i][0]], 'blue'))
                if path_cost + neighbors[i][1] + heuristic[neighbors[i][0]] < optimal:
                    optimal = path_cost + neighbors[i][1] + heuristic[neighbors[i][0]]
                    print('Current path cost: ' + str(path_cost) + ', Optimal: ' + str(colored(optimal, 'green')))
                    index = i
            optimal_city = neighbors[index][0]
            for n in neighbors:
                if n[0] == optimal_city:
                    print(optimal_city)
                    path_cost += n[1]
                    print(n[1])
                    break
            if optimal_city == city_node_b.name:
                return path_cost
            stack.append(graph.vertices[optimal_city])


def get_key(val):
    for key, value in stl.items():
        if val == value:
            return key

    return 'none'


if __name__ == '__main__':
    spain = Graph()
    read_file("input-spain.txt", spain)
    bfs_cost = best_first_search(spain, city_start, city_finish, stl)
    print('The path cost using Best First Search is: ' + str(bfs_cost), end='\n\n')
    a_star_cost = a_star_search(spain, city_start, city_finish, stl)
    print('The path cost using A* Search is: ' + str(a_star_cost))
