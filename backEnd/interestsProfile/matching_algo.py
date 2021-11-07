import faiss
import numpy as np
from hackathon_project_backend.settings import PKL_PATH
# PKL_PATH = ''
import os


# Words represent dimensions
# Magnitude is represented by weights correlated to words
# Each vector is a user

class MatchingAlgo:
    def __init__(self, number_of_categories):
        self.index = faiss.IndexFlatL2(number_of_categories)

    def length(self):
        # print(self.index.ntotal)
        return self.index.ntotal

    def add_vector(self, user_weights):
        user_weights = np.array([user_weights]).astype('float32')
        return self.index.add(user_weights)

    def k_nearest_neighbours(self, k, user_weight):
        user_weight = np.array([user_weight]).astype('float32')
        D, I = self.index.search(user_weight, k)
        I = [e for e in I[0].tolist() if e != -1]
        return I

    def serialize_index(self, path=PKL_PATH):
        faiss.write_index(self.index, path)

    def deserialize_index(self, path=PKL_PATH):
        if os.path.exists(path):
            self.index = faiss.read_index(path)

    def add_vector_workflow(self, user_weights, path=PKL_PATH):
        self.deserialize_index()
        self.add_vector(user_weights)
        self.serialize_index()


if __name__ == '__main__':
    algo = MatchingAlgo(2)
    user_weights1 = [1, 3]
    user_weights2 = [0, 0]
    user_weights3 = [100, 200]
    algo.add_vector(user_weights1)
    algo.add_vector(user_weights3)
    algo.add_vector(user_weights2)
    algo.serialize_index('temp_index.pkl')
    algo.index = None
    algo.deserialize_index('temp_index.pkl')
    print()
