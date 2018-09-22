import pickle

def loadFromFile(path):
    with open(path + '.pkl', 'rb') as f:
        return pickle.load(f)