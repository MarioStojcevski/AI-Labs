import socket
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os
import math
import copy


class Mancala():

    def __init__(self, player_turn, board):
        self.board = board
        self.player = player_turn
        self.free_move = False
        

    def minimax(game, depth, alpha, beta):
    # If the game is finished or you reached your depth, do the evaluation.
    if game.is_over() or depth == 0:
        return game.utility(game)

    # MAX
    if game.player == 1:
        _max = -math.inf
        allowed_moves = game.get_all_moves()

        # For move in allowed_moves, do the move and see what happens with the game, 
        # then call minimax again until you evaluate
        for m in allowed_moves:
            new_game = copy.copy(game)
            new_game.make_move(m)

            evaluate = minimax(new_game, depth-1, alpha, beta)
            _max = max(_max, evaluate)
            alpha = max(alpha, evaluate)

            if beta  <= alpha:
                break
        return _max

    # MIN
    else:
        _min = math.inf
        allowed_moves = game.get_all_moves()

        # For move in allowed_moves, do the move and see what happens with the game, 
        # then call minimax again until you evaluate
        for m in allowed_moves:
            new_board = copy.copy(game)
            new_board.make_move(m)

            evaluate = minimax(new_board, depth-1, alpha, beta)
            _min = min(_min, evaluate)
            beta = min(beta, evaluate)

            if alpha <= beta:
                break
        return _min


    def make_move(self, hole):
        self.free_move = False

        if self.player == 1:
            change_player = True
            # Take the stones from the hole
            stones = self.board[hole]
            self.board[hole] = 0
            # Start putting stones in the hole after the one from which you pick the stones
            index = hole + 1

            while stones > 0:
                # If you have one stone you can see if you get a free turn or take the opposite hole.
                if stones == 1:

                    # If the index to put is your hole, you get a free turn
                    if index == 6:
                        self.board[6] += 1
                        self.player = 1
                        change_player = False
                        self.free_move = True
                        break
                    # Add other players stones from opposite hole
                    if self.board[index] == 0 and index in range(6):
                        self.board[6] += 1
                        opposite_hole = self.find_opposite_hole(index)
                        self.board[6] += self.board[opposite_hole[1]]
                        self.board[opposite_hole[1]] = 0
                        break

                # If you end up at the other player's hole
                if index == 13:
                    index = 0
                else:
                    stones -= 1
                    self.board[index] += 1
                    index += 1
            if change_player:
                self.player = 2

        else:
            change_player = True
            # Take the stones from the hole
            stones = self.board[hole]
            self.board[hole] = 0
            # Start putting stones in the hole after the one from which you pick the stones
            index = hole + 1

            while stones > 0:
                # If you have one stone you can see if you get a free turn or take the opposite hole.
                if stones == 1:

                    # If the index to put is your hole, you get a free turn
                    if index == 13:
                        self.board[13] += 1
                        self.player = 1
                        change_player = False
                        self.free_move = True
                        break
                    # Add other players stones from opposite hole
                    if self.board[index] == 0 and index in range(7,13):
                        self.board[13] += 1
                        opposite_hole = self.find_opposite_hole(index)
                        self.board[13] += self.board[opposite_hole[0]]
                        self.board[opposite_hole[0]] = 0
                        break

                # If you end up at the other player's hole
                if index == 6:
                    index = 7
                else:
                    stones -= 1
                    self.board[index] += 1
                    index += 1
            if change_player:
                self.player = 1


    def find_opposite_hole(self, hole):
        pair = (-1, -1)

        if  hole == 0 or hole == 12:
            pair = (0, 12)
        elif hole == 1 or hole == 11:
            pair = (1, 11)
        elif hole == 2 or hole == 10:
            pair = (2, 10)
        elif hole == 3 or hole == 9:
            pair = (3, 9)
        elif hole == 4 or hole == 8:
            pair = (4, 8)
        elif hole == 5 or hole == 7:
            pair = (5, 7)

        return pair


    # Utility function
    def utility(self, state):
        other_players_stones = 0
        for i in range(7,13):
            other_players_stones += state.board[i]
        other_players_stones += state.board[13] * 1.5

        return other_players_stones + 5 if state.free_move else other_players_stones


    def get_all_moves(self):
        return [i for i in range(6) if self.board[i] != 0] if self.player==1 else [i for i in range(7,13) if self.board[i] != 0]


    def is_over(self):
        game_over = True

        # If player one, check to see if the state of the game is over
        for i in range(6):
            if self.board[i] == 0:
                game_over = False
                break

        # If it's not over for player one, check if player two has empty state
        if not game_over: 
            for i in range(7, 13):
                if self.board[i] != 0:
                    return False

            return True 
        else:   # the game is finished
            return True


def find_best_move(game):
    allowed_moves = game.get_all_moves()
    max_value = -math.inf
    best_move = '-1'

    for m in allowed_moves:
        new_game = copy.copy(game)
        new_game.make_move(m)
        value = minimax(new_state, 3, -math.inf, math.inf)

        if value > max_value:
            max_value = value
            best_move = m

    best_move = (best_move+1) % 7
    return best_move


def receive(socket):
    msg = ''.encode()  # type: str

    try:
        data = socket.recv(1024)  # type: object
        msg += data
    except:
        pass
    return msg.decode()


def send(socket, msg):
    socket.sendall(msg.encode())


if __name__ == "__main__":

    # VARIABLES
    playerName = 'mario stojcevski'
    host = '127.0.0.1'
    port = 30000  # Reserve a port for your service.
    s = socket.socket()  # Create a socket object
    pool = ThreadPool(processes=1)
    gameEnd = False
    MAX_RESPONSE_TIME = 5

    print('The player: ' + playerName + ' starts!')
    s.connect((host, port))
    print('The player: ' + playerName + ' connected!')

    while not gameEnd:
        asyncResult = pool.apply_async(receive, (s,))
        startTime = time.time()
        currentTime = 0
        received = 0
        data = []
        while received == 0 and currentTime < MAX_RESPONSE_TIME:
            if asyncResult.ready():
                data = asyncResult.get()
                received = 1
            currentTime = time.time() - startTime

        if received == 0:
            print('No response in ' + str(MAX_RESPONSE_TIME) + ' sec')
            gameEnd = 1

        if data == 'N':
            send(s, playerName)

        if data == 'E':
            gameEnd = 1

        if len(data) > 1:
            # Read the board and player turn
            board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            player_turn = int(data[0])
            i = 0
            j = 1
            while i <= 13:
                board[i] = int(data[j]) * 10 + int(data[j + 1])
                i += 1
                j += 2
            # Using your intelligent bot, assign a move to "move"
            # example: move = '1';  Possible moves from '1' to '6' if the game's rules allows those moves.
            # TODO: Change this
            ################

            game = Mancala(player_turn, board)
            move = find_best_move(game)

            ################
            send(s, str(move))
