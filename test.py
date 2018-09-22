from tictactoeTEST import Game
from utility import loadFromFile

qtable = loadFromFile("qtable.pkl")

game_test = Game(False, qtable)
game_test.run()
