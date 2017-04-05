import numpy as np
from scipy.spatial import distance, distance_matrix

class FeatureMatrix(object):
    """docstring for FeatureMatrix"""
    def __init__(self):
        super(FeatureMatrix, self).__init__()
        self.matrix = self._load_matrix()
        self.user_list = self._load_list()


    def _load_matrix(self):
        placeholder = np.array([[0.2, 0.1, 0.9, 0.5],\
                                [0.9, 0.3, 0.8, 0.2],\
                                [0.7, 0.6, 0.3, 0.2]])
        return placeholder


    # TODO: Better data structure
    def _load_list(self):
        placeholder = np.array(['A', 'B', 'C'])
        return placeholder


    # Update matrix and return neighbors as list
    def match(self, user, vector):

        user_index = np.where(self.user_list == user)

        self.updateVector(user_index, vector)
        neighbors = self._findNeighbors(user_index)

        return neighbors


    # Update user vector in matrix
    # TODO Catch for new user, add new user
    def updateVector(self, user_index, vector):
        self.matrix[user_index] = vector


    # Calcualte distance between users, return closest
    # TODO Return list of nearest neighbors, not single neighbor
    def _findNeighbors(self, user_index):
        all_neighbors = distance.pdist(self.matrix, 'euclidean')
        d_matrix = distance_matrix(self.matrix, self.matrix)[user_index]
        d_matrix = d_matrix.tolist()[0]

        _min = min(i for i in d_matrix if i > 0)
        neighbor = d_matrix.index(_min)

        return self.user_list[neighbor]
