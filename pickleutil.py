import pickle


def dump_pickle(obj, file):
    with open(file, "wb") as fp:
        pickle.dump(obj, file=fp)


def load_pickle(file):
    with open(file, "rb") as fp:
        return pickle.load(fp)
