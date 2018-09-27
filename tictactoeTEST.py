from os import system, name
from random import choice
import numpy as np
from utility import getInvertedBoard

convertSymbols = {1: 'O', -1: 'X', 0: ' '}


# self defined console clear
def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


# general horizontal win check
def checkHorizontal(board, i):
    j = 1
    if board[i] == board[i + j] and board[i] == board[i + j * 2]:
        return True
    else:
        return False


# general vertical win check
def checkVertical(board, i):
    j = 3
    if board[i] == board[i + j] and board[i] == board[i + j * 2]:
        return True
    else:
        return False


class Game:
    def __init__(self, num, qtable):
        # the boarddata
        if num:
            self.board = [str(i) for i in range(9)]
        else:
            self.board = [0 for i in range(9)]
        # the leftover fields
        self.fields = [i for i in range(9)]
        # to determine who starts and which player is active
        self.comTurn = choice([True, False])
        self.qtable = qtable

        self.initializePlayers()

    def drawBoard(self, board):
        board_str = ['' for i in range(9)]
        for i in range(9):
            board_str[i] = convertSymbols[board[i]]
        print('#' * 13)
        print('# ' + board_str[0] + ' # ' + board_str[1] + ' # ' + board_str[2] + ' #')
        print('#' * 13)
        print('# ' + board_str[3] + ' # ' + board_str[4] + ' # ' + board_str[5] + ' #')
        print('#' * 13)
        print('# ' + board_str[6] + ' # ' + board_str[7] + ' # ' + board_str[8] + ' #')
        print('#' * 13)

    def reset(self):
        if input("Play again?(y/n)") == 'y':
            self.comTurn = choice([True, False])
            self.board = [0 for i in range(9)]
            self.fields = [i for i in range(9)]
            self.run()

    def initializePlayers(self):
        inputName = input('Insert your name: ')
        self.human = Player(inputName, -1)
        self.com = Player('Computer', 1)

    def inputTurn(self, player):
        if not self.comTurn:
            table_entry = self.qtable[tuple(getInvertedBoard(self.board))][:]
            field = np.where(table_entry == np.max(table_entry))[0]
            print(table_entry)
            print(field)
            field = int(input('Choose a field: '))
            while field not in self.fields:
                field = int(input('This field does not exist or is already set. Choose another: '))
        else:
            try:
                print(self.qtable[tuple(self.board)][:])
                table_entry = self.qtable[tuple(self.board)][:]
                field = np.where(table_entry == np.max(table_entry))[0]
                print(field)
                field = choice(field)
                if field not in self.fields:
                    field = choice(self.fields)
            except KeyError:
                field = choice(self.fields)
        self.fields.remove(field)
        self.board[field] = player.char
        self.comTurn = not self.comTurn

    def checkWin(self):
        win = 0
        for i in range(len(self.board)):

            # checks for field 1
            if i == 0:
                if checkHorizontal(self.board, i):
                    win = self.determineWinner(i)
                elif checkVertical(self.board, i):
                    win = self.determineWinner(i)
                # check diagonal
                elif self.board[i] == self.board[i + 4] and self.board[i] == self.board[i + 8]:
                    win = self.determineWinner(i)

            # checks for field 2
            elif i == 1:
                if checkVertical(self.board, i):
                    win = self.determineWinner(i)

            # checks for field 3
            elif i == 2:
                if checkVertical(self.board, i):
                    win = self.determineWinner(i)
                # check diagonal
                elif self.board[i] == self.board[i + 2] and self.board[i] == self.board[i + 4]:
                    win = self.determineWinner(i)

            # checks for field 4
            elif i == 3:
                if checkHorizontal(self.board, i):
                    win = self.determineWinner(i)

            # checks for field 7
            elif i == 6:
                if checkHorizontal(self.board, i):
                    win = self.determineWinner(i)

        return win

    def determineWinner(self, i):
        if self.board[i] == self.human.char:
            return self.human
        elif self.board[i] == self.com.char:
            return self.com
        else:
            return 0

    def run(self):
        # clear()
        # the game loop
        while True:
            clear()
            self.drawBoard(self.board)
            if not self.comTurn:
                self.inputTurn(self.human)
            else:
                self.inputTurn(self.com)
            winner = self.checkWin()
            # determine the winner
            if winner == self.human:
                # clear()
                self.drawBoard(self.board)
                print(self.human.name + ' has won the game!')
                break
            elif winner == self.com:
                # clear()
                self.drawBoard(self.board)
                print(self.com.name + ' has won the game!')
                break
            # check for draw
            if len(self.fields) == 0:
                # clear()
                self.drawBoard(self.board)
                print('The game is a draw!')
                break

        self.reset()


class Player:
    def __init__(self, inputName, inputChar):
        self.name = inputName
        self.char = inputChar
