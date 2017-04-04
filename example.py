import numpy as np
from featureMatrix import FeatureMatrix

fm = FeatureMatrix()

nearest_neighbor = fm.match('A', np.array([.1,.2,.3,.5]))

print(nearest_neighbor)
