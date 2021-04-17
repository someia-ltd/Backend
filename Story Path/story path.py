from sklearn.neighbors import KDTree
import pandas as pd
import numpy as np

latlong = pd.read_csv(r"story_location.csv")[["latitude", "longitude"]]

tree = KDTree(latlong)

def get_k_nearest_story(point, k):
    return(tree.query(point, k = k))

def get_story_within_radius(point, radius, sort):
    return(tree.query_radius(point, r = radius, return_distance = True, sort_results = sort))

def get_story_path(point, radius):
    idx, dist = get_story_within_radius(point, radius, sort = True)
    return(idx)

# print(get_k_nearest_story(np.array([22.381127, 114.196032]).reshape(1, -1), 10))

# print(get_story_within_radius(np.array([22.381127, 114.196032]).reshape(1, -1), 0.01, sort = False))
