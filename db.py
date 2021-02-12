from os import path
import pickle


class db:
    def __init__(self, path):
        print("initializing database")
        self.save_path = path

    def get_user_fu(self, id):
        self.load()
        if id in self.data.keys():
            return self.data[id]
        else:
            raise KeyError

    def set_user_fu(self, id, time):
        self.data[id] = time
        self.save()

    def save(self):
        print("Saving database to file")
        with open(self.save_path, "wb") as ofile:
            pickle.dump(self.data, ofile)

    def load(self):
        if path.exists(self.save_path):
            print("Loading database from file")
            with open(self.save_path, "rb") as ifile:
                return pickle.load(ifile)
        else:
            print("Creating new empty database in memory")
            return {}

    def dump(self):
        for id in self.data.keys():
            yield (id, self.data[id])
