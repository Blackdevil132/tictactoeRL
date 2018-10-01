import pickle

import numpy as np

convertToSymbol = {1: 'O', 0: ' ', -1: 'X'}


def drawBoard(board):
    boardPP = []
    for row in board:
        for field in row:
            boardPP.append(convertToSymbol[field])

    s = '#' * 13 + '\n'
    s += '# %s # %s # %s #\n' % tuple(boardPP[0:3])
    s += '#' * 13 + '\n'
    s += '# %s # %s # %s #\n' % tuple(boardPP[3:6])
    s += '#' * 13 + '\n'
    s += '# %s # %s # %s #\n' % tuple(boardPP[6:9])
    s += '#' * 13 + '\n'

    print(s)
    return s


def invertBoard(board):
    invBoard = board.copy()
    invBoard *= -1

    return invBoard


def boardToState(board):
    state = tuple(board.flatten())
    return state


def checkWin(board):
    rowColumnDiaSums = [0 for i in range(8)]

    #check rows
    rowColumnDiaSums[0:3] = np.sum(board, 1)
    #check columns
    rowColumnDiaSums[3:6] = np.sum(board, 0)
    #check diagonals
    rowColumnDiaSums[6] = np.sum(np.diagonal(board))
    rowColumnDiaSums[7] = np.sum([board[2][0], board[1][1], board[0][2]])

    # return 1 or -1
    for value in rowColumnDiaSums:
        if value != 0 and (value % 3) == 0:
            return int(value/3)

    # return 0 if no winner
    return 0


def loadFromFile(path):
    with open(path + '.pkl', 'rb') as f:
        return pickle.load(f)
