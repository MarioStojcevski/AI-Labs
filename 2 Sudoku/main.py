from time import time


def read_sudokus():
    with open('sudoku.txt', 'r') as file:
        data_flag = False
        sudokus = []
        board = []
        for line in file.readlines():
            if line.startswith('SUDOKU'):
                data_flag = True
                continue
            if line == 'EOF\n' or line == '\n':
                if len(board):
                    sudokus.append(board)
                board = []
                data_flag = False
            if data_flag:
                nums = list(map(int, line[:9]))
                board.append(nums)

        return sudokus


def to_string(sudoku):
    for i in range(9):
        if i % 3 == 0:
            print('  =============================')
        for j in range(9):
            if j % 3 == 0:
                print(' || ', end='')
            if j == 8:
                print(str(sudoku[i][j]) + ' || ')
            else:
                print(str(sudoku[i][j]) + ' ', end='')
    print('  =============================')


def find_next(sudoku):
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] == 0:
                return i, j


def is_solution(sudoku, num, pos):
    for i in range(9):
        if sudoku[pos[0]][i] == num:
            return False

    for i in range(9):
        if sudoku[i][pos[1]] == num:
            return False

    small_j = int(pos[1] / 3) * 3               #
    small_i = int(pos[0] / 3) * 3
    for i in range(small_i, small_i + 3):
        for j in range(small_j, small_j + 3):
            if sudoku[i][j] == num:
                return False

    return True


def backtrack(sudoku):
    next_empty = find_next(sudoku)
    if not next_empty:
        return True
    else:
        row, col = next_empty

    for i in range(1, 10):
        if is_solution(sudoku, i, (row, col)):
            sudoku[row][col] = i

            if backtrack(sudoku):
                return True
            sudoku[row][col] = 0
    return False


if __name__ == '__main__':
    boards = read_sudokus()
    start = time()
    for b in boards:
        ind = str(boards.index(b)+1)
        print(f'Printing sudoku board #{ind}')
        to_string(b)
        ts = time()
        backtrack(b)
        te = time()
        print(f'Solved sudoku board #{ind} for {round(te-ts, 4)}')
        to_string(b)
        print()
    end = time()
    print(f'Full time for 10 boards is: {round(end-start, 2)}')
