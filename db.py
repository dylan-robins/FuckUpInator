from os import path
import pickle


class db:
    def __init__(self, path):
        self.save_path = path
        self.data = self.load()
    
    def get_user_fu(self, id):
        if id in self.data.keys():
            return self.data[id]
        else:
            raise KeyError

    def set_user_fu(self, id, time):
        self.data[id] = time
    
    def save(self):
        with open(self.save_path, "wb") as ofile:
            pickle.dump(self.data, ofile)

    def load(self):
        if path.exists(self.save_path):
            with open(self.save_path, "rb") as ifile:
                return pickle.load(ifile)
        else:
            return {}