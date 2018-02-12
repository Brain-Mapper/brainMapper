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
# 16 january 2018 - Added functions for k-medoids clustering


from sklearn.cluster import KMeans, AgglomerativeClustering
import numpy as np
import random


def perform_kmeans(param_dict, X):
    kmeans = KMeans(n_clusters=int(param_dict["n_clusters"]), random_state=int(param_dict["random_state"]),
                    init=param_dict["init"],
                    n_init=int(param_dict["n_init"]), max_iter=int(param_dict["max_iter"])).fit(X)
    return kmeans.labels_


def perform_agglomerative_clustering(param_dict, X) :
    agglo_clust = AgglomerativeClustering(n_clusters=int(param_dict["n_clusters"]), affinity=param_dict["affinity"],
                                          linkage=param_dict["linkage"]).fit(X)
    return agglo_clust.labels_


# ------------------ K Medoids implementation ------------------

def kmedoids_cluster(distances, k=3):
    m = distances.shape[0]  # number of points

    # Pick k random medoids.
    curr_medoids = np.array([-1] * k)
    while not len(np.unique(curr_medoids)) == k:
        curr_medoids = np.array([random.randint(0, m - 1) for _ in range(k)])
    old_medoids = np.array([-1] * k)  # Doesn't matter what we initialize these to.
    new_medoids = np.array([-1] * k)

    # Until the medoids stop updating, do the following:
    while not ((old_medoids == curr_medoids).all()):

        # Assign each point to cluster with closest medoid.
        clusters = assign_points_to_clusters(curr_medoids, distances)

        # Update cluster medoids to be lowest cost point.
        for curr_medoid in curr_medoids:
            cluster = np.where(clusters == curr_medoid)[0]
            new_medoids[curr_medoids == curr_medoid] = compute_new_medoid(cluster, distances)

        old_medoids[:] = curr_medoids[:]
        curr_medoids[:] = new_medoids[:]

    return clusters, curr_medoids


def assign_points_to_clusters(medoids, distances):
    distances_to_medoids = distances[:, medoids]
    clusters = medoids[np.argmin(distances_to_medoids, axis=1)]
    clusters[medoids] = medoids
    return clusters


def compute_new_medoid(cluster, distances):
    mask = np.ones(distances.shape)
    mask[np.ix_(cluster, cluster)] = 0.
    cluster_distances = np.ma.masked_array(data=distances, mask=mask, fill_value=10e9)
    costs = cluster_distances.sum(axis=1)
    return costs.argmin(axis=0, fill_value=10e9)

# def compute_distances(data_matrix, distance, normalize=True)