# pop the first one, !isSolution? ->create children.
#               -1-1-1
#           /             \
#         -1-10          -1-11
#       /     \         /     \
#    -110     -100   -101    -111
#    /  \    / \      / \     / \
#  010  110 000 100  001 101 011 111
import time
c = 0
values = []
weights = []
max_weight = 0


def timed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        print(f'Time for {func} = {end - start}', end='\n')

        return value

    return wrapper


class Elem:
    def __init__(self, index, value, weight):
        self.index = index
        self.value = value
        self.weight = weight


def read_file(filename):
    with open(filename, 'r') as file:
        start_data = False
        global c
        for line in file.readlines():
            if line.startswith('MAXIMUM WEIGHT'):
                global max_weight
                max_weight = int(line.split(' ')[2])
            if line == 'ID b w\n':
                start_data = True
                continue
            if start_data:
                if line == 'EOF':
                    break
                else:
                    c += 1
                    parts = line.split(' ')
                    values.append(int(parts[1]))
                    weights.append(int(parts[2]))


def is_solution(node, nodes): #0 1 0
    if -1 in node:
        return -1

    total_weight = 0
    total_value = 0

    for i in range(len(node)):
        if node[i] == 1:
            total_weight += nodes[i].weight
            total_value += nodes[i].value

    if total_weight > max_weight:
        return -1

    return total_value


@timed
def run_bfs(root, nodes):
    visited = []
    stack = [root] #-1-1-1-1
    best_benefit = 0
    best_solution = []

    while stack:
        current = stack.pop()
        if current not in visited:
            visited.append(current)
            current_value = is_solution(current, nodes)

            if current_value != -1 and current_value > best_benefit:
                best_solution = current
                best_benefit = current_value

            if current_value == -1:
                try:
                    index = current.index(-1)
                    left = current.copy()
                    right = current.copy()
                    left[index] = 0
                    right[index] = 1
                    stack.insert(0, left)
                    stack.insert(0, right)
                except:
                    pass

    return best_benefit, best_solution


@timed
def run_dfs(root, nodes):
    visited = []
    stack = [root]
    best_benefit = 0
    best_solution = []

    while stack:
        current = stack.pop()
        if current not in visited:
            visited.append(current)
            current_value = is_solution(current, nodes)

            if current_value != -1 and current_value > best_benefit:
                best_solution = current
                best_benefit = current_value

            if current_value == -1:
                try:
                    index = current.index(-1)
                    left = current.copy()
                    right = current.copy()
                    left[index] = 0
                    right[index] = 1
                    stack.append(left)
                    stack.append(right)
                except:
                    pass

    return best_benefit, best_solution


def knapsack(nodes):
    root = [-1 for _ in range(c)]
    bfs = run_bfs(root, nodes)
    dfs = run_dfs(root, nodes)

    return bfs, dfs


def print_data(bfs, dfs):
    bfs_values = []
    bfs_weights = []
    dfs_values = []
    dfs_weights = []
    count = 0

    for b in bfs:
        if b == 1:
            bfs_values.append(values[count])
            bfs_weights.append(weights[count])
        else:
            bfs_values.append(0)
            bfs_weights.append(0)
        count += 1
    count = 0
    for d in dfs:
        if d == 1:
            dfs_values.append(values[count])
            dfs_weights.append(weights[count])
        else:
            dfs_values.append(0)
            dfs_weights.append(0)
        count += 1

    print('BFS Data:')
    print(bfs_weights)
    print(bfs_values)
    print('DFS Data:')
    print(dfs_weights)
    print(dfs_values)


if __name__ == '__main__':
    read_file('input.txt')
    nodes = []
    for i in range(c):
        nodes.append(Elem(i, values[i - 1], weights[i - 1]))
    solutions = knapsack(nodes)
    print(f'BFS: {solutions[0]}')
    print(f'DFS: {solutions[1]}', end="\n\n")

    print_data(solutions[0][1], solutions[1][1])
