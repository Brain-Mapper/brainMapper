# NAME
#        clustering
#
# DESCRIPTION
#
#       The module 'clustering' contains methods for clustering on
#       nifti image collections extracted data
#
# HISTORY
#
# 6 january 2018 - Initial design and coding. (@vz-chameleon, Valentina Z.)
# 16 january 2018 - Added functions for k-medoids clustering (@vz-chameleon, Valentina Z.)
# 12 february 2018 - Finished K-Medoids and added DBSCAN (@vz-chameleon, Valentina Z.)


from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.neighbors import DistanceMetric
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


def perform_DBSCAN(param_dict, X):
    dbscan = DBSCAN(eps=float(param_dict["eps"]), min_samples=int(param_dict["min_samples"]), metric=param_dict["metric"]).fit(X)
    return dbscan.labels_


def perform_kmedoids(param_dict, X):
    distances_matrix_pairwise = compute_distances(X, param_dict['metric'])
    medoids_result = kmedoids_cluster(X, distances_matrix_pairwise, int(param_dict["n_clusters"]))
    return medoids_result[0]


# ------------------ K Medoids implementation ------------------

def compute_distances(data_matrix, distance, normalize=False):
    """
    Compute distances between data points
    :param data_matrix: The array containing the data shape=(ND x 4)
    :param distance: 'euclidean' or 'manhattan'
    :param normalize: False by default
    :return: The symmetric matrix of distances
    """

    # Euclidean or Manhattan
    dist = DistanceMetric.get_metric(distance)
    # See sklearn.neighbors.DistanceMetric documentation to see the distance matrix returned
    return dist.pairwise(data_matrix)


def kmedoids_cluster(data_matrix, distances, k=3):
    """
    Perform kmedoids clustering
    :param distances: The symmetric matrix of distances between data points
    :param k: number of clusters
    :return: array of cluster labels and latest medoids
    """
    m = distances.shape[0]  # number of points

    # Pick k random medoids and keep their indexes in data_matrix
    curr_medoids_index = np.array([-1] * k)
    while not len(np.unique(curr_medoids_index)) == k:
        curr_medoids_index = np.array([random.randint(0, m - 1) for _ in range(k)])

    curr_medoids = np.zeros(shape=(k, data_matrix.shape[1]))

    c = 0
    for index in curr_medoids_index:
        curr_medoids[c] = np.array(data_matrix[index])
        c = c+1

    old_medoids_index = np.array([-1] * k)
    new_medoids_index = np.array([-1] * k)

    while not (old_medoids_index == curr_medoids_index).all():

        # Assign each point to cluster with closest medoid.
        clusters = assign_points_to_clusters(curr_medoids_index, distances)

        # Update cluster medoids to be lowest cost point.
        for curr_medoid in curr_medoids_index:
            cluster = np.where(clusters == curr_medoid)[0]
            new_medoids_index[curr_medoids_index == curr_medoid] = compute_new_medoid(cluster, distances)

        old_medoids_index[:] = curr_medoids_index[:]
        curr_medoids_index[:] = new_medoids_index[:]

    clusters_labels = []
    c = 0
    for cluster_index in clusters:
        clust_i, = np.where(curr_medoids_index == cluster_index)
        clusters_labels.append(int(clust_i))
        c = c+1

    return clusters_labels, curr_medoids


def assign_points_to_clusters(medoids, distances):
    """
    Assign data entries to its nearest cluster based on distance to cluster's medoid
    :param medoids: An array containing the medoids of each cluster
    :param distances: The symmetric matrix of distances between data points
    :return:
    """
    distances_to_medoids = distances[:, medoids]
    clusters = medoids[np.argmin(distances_to_medoids, axis=1)]
    clusters[medoids] = medoids
    return clusters


def compute_new_medoid(cluster, distances):
    """
    Update the medoid point of each cluster after assigns
    :param cluster: The cluster of which the medoid should be updated
    :param distances: The symmetric matrix of distances between data points
    :return:
    """
    mask = np.ones(distances.shape)
    mask[np.ix_(cluster, cluster)] = 0.
    cluster_distances = np.ma.masked_array(data=distances, mask=mask, fill_value=10e9)
    costs = cluster_distances.sum(axis=1)
    return costs.argmin(axis=0, fill_value=10e9)




