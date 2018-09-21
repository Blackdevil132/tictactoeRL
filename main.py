import sys
import QRL

if len(sys.argv) < 5:
	print("Usage: "+sys.argv[0]+" total_runs learning_rate discount_rate decay_rate")
	exit(0)

alg = QRL.QRL(int(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]))

alg.learn()

print(alg.test())