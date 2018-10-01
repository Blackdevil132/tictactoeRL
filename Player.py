import random
import numpy as np
from utility import drawBoard, invertBoard, boardToState


class Player:
    def __init__(self, name, input_char):
        self.name = name
        self.char = input_char

    def takeTurn(self, board, options, epsilon):
        return None


class Human(Player):
    def __init__(self, name, input_char):
        Player.__init__(self, name, input_char)

    def takeTurn(self, board, options, epsilon=0):
        drawBoard(board)
        action = int(input('Choose a field: '))
        while action not in options:
            action = int(input('This field does not exist or is already set. Choose another: '))

        return action


class Agent(Player):
    def __init__(self, name, input_char, qtable=None):
        Player.__init__(self, name, input_char)
        self.qtable = qtable

    def takeTurn(self, board, options, epsilon):
        exp_exp_tradeoff = random.uniform(0, 1)

        if exp_exp_tradeoff > epsilon:
            # exploit
            try:
                if self.char == -1:
                    board = invertBoard(board)

                state = boardToState(board)
                possible_actions = self.qtable[state][:]
                actions = np.where(possible_actions == np.max(possible_actions))[0]
                action = random.choice(actions)
                # take random action, if no action can lead to draw/victory
                if action not in options:
                    action = random.choice(options)
            # take random action, if qtable has no values yet
            except KeyError:
                action = random.choice(options)

        else:
            # explore
            action = random.choice(options)

        return action

    def setQTable(self, qtable):
        self.qtable = qtable


class Bot(Player):
    def __init__(self, name, input_char):
        Player.__init__(self, name, input_char)

    def takeTurn(self, board, options, epsilon=0):
        action = random.choice(options)

        return action
