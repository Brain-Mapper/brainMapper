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

from PyQt4 import QtGui
from PyQt4.Qt import *

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from BrainMapper import *

import resources


class ClusteringDataTable(QtGui.QTableWidget):
    def __init__(self):
        super(ClusteringDataTable, self).__init__()
        self.clustering_usable_dataset = None
        self.setRowCount(20)
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(["Image Coll ID","Origin filename", "X", "Y", "Z", "Intensity", "Assigned cluster"])

    def fill_with_extracted_data(self, a_usable_dataset_instance):
        self.clustering_usable_dataset = a_usable_dataset_instance
        self.setRowCount(a_usable_dataset_instance.get_row_num())

        row_count=0
        for udcoll in self.clustering_usable_dataset.get_usable_data_list():

            extracted_data_dictionary = udcoll.get_extracted_data_dict()

            for origin_file in extracted_data_dictionary.keys():
                data_array = extracted_data_dictionary[origin_file]
                for data_rows in range(0, data_array.shape[0]):
                    self.setItem(row_count, 0, QtGui.QTableWidgetItem(udcoll.get_imgcoll_name()))
                    self.setItem(row_count, 1, QtGui.QTableWidgetItem(str(origin_file.filename)))
                    self.setItem(row_count, 2, QtGui.QTableWidgetItem(str(data_array[data_rows, 0]))) # X coodinate at column 0
                    self.setItem(row_count, 3, QtGui.QTableWidgetItem(str(data_array[data_rows, 1]))) # Y coodinate at column 1
                    self.setItem(row_count, 4, QtGui.QTableWidgetItem(str(data_array[data_rows, 2]))) # Z coodinate at column 2
                    self.setItem(row_count, 5, QtGui.QTableWidgetItem(str(data_array[data_rows, 3]))) # Intensity at column 3
                    self.setItem(row_count, 6, QtGui.QTableWidgetItem("None yet"))
                    row_count = row_count+1

    def fill_clust_labels(self, assigned_labels_array):

        def generate_random_hex_dict(n):
            import random
            ra = lambda: random.randint(0, 255)
            hex_dict = dict()
            for i in range(0, n):
                hex_string = '#%02X%02X%02X' % (ra(), ra(), ra())
                hex_dict[str(i)] = hex_string
            return hex_dict

        colors = generate_random_hex_dict(len(assigned_labels_array))

        row_count = 0
        for lab in assigned_labels_array:
            item = QTableWidgetItem(str(lab))
            item.setTextAlignment(Qt.AlignCenter)
            item.setBackground(QtGui.QColor(colors[str(lab)]))
            self.setItem(row_count, 6, item)
            row_count = row_count + 1


class ClusteringView(QtGui.QWidget):
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)

    showMain = pyqtSignal()

    def __init__(self):
        super(ClusteringView, self).__init__()
        self.selected_clustMethods_displayer = None
        self.table_displayer = None
        self.initClusteringView()

    def initClusteringView(self):

        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"
        # ---------- Box Layout Set up ---------
        # Here, the instance IS a Widget, so we'll add the layouts to itself

        # - Horizontal box for a displayer of selected method
        selectedMBox = QtGui.QHBoxLayout()
        label = QtGui.QLabel('Clustering method : ')
        self.selected_clustMethods_displayer = QtGui.QLabel('KMeans(k=3)')
        self.selected_clustMethods_displayer.setMargin(5)
        self.selected_clustMethods_displayer.setStyleSheet("background-color:white;")

        selectedMBox.addWidget(label)
        selectedMBox.addWidget(self.selected_clustMethods_displayer)

        # - Horizontal box for go back home button
        buttonsBox= QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        runClusteringButton = QtGui.QPushButton('Run')
        runClusteringButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/play.png'))
        runClusteringButton.setToolTip("Run selected clustering")
        runClusteringButton.clicked.connect(lambda: self.runSelectedClust('kmeans', [3]))

        goHomeButton = QtGui.QPushButton('Go back')
        goHomeButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/home-2.png'))
        goHomeButton.setToolTip("Return to main page")
        goHomeButton.clicked.connect(self.showMain.emit)# When go back home button is clicked, change central views

        buttonsBox.addWidget(runClusteringButton)
        buttonsBox.addWidget(goHomeButton)

        topBox=QtGui.QHBoxLayout()
        topBox.addLayout(selectedMBox)
        topBox.addLayout(buttonsBox)

        # -------------- Script Environemment Widget --------------
        scriptWidget=QtGui.QWidget()
        # - Vertical box for future script Environnement
        scriptEnvBox = QtGui.QVBoxLayout()

        scriptEnv_title = QtGui.QLabel('Script Environment')
        scriptEnv_title.setStyleSheet(title_style)

        editor = QtGui.QVBoxLayout()
        edit_input = QtGui.QTextEdit()

        editor.addWidget(scriptEnv_title)
        editor.addWidget(edit_input)

        scriptEnvBox.addLayout(editor)

        # Add the layout to script widget
        scriptWidget.setLayout(scriptEnvBox)


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
        graphWidget=QtGui.QWidget()

        # Horizontal box for mini graphs display
        graphBox = QtGui.QVBoxLayout()

        graph_title = QtGui.QLabel('Results Graphs')
        graph_title.setStyleSheet(title_style)

        grid = QtGui.QGridLayout()
        grid.setSpacing(8)

        graph1 = QtGui.QTextEdit()
        graph2 = QtGui.QTextEdit()
        graph3 = QtGui.QTextEdit()
        grid.addWidget(graph1, 1, 0)
        grid.addWidget(graph2, 1, 1)
        grid.addWidget(graph3, 1, 2)

        graphBox.addWidget(graph_title)
        graphBox.addLayout(grid)

        # Set graph widgets's layout
        graphWidget.setLayout(graphBox)

        # Add the previous widgets to clustering splitter
        clust_res_splitter.addWidget(table_clust)
        clust_res_splitter.addWidget(graphWidget)

        hbox=QtGui.QHBoxLayout()
        hbox.addWidget(clust_res_splitter)
        clustWidget.setLayout(hbox)

        # ----- Now that we have our two main widgets, we can add them to the main splitter of this view -----

        # Set the layout of clustering widget and set it as the central widget for QtMainWindow
        main_splitter = QtGui.QSplitter(Qt.Horizontal)
        main_splitter.addWidget(scriptWidget)
        main_splitter.addWidget(clustWidget)

        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(main_splitter)

        containerVbox = QtGui.QVBoxLayout()
        containerVbox.addLayout(topBox)
        containerVbox.addLayout(hbox)

        self.setLayout(containerVbox)

    def fill_table(self, usable_dataset_instance):
        self.table_displayer.fill_with_extracted_data(usable_dataset_instance)

    def runSelectedClust(self, selectedMethod, param_list):
        labs = run_clustering(selectedMethod, param_list)
        # print(labs)
        # print(str(len(labs)))
        self.table_displayer.fill_clust_labels(labs)
