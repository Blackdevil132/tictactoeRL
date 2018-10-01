import TicTacToe
from utility import loadFromFile

qtable = loadFromFile("qtable")

game = TicTacToe.Game((10, -10, 5))
game.showcase(qtable)
