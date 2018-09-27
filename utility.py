import pickle

def loadFromFile(path):
    with open(path + '.pkl', 'rb') as f:
        return pickle.load(f)


def getInvertedBoard(board):
    new_board = []
    for i in range(9):
        new_board.append(board[i] * -1)

    return new_board
