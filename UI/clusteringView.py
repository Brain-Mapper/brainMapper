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
from functools import partial

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
                # Mixing with white to have pastel colors
                hex_string = '#%02X%02X%02X' % ((ra()+255)/2, (ra()+255)/2, (ra()+255)/2)
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


class ClusteringParameters(QtGui.QWidget):

    def __init__(self):
        super(ClusteringParameters, self).__init__()

        # I chose to use a dictionary : the implemented base clustering algorithms will give an
        # 'expected parameter dictionnary'...
        # For example : {"distance":None, "k":None}, could be the dictionary given by the Kmeans method,
        # and it will expect this dictionary to be completed by the user

        self.parameters_dict = None
        self.clustering_name = "None selected yet"
        self.clustering_info = "Please select a classifier from the top menu"

        self.container_box = None
        self.param_box = None
        self.init_parameterBox()

    def init_parameterBox(self):
        self.container_box = QtGui.QVBoxLayout()
        self.container_box.setAlignment(Qt.AlignTop)

        # --- Parameters box title : clustering name + info -----

        grp_box_title = QtGui.QGroupBox("Clustering method parameters");
        vbox1 = QtGui.QVBoxLayout()
        grid = QtGui.QGridLayout()

        # Labels for the title group box
        clustering_method_label = QtGui.QLabel("Clustering : ")
        clustering_selected_label = QtGui.QLabel(self.clustering_name)

        clustering_info = QtGui.QLabel("Clustering method information : ")
        clustering_selected_info = QtGui.QLabel(self.clustering_info)

        grid.addWidget(clustering_method_label, 0, 0)
        grid.addWidget(clustering_selected_label, 1, 0)

        grid.addWidget(clustering_info, 2, 0)
        grid.addWidget(clustering_selected_info, 3, 0)

        vbox1.addLayout(grid)
        grp_box_title.setLayout(vbox1)

        self.container_box.addWidget(grp_box_title)

        # --- Parameters box to be filled by user -----
        self.param_box= self.ParametersBox("Method parameters")
        self.container_box.addWidget(self.param_box)

        self.setLayout(self.container_box)

    def fill_parameter_box(self, clustering_parameters_dict, clustering_name, clustering_info):
        print("I dont know what to do yet")

    def get_parameters_list(self):
        return self.parameters_list

    # An inner class for the params box
    class ParametersBox(QtGui.QGroupBox):
        def __init__(self, box_name, parameters_dict=None):
            super(ClusteringParameters.ParametersBox, self).__init__(box_name)
            vbox = QtGui.QVBoxLayout()
            if parameters_dict is not None:
                self.grid = QtGui.QGridLayout()

                line = 0
                for param_name in parameters_dict.keys():
                    param_name_label = QtGui.QLabel(param_name)
                    param_value_label = QtGui.QLabel(parameters_dict[param_name])
                    self.grid.addWidget(param_name_label, line, 0)
                    self.grid.addWidget(param_value_label, line, 1)
                    line = line + 1

            else:
                self.grid = QtGui.QGridLayout()
                placeholder_label = QtGui.QLabel("No parameters to show")
                self.grid.addWidget(placeholder_label, 1, 1)

            vbox.addLayout(self.grid)
            vbox.addStretch(5)
            self.setLayout(vbox)

        # def set_Params


# A custom widget to implement the script environment
class ScriptEnvironment(QtGui.QWidget):
    
    def __init__(self, title_style):
        super(ScriptEnvironment, self).__init__()

        container_box = QtGui.QVBoxLayout()

        scriptEnv_title = QtGui.QLabel('Script Environment')
        scriptEnv_title.setStyleSheet(title_style)

        editor = QtGui.QVBoxLayout()
        self.edit_input = QtGui.QTextEdit()

        editor.addWidget(scriptEnv_title)
        editor.addWidget(self.edit_input)

        container_box.addLayout(editor)

        # Add the layout to script widget
        self.setLayout(container_box)


