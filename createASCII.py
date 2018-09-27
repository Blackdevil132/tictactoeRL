import pickle

def loadFromFile(path):
    with open(path + '.pkl', 'rb') as f:
        return pickle.load(f)

qtable = loadFromFile("qtable")
chart = open("qtableASCII.txt","w")

for board,values in qtable.items():
    board = [str(integer) for integer in board]
    chart.write("#" * 13 + "\t" * 2 + "#" * 25 + "\n")
    chart.write("# " + board[0] + " # " + board[1] + " # " + board[2] + " #" + "\t" * 2 + "| %.2f | %.2f | %.2f |\n" %(values[0],values[1],values[2]))
    chart.write("#" * 13 + "\t" * 2 + "#" * 25 + "\n")
    chart.write("# " + board[3] + " # " + board[4] + " # " + board[5] + " #" + "\t" * 2 + "| %.2f | %.2f | %.2f |\n" %(values[3],values[4],values[5]))
    chart.write("#" * 13 + "\t" * 2 + "#" * 25 + "\n")
    chart.write("# " + board[6] + " # " + board[7] + " # " + board[8] + " #" + "\t" * 2 + "| %.2f | %.2f | %.2f |\n" %(values[6],values[7],values[8]))
    chart.write("#" * 13 + "\t" * 2 + "#" * 25 + "\n")
    chart.write("\n")
    chart.write("\n")

chart.close()