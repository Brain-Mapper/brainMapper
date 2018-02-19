
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
# 5 january 2018 - Added functions to fill table with extracted data
# 13 fev 2018 - Add histogram view (@Graziella-Husson)

from PyQt4 import QtGui
from PyQt4.Qt import pyqtSignal, QFileDialog
from PyQt4.QtCore import Qt, QRect

from BrainMapper import *
import ourLib.ExcelExport.excelExport as ee
import os

import numpy as np
import pyqtgraph.opengl as gl

# View components' import
from clustering_components.clustering_results import ClusteringDataTable, ClusteringGraphs, ClusteringResultsPopUp
from clustering_components.clustering_paramspace import ParameterAndScriptStack
from clustering_components.clustering_topbar import *

import resources


class ClusteringView(QtGui.QWidget):
    """
    A custom QWidget that is the clustering view.
    Its components are : ClusteringChooser, ClusteringButtonBar, ParamAndScriptStack, ClusteringDataTable
    (see 'clustering_components' directory for their modules)
    """
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)

    showMain = pyqtSignal()

    # CONSTRUCTOR
    def __init__(self):
        super(ClusteringView, self).__init__()
        self.clust_chooser = None
        self.table_displayer = None

        self.results_popup = ClusteringResultsPopUp(':ressources/logo.png', ':ressources/app_icons_png/file-1.png')

        self.label = None

        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"
        # ---------- Box Layout Set up ---------
        # Here, the instance IS a Widget, so we'll add the layouts to itself

        # - Horizontal box for a displayer of selected method
        selectedMBox = QtGui.QHBoxLayout()
        label = QtGui.QLabel('Clustering method : ')
        self.clust_chooser = ClusteringChooser() # Our custom widget for clustering algorithm selection

        selectedMBox.addWidget(label)
        selectedMBox.addWidget(self.clust_chooser)

        # --- Param/Script Env Stack ------
        self.param_script_stack = ParameterAndScriptStack(title_style, self.clust_chooser)

        # - Horizontal box for go back home button
        buttonsBox= QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        runClusteringButton = QtGui.QPushButton('Run')
        runClusteringButton.setStyleSheet("background-color: #b4ecb4;")
        runClusteringButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/play.png'))
        runClusteringButton.setStatusTip("Run selected clustering")
        runClusteringButton.clicked.connect(lambda: self.runSelectedClust(self.clust_chooser.get_selected_method_name(), self.param_script_stack.get_user_params()))

        detailsButton = QtGui.QPushButton('Results Details')
        detailsButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/powerpoint.png'))
        detailsButton.setStatusTip("Show more details on clustering results")
        detailsButton.clicked.connect(lambda: self.popup_results_details(self.clust_chooser.get_selected_method_name(),
                                                                         self.param_script_stack.get_user_params()))

        goHomeButton = QtGui.QPushButton('Go back')
        goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        goHomeButton.setStatusTip("Return to main page")
        goHomeButton.clicked.connect(self.go_back)# When go back home button is clicked, change central views

        exportButton = QtGui.QPushButton('Export')
        exportButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/libreoffice.png'))
        exportButton.setStatusTip("Export to CSV file")
        exportButton.clicked.connect(self.export)

        saveButton = QtGui.QPushButton('Save as set')
        saveButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/checking.png'))
        saveButton.setStatusTip("Save the results in a set (available in home page)")
        saveButton.clicked.connect(self.save)

        buttonsBox.addWidget(runClusteringButton)
        buttonsBox.addWidget(detailsButton)
        buttonsBox.addWidget(exportButton)
        buttonsBox.addWidget(saveButton)
        buttonsBox.addWidget(goHomeButton)

        topBox=QtGui.QHBoxLayout()
        topBox.addLayout(selectedMBox)
        topBox.addLayout(buttonsBox)


        # -------------- Clustering Widget -----------------------
        clustWidget = QtGui.QWidget()

        # - A splitter for clustering results display
        clust_res_splitter = QtGui.QSplitter(Qt.Vertical)

        # === A table widget ===
        table_clust=QtGui.QWidget()

        # Horizontal box for table display
        tableBox = QtGui.QVBoxLayout()

        table_title = QtGui.QLabel('Data - Clustering Results')
        table_title.setStyleSheet(title_style)
        self.table_displayer = ClusteringDataTable()
        tableBox.addWidget(table_title)
        tableBox.addWidget(self.table_displayer)

        # set table clust widget's layout
        table_clust.setLayout(tableBox)

        # === A graphs widget ===
        self.resultsGraphs = ClusteringGraphs(title_style)

        # Add the previous widgets to clustering splitter
        clust_res_splitter.addWidget(table_clust)
        clust_res_splitter.addWidget(self.resultsGraphs)

        hbox=QtGui.QHBoxLayout()
        hbox.addWidget(clust_res_splitter)
        clustWidget.setLayout(hbox)

        # ----- Now that we have our two main widgets, we can add them to the main splitter of this view -----

        # Set the layout of clustering widget and set it as the central widget for QtMainWindow
        main_splitter = QtGui.QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.param_script_stack)
        main_splitter.addWidget(clustWidget)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(main_splitter)

        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(topBox)
        containerVbox.addLayout(hbox)

        self.setLayout(containerVbox)

    def fill_table(self, usable_dataset_instance):
        self.table_displayer.fill_with_extracted_data(usable_dataset_instance)

    def runSelectedClust(self, selectedMethod, param_dict):
        self.label = run_clustering(selectedMethod, param_dict)
        self.table_displayer.fill_clust_labels(self.label)
        self.add_hist(param_dict, self.label)
        self.add_3D(self.table_displayer.clustering_usable_dataset, self.label)

    def export(self):
        if self.label is not None:
            (f_path, f_name) = os.path.split(str(QFileDialog.getSaveFileName(self, "Browse Directory")))

            ee.clustering_export(f_name, f_path, self.table_displayer.clustering_usable_dataset, self.label)
        else:
            QtGui.QMessageBox.information(self, "Run Clustering before", "No cluster affectation")

    def save(self):
        if self.label is not None:
            makeClusterResultSet(self.table_displayer.clustering_usable_dataset, self.label)
            QtGui.QMessageBox.information(self, "Results saved!", "A set has been created in the clustering results tab at home page.")

        else:
            QtGui.QMessageBox.information(self, "Run Clustering before", "No cluster affectation")

    def add_hist(self, param_dict, label):

        k = float(param_dict["n_clusters"])
        self.resultsGraphs.clear_graph1()
        plt = self.resultsGraphs.graph1.addPlot()

        # make interesting distribution of values
        vals = np.hstack([label])

        # compute standard histogram
        y, x = np.histogram(vals, bins=np.linspace(0, k, k+1))

        # Using stepMode=True causes the plot to draw two lines for each sample.
        # notice that len(x) == len(y)+1
        plt.plot(x, y, stepMode=True, fillLevel=0, brush=(0, 0, 255, 150))

    def add_3D(self, clustering_usable_dataset, label):
        old = self.resultsGraphs.grid.itemAt(1).widget()
        self.resultsGraphs.grid.removeWidget(old)
        old.setParent(None)

        self.resultsGraphs.graph2 = gl.GLViewWidget()
        self.resultsGraphs.graph2.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.resultsGraphs.grid.addWidget(self.resultsGraphs.graph2, 1, 1)
        res = makePoints(clustering_usable_dataset, label)
        sp1 = gl.GLScatterPlotItem(pos=res[0], size=res[1], color=res[2], pxMode=True)
        sp1.translate(5, 5, 0)
        sp1.setGLOptions('opaque')
        self.resultsGraphs.graph2.addItem(sp1)

    def go_back(self):
        # -- When the user wants to return to the main view, we reinit the cluster view
        self.resultsGraphs.graph1.clear()
        old = self.resultsGraphs.grid.itemAt(1).widget()
        self.resultsGraphs.grid.removeWidget(old)
        old.setParent(None)
        self.resultsGraphs.graph2 = gl.GLViewWidget()
        self.resultsGraphs.graph2.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.resultsGraphs.grid.addWidget(self.resultsGraphs.graph2, 1, 1)
        self.showMain.emit()

    def popup_results_details(self, method_name, user_params):
        self.results_popup.setGeometry(QRect(100, 100, 500, 300))

        if self.label is not None:
            self.results_popup.update_details(method_name, user_params, clustering_validation_indexes(self.label))

        self.results_popup.show()
