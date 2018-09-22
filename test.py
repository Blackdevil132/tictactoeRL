from tictactoeTEST import Game
from utility import loadFromFile

qtable = loadFromFile("qtable")

game_test = Game(False, qtable)
game_test.run()
