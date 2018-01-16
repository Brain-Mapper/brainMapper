# NAME
#        calculations
#
# DESCRIPTION
#
#       The module 'calculations' contains methods for mathematical or preprocessing operations on
#       nifti image collections, sets or single files
#
# HISTORY
#
# 6 january 2018 - Initial design and coding. (@vz-chameleon, Valentina Z.)


from sklearn.cluster import KMeans
import numpy as np


def perform_kmeans(param_dict, X):
    kmeans = KMeans(n_clusters=int(param_dict["n_clusters"]), random_state=int(param_dict["random_state"]),
                    init=param_dict["init"],
                    n_init=int(param_dict["n_init"]), max_iter=int(param_dict["max_iter"])).fit(X)
    return kmeans.labels_
