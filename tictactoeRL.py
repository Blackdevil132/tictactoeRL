import random
import numpy as np


def drawBoard(board):
    print('#' * 13)
    print('# ' + board[0] + ' # ' + board[1] + ' # ' + board[2] + ' #')
    print('#' * 13)
    print('# ' + board[3] + ' # ' + board[4] + ' # ' + board[5] + ' #')
    print('#' * 13)
    print('# ' + board[6] + ' # ' + board[7] + ' # ' + board[8] + ' #')
    print('#' * 13)


class Game:
    def __init__(self, rewards):
        # the boarddata
        self.board = [' ' for i in range(9)]
        # the leftover fields
        self.fields = [i for i in range(9)]
        self.players = [Player("Bot 1", 'O'), Player('Bot 2', 'X')]
        # to determine who starts and which player is active
        self.activePlayer = random.choice([True, False])
        self.rewards = rewards

    def reset(self):
        # the boarddata
        self.board = [' ' for i in range(9)]
        # the leftover fields
        self.fields = [i for i in range(9)]
        self.activePlayer = random.choice([True, False])
        return self.board

    def inputTurn(self, qtable, epsilon):
        if self.activePlayer == 0:
            exp_exp_tradeoff = random.uniform(0, 1)

            if exp_exp_tradeoff > epsilon:
                try:
                    action = np.argmax(qtable[tuple(self.board)][:])
                    if action not in self.fields:
                        action = random.choice(self.fields)
                except KeyError:
                    action = random.choice(self.fields)

            else:
                action = random.choice(self.fields)
        else:
            action = random.choice(self.fields)

        self.fields.remove(action)
        self.board[action] = self.players[self.activePlayer].char
        self.activePlayer = not self.activePlayer
        return action

    # general horizontal win check
    def checkHorizontal(self, i):
        j = 1
        return self.board[i] == self.board[i + j] and self.board[i] == self.board[i + j * 2]

    # general vertical win check
    def checkVertical(self, i):
        j = 3
        return self.board[i] == self.board[i + j] and self.board[i] == self.board[i + j * 2]

    def checkWin(self):
        win = -1
        for i in range(len(self.board)):

            # checks for field 1
            if i == 0:
                if self.checkHorizontal(i):
                    win = self.determineWinner(i)
                elif self.checkVertical(i):
                    win = self.determineWinner(i)
                # check diagonal
                elif self.board[i] == self.board[i + 4] and self.board[i] == self.board[i + 8]:
                    win = self.determineWinner(i)

            # checks for field 2
            elif i == 1:
                if self.checkVertical(i):
                    win = self.determineWinner(i)

            # checks for field 3
            elif i == 2:
                if self.checkVertical(i):
                    win = self.determineWinner(i)
                # check diagonal
                elif self.board[i] == self.board[i + 2] and self.board[i] == self.board[i + 4]:
                    win = self.determineWinner(i)

            # checks for field 4
            elif i == 3:
                if self.checkHorizontal(i):
                    win = self.determineWinner(i)

            # checks for field 7
            elif i == 6:
                if self.checkHorizontal(i):
                    win = self.determineWinner(i)

        return win

    def determineWinner(self, i):
        if self.board[i] == self.players[0].char:
            return 0
        elif self.board[i] == self.players[1].char:
            return 1
        else:
            return -2

    def run(self, qtable, epsilon):
        steps = []
        while True:
            step = [None, 0, None, 0]
            step[0] = tuple(self.board)
            action = self.inputTurn(qtable, epsilon)
            step[1] = action
            step[2] = tuple(self.board)
            winner = self.checkWin()

            if self.activePlayer:
                steps.append(step)

            # determine the winner
            if winner >= 0:
                if winner == 0:
                    steps[-1][3] = self.rewards[0]
                    return steps
                else:
                    steps[-1][3] = self.rewards[1]
                    return steps
            # check for draw
            if len(self.fields) == 0:
                steps[-1][3] = self.rewards[2]
                return steps


class Player:
    def __init__(self, inputName, inputChar):
        self.name = inputName
        self.char = inputChar


#game = Game()
#print(game.run({}, 0.5))
#drawBoard(game.board)
