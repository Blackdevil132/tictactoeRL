import sys
import QRL
import pickle
import tictactoeTEST

if len(sys.argv) < 5:
    print("Usage: " + sys.argv[0] + " total_runs learning_rate discount_rate decay_rate")
    exit(0)

alg = QRL.QRL(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]))

alg.learn()
alg.saveToFile()

print()
print(alg.qtable[(' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ')])

wins, draws, losses = alg.test()
lossrate = losses / 1000 * 100
winrate = wins / 1000 * 100
print("Won: %s" % wins)
print("Draw: %s" % draws)
print("Lost: %s" % losses)
print("Losing Rate: %.2f%%" % lossrate)
print("Win Rate: %.2f%%" % winrate)

for i in range(10):
    game_test = tictactoeTEST.Game(False, alg.qtable)
    game_test.run()



def loadFromFile(path):
    with open(path + '.pkl', 'rb') as f:
        return pickle.load(f)
