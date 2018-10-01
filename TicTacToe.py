import random
import numpy as np
from Player import Human, Bot, Agent
from utility import invertBoard, boardToState


class Game:
    def __init__(self, rewards, player_types=(0, 0, 2)):
        # the boarddata
        self.board = np.zeros((3, 3), dtype='int32')
        # the leftover fields
        self.fields = [i for i in range(9)]

        self.players = []
        self.initPlayers(player_types)
        # to determine who starts and which player is active
        self.active_player = random.choice([0, 1])
        self.rewards = rewards

    def initPlayers(self, player_types):
        chars = [1, -1]

        if not(0 <= np.sum(player_types) <= 2):
            raise ValueError("Can't have %i players" % np.sum(player_types))

        # init human players
        for i in range(player_types[0]):
            self.players.append(Human(input("Name of Player %i: " % (i+1)), chars[i]))

        # init random choice bots
        for i in range(player_types[1]):
            self.players.append(Bot("Bot %i" % (i+1), chars[player_types[0]+i]))

        # init qrl agents
        for i in range(player_types[2]):
            self.players.append(Agent("Agent %i" % (i+1), chars[player_types[0]+player_types[1]+i]))

    def reset(self):
        # the boarddata
        self.board = np.zeros((3, 3), dtype='int32')
        # the leftover fields
        self.fields = [i for i in range(9)]
        self.active_player = random.choice([0, 1])

    def getCurrentState(self):
        return boardToState(self.board)

    def getNextAction(self, epsilon=0):
        action = self.players[self.active_player].takeTurn(self.board, self.fields, epsilon)

        return action

    def execAction(self, action):
        self.fields.remove(action)

        row = int(action/3)
        column = action % 3
        self.board[row][column] = self.players[self.active_player].char
        self.active_player = not self.active_player

    def checkWin(self):
        rowColumnDiaSums = [0 for i in range(8)]

        #check rows
        rowColumnDiaSums[0:3] = np.sum(self.board, 1)
        #check columns
        rowColumnDiaSums[3:6] = np.sum(self.board, 0)
        #check diagonals
        rowColumnDiaSums[6] = np.sum(np.diagonal(self.board))
        rowColumnDiaSums[7] = np.sum([self.board[2][0], self.board[1][1], self.board[0][2]])

        # return 1 or -1
        for value in rowColumnDiaSums:
            if value != 0 and (value % 3) == 0:
                return int(value/3)

        # return 0 if no winner
        return 0

    def run(self, qtable={}, epsilon=0):
        steps = []

        for player in self.players:
            if type(player) == Agent:
                player.setQTable(qtable)

        while True:
            step = [None, 0, None, 0]

            step[0] = self.getCurrentState()

            action = self.getNextAction(epsilon)
            step[1] = action
            self.execAction(action)

            step[2] = self.getCurrentState()

            if self.active_player:
                steps.append(step)

            # determine the winner
            winner = self.checkWin()
            if winner != 0:
                # winner is player 0; with char 'O' or 1
                if winner == 1:
                    steps[-1][3] = self.rewards[0]
                    return steps
                # winner is player 1; with char 'X' or -1
                else:
                    steps[-1][3] = self.rewards[1]
                    return steps
            # check for draw
            if len(self.fields) == 0:
                steps[-1][3] = self.rewards[2]
                return steps

    def showcase(self, qtable):
        self.players = [None, None]
        self.players[0] = Agent("Agent 1", 1, qtable)
        self.players[1] = Human("GG", -1)


        again = 'y'
        while again == 'y':
            self.reset()
            while True:
                # display qtable value and get/execute action for active player
                state = boardToState(self.board)
                if np.sum(self.board) == 1:
                    state = boardToState(invertBoard(self.board))

                print(qtable[state][:])
                action = self.getNextAction()
                self.execAction(action)

                # check for end of game
                winner = self.checkWin()
                if winner != 0:
                    print("%i wins!" % winner)
                    break
                # check for draw
                if len(self.fields) == 0:
                    print("Draw!")
                    break

            again = input("Play again? (y/n)")
