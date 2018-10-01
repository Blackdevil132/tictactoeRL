import sys
import QRL

if len(sys.argv) < 5:
    print("Usage: " + sys.argv[0] + " total_runs learning_rate discount_rate decay_rate")
    exit(0)

qrl = QRL.QRL(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), (9, 19683))

qrl.run()

print()
print(qrl.qtable[(0, 0, 0, 0, 0, 0, 0, 0, 0)])

wins, losses, remis = qrl.getWLRs()
print("Won: %s" % wins)
print("Draw: %s" % remis)
print("Lost: %s" % losses)

