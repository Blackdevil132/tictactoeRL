import QRL

alg = QRL.QRL(9, 19683)

alg.learn()

print(alg.test())