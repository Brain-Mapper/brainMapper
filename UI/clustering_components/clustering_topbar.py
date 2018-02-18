# NAME
#
#        clusteringView
#
# DESCRIPTION
#
#       'clusteringView' contains the Qwidget for the clustering view
#
# HISTORY
#
# 2 january 2018 - Initial design and coding. (@vz-chameleon, Valentina Z.)
# 15 january 2018 - Creating a Clustering Method chooser (@vz-chameleon, Valentina Z.)

from PyQt4 import QtGui
from PyQt4.Qt import pyqtSignal

from BrainMapper import *


class ClusteringChooser(QtGui.QToolButton):
    """
    A Custom QToolButton to select and launch loading of available clustering methods
    """
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to communicate between the widgets ClusteringParameters and ScriptEnv, that will be stacked in
    # an instance of ParameterAndScriptStack (see clustering_paramspace file)

    showClustParamsWidget = pyqtSignal()
    showScriptEnvWidget = pyqtSignal()

    # CONSTRUCTOR
    def __init__(self):
        super(ClusteringChooser, self).__init__()

        self.currently_selected = None
        self.setText("Choose a clustering algorithm")
        self.setStyleSheet("width: 250px; background-color: #fefee1;")
        self.setPopupMode(QtGui.QToolButton.MenuButtonPopup)

        self.clustering_algo_menu = QtGui.QMenu()

        Kmeans_choice = QtGui.QAction('KMeans', self)
        Kmeans_choice.setStatusTip('Apply KMeans algorithm to dataset')
        Kmeans_choice.triggered.connect(lambda: self.updateLabel("KMeans", self.showClustParamsWidget))

        Kmedoids_choice = QtGui.QAction('&KMedoids', self)
        Kmedoids_choice.setStatusTip('Apply KMedoids algorithm to dataset')
        Kmedoids_choice.triggered.connect(
            lambda: self.updateLabel("KMedoids", self.showClustParamsWidget))

        Agglomerative_choice = QtGui.QAction('&AgglomerativeClustering', self)
        Agglomerative_choice.setStatusTip('Apply Agglomerative Clustering algorithm to dataset')
        Agglomerative_choice.triggered.connect(lambda: self.updateLabel("AgglomerativeClustering", self.showClustParamsWidget))

        # I have some problems with DBSCAN

        # DBSCAN_choice = QtGui.QAction('&DBSCAN', self)
        # DBSCAN_choice.setStatusTip('Apply DBSCAN algorithm to dataset')
        # DBSCAN_choice.triggered.connect(
        #     lambda: self.updateLabel("DBSCAN", self.showClustParamsWidget))

        user_script_choice = QtGui.QAction('&Custom user script', self)
        user_script_choice.setStatusTip('Make a custom clustering script')
        user_script_choice.triggered.connect(lambda: self.updateLabel("Custom user script", self.showScriptEnvWidget))

        self.clustering_algo_menu.addAction(Kmeans_choice)
        self.clustering_algo_menu.addAction(Kmedoids_choice)
        self.clustering_algo_menu.addAction(Agglomerative_choice)
        # self.clustering_algo_menu.addAction(DBSCAN_choice)
        self.clustering_algo_menu.addAction(user_script_choice)

        self.setMenu(self.clustering_algo_menu)

    def updateLabel(self, selected_clustering, signal_to_emit):
        self.currently_selected = selected_clustering
        self.setText(selected_clustering)
        set_selected_clustering_method(selected_clustering)
        signal_to_emit.emit()

    def get_selected_method_name(self):
        return self.currently_selected

