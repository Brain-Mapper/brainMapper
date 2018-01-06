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


def performKmeans(k,X):
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
    return kmeans.labels_