# A custom widget to stack the ClusteringParameters Widget and the ScripEnvironnement Widget
class ParameterScriptEnvStack(QtGui.QWidget):

    def __init__(self, title_style, clustering_chooser=None):

        super(ParameterScriptEnvStack, self).__init__()

        # Initialize a stack (pile) widget
        self.stack = QStackedWidget()
        layout = QVBoxLayout(self) # vertical layout
        layout.addWidget(self.stack) # stack in the vertical layout

        # Here are the custom widgets we will put on the stack
        self.clust_params_widget = ClusteringParameters()
        self.script_env_widget = ScriptEnvironment(title_style)
        # -- Add them to stack widget
        self.stack.addWidget(self.clust_params_widget)
        self.stack.addWidget(self.script_env_widget)

        self.clusteringChooser = clustering_chooser

        # Define behaviour when widget emit certain signals (see class MainView and Clustering View for more details
        #  on signals and events)

        # -- when clusteringChooser widget emits signal showClustParamsWidget, change current Widget in stack to clust params widget
        self.clusteringChooser.showClustParamsWidget.connect(partial(self.stack.setCurrentWidget, self.clust_params_widget))
        # -- when clusteringChooser widget emits signal showClustParamsWidget, change current Widget in stack to scrip env widget
        self.clusteringChooser.showScriptEnvWidget.connect(partial(self.stack.setCurrentWidget, self.script_env_widget))


        # Set current widget to main view by default
        self.stack.setCurrentWidget(self.clust_params_widget)
        rec = QApplication.desktop().availableGeometry()
        mainwind_h = rec.height() / 1.4
        mainwind_w = rec.width() / 1.5
        del rec  # Saves memory
        self.setMaximumSize(QSize(mainwind_w / 3, mainwind_h))


class ClusteringChooser(QtGui.QToolButton):
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to communicate between the widgets ClusteringParameters and ScriptEnv, that will be stacked in
    # an instance of ParameterScriptEnvStack

    showClustParamsWidget = pyqtSignal()
    showScriptEnvWidget = pyqtSignal()

    def __init__(self):
        super(ClusteringChooser, self).__init__()
        self.setText("Choose a clustering algorithm")
        self.setStyleSheet("width: 250px; background-color: #fefee1;")
        self.setPopupMode(QtGui.QToolButton.MenuButtonPopup)

        self.clustering_algo_menu = QtGui.QMenu()

        Kmeans_choice = QtGui.QAction('&KMeans', self)
        Kmeans_choice.setStatusTip('Perform KMeans algorithm on dataset')
        Kmeans_choice.triggered.connect(lambda: self.updateLabel("KMeans", self.showClustParamsWidget))

        user_script_choice = QtGui.QAction('&Custom user script', self)
        user_script_choice.setStatusTip('Make a custom clustering script')
        user_script_choice.triggered.connect(lambda: self.updateLabel("Custom user script", self.showScriptEnvWidget))

        self.clustering_algo_menu.addAction(Kmeans_choice)
        self.clustering_algo_menu.addAction(user_script_choice)
        self.setMenu(self.clustering_algo_menu)

    def updateLabel(self, selected_clustering, signal_to_emit):
        self.setText(selected_clustering)
        print(app_clustering_available)
        signal_to_emit.emit()



class ClusteringView(QtGui.QWidget):
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to know when to change the central view (central widget) of our app
    # In our custom widgets (like this one), buttons will emit a given signal, and the change of views will be handled
    # by the HomePage widgets' instances (see UI.py, class HomePage)

    showMain = pyqtSignal()

    def __init__(self):
        super(ClusteringView, self).__init__()
        self.clust_chooser = None
        self.table_displayer = None
        self.initClusteringView()

    def initClusteringView(self):

        title_style = "QLabel { background-color : #ffcc33 ; color : black;  font-style : bold; font-size : 14px;}"
        # ---------- Box Layout Set up ---------
        # Here, the instance IS a Widget, so we'll add the layouts to itself

        # - Horizontal box for a displayer of selected method
        selectedMBox = QtGui.QHBoxLayout()
        label = QtGui.QLabel('Clustering method : ')
        self.clust_chooser = ClusteringChooser() # Our custom widget for clustering algorithm selection

        selectedMBox.addWidget(label)
        selectedMBox.addWidget(self.clust_chooser)

        # - Horizontal box for go back home button
        buttonsBox= QtGui.QHBoxLayout()
        buttonsBox.addStretch(1)

        runClusteringButton = QtGui.QPushButton('Run')
        runClusteringButton.setStyleSheet("background-color: #b4ecb4;")
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

        # --- Param/Script Env Stack ------

        param_script_stack = ParameterScriptEnvStack(title_style, self.clust_chooser)

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
        main_splitter.addWidget(param_script_stack)
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
