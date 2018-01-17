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
from PyQt4.Qt import pyqtSignal
from PyQt4.QtCore import Qt, QSize, QObjectCleanupHandler

import sys
from os import path
import gc
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
        self.setHorizontalHeaderLabels(["Image Coll ID", "Origin filename", "X", "Y", "Z", "Intensity", "Assigned cluster"])

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
                    self.setItem(row_count, 2, QtGui.QTableWidgetItem(str(data_array[data_rows, 0]))) # X coordinate at column 0
                    self.setItem(row_count, 3, QtGui.QTableWidgetItem(str(data_array[data_rows, 1]))) # Y coordinate at column 1
                    self.setItem(row_count, 4, QtGui.QTableWidgetItem(str(data_array[data_rows, 2]))) # Z coordinate at column 2
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
            item = QtGui.QTableWidgetItem(str(lab))
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
        self.clust_title = None
        self.param_box = None

        self.container_box = QtGui.QVBoxLayout()
        self.container_box.setAlignment(Qt.AlignTop)

        self.setLayout(self.container_box)

    def update_clustering_info_and_params(self, selected_clustering_name):
        method_dict = get_selected_clustering_info()
        if method_dict is None:
            err=QtGui.QMessageBox.critical(self, "Error",
                                             "No clustering method has been selected yet")
            err.setParent(None)
            err.deleteLater()   # Saves memory !
        else:
            self.clustering_name = selected_clustering_name
            self.clustering_info = method_dict['algo_info'] + "\nUsecase :" + method_dict["algo_usecase"]
            self.parameters_dict = method_dict["param_list"]

            # Clean up the previous param box and the cluster labels
            for i in reversed(range(self.container_box.count())):
                self.container_box.itemAt(i).widget().setParent(None)

            gc.collect()  # DANGER : calling garbage collector

            # ---- Add clustering info and title box ----
            self.clust_title = QtGui.QGroupBox("Clustering method parameters");
            vbox1 = QtGui.QVBoxLayout()
            grid = QtGui.QGridLayout()

            # Labels for the title group box
            clustering_selected_label = QtGui.QLabel(self.clustering_name)
            clustering_selected_label.setWordWrap(True)

            clustering_info = QtGui.QLabel("Clustering method information : ")
            clustering_selected_info = QtGui.QLabel(self.clustering_info)
            clustering_selected_info.setWordWrap(True)

            grid.addWidget(clustering_selected_label, 0, 0)

            grid.addWidget(clustering_info, 1, 0)
            grid.addWidget(clustering_selected_info, 2, 0)

            vbox1.addLayout(grid)
            self.clust_title.setLayout(vbox1)
            self.container_box.addWidget(self.clust_title)

            # Add parameter box
            self.param_box = self.ParametersBox(self.parameters_dict) #self.param_dict has been set to method_dict["param_list"]
            self.container_box.addWidget(self.param_box)

    def export_user_params(self):
        return self.param_box.get_user_params()

    # An inner class for the params box
    class ParametersBox(QtGui.QGroupBox):
        def __init__(self, parameters_dict=None):
            super(ClusteringParameters.ParametersBox, self).__init__("Parameters")
            self.user_params = {}
            self.vbox = QtGui.QVBoxLayout()

            if parameters_dict is not None:

                for param_name in parameters_dict.keys():

                    particular_param_dict = parameters_dict[param_name]
                    param = ClusteringParameters.ParameterNameAndValue(param_name, particular_param_dict["type"],
                                                                       particular_param_dict["default"],
                                                                       particular_param_dict["param_info"])

                    self.vbox.addWidget(param)
            else:
                placeholder_label = QtGui.QLabel("No parameters to show")
                self.vbox.addWidget(placeholder_label)

            self.vbox.addStretch(5)
            self.setLayout(self.vbox)

        def save_user_params(self):
            for i in reversed(range(self.vbox.count())):
                if self.vbox.itemAt(i).widget() is not None :
                    (param_name, param_value) = self.vbox.itemAt(i).widget().get_name_value_pair()
                    self.user_params[param_name] = param_value

        def get_user_params(self):
            self.save_user_params()
            return self.user_params

    # An inner class for parameter labels (simplifies the dictionnary building process)
    class ParameterNameAndValue(QtGui.QGroupBox):
        def __init__(self, param_name, param_type, param_default_value, param_info):
            super(ClusteringParameters.ParameterNameAndValue, self).__init__()
            self.grid = QtGui.QGridLayout()

            # -- Parameter's name ------
            self.param_name_label = QtGui.QLabel(param_name)

            # --- Parameter type control ----
            if type(param_type) is list:
                print("It's a list !")
                self.param_value_input = QtGui.QToolButton()
                self.param_value_input.setText(param_default_value)
                self.param_value_input.setStyleSheet("background-color: white;")
                self.param_value_input.setPopupMode(QtGui.QToolButton.MenuButtonPopup)

                param_value_chooser = QtGui.QMenu()

                for param_value_choice in param_type:
                    print(param_value_choice)
                    param_choice = QtGui.QAction(param_value_choice, self)
                    param_choice.triggered.connect(self.choice_clicked)
                    param_value_chooser.addAction(param_choice)

                self.param_value_input.setMenu(param_value_chooser)

            else:
                self.param_value_input = QtGui.QLineEdit(str(param_default_value))

            self.param_value_input.setToolTip(param_info)
            self.param_value_input.setStatusTip(param_info)
            self.param_value_input.setMaximumSize(QSize(150, 50))

            self.grid.addWidget(self.param_name_label, 0, 0)
            self.grid.addWidget(self.param_value_input, 0, 1)
            self.setLayout(self.grid)

        def choice_clicked(self):
            """
            Change label based on what button was pressed
            """
            choice = self.sender()
            if isinstance(choice, QtGui.QAction):
                self.param_value_input.setText(choice.text())

        def update_param_value_label(self, new_user_value):
            print(new_user_value)
            self.param_value_input.setText(new_user_value)

        def get_name_value_pair(self):
            return str(self.param_name_label.text()), str(self.param_value_input.text())


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
        self.stack = QtGui.QStackedWidget()
        layout = QtGui.QVBoxLayout(self) # vertical layout
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
        self.clusteringChooser.showClustParamsWidget.connect(self.update_clustering_parameters)
        # -- when clusteringChooser widget emits signal showClustParamsWidget, change current Widget in stack to scrip env widget
        self.clusteringChooser.showScriptEnvWidget.connect(partial(self.stack.setCurrentWidget, self.script_env_widget))


        # Set current widget to main view by default
        self.stack.setCurrentWidget(self.clust_params_widget)
        rec = QtGui.QApplication.desktop().availableGeometry()
        mainwind_h = rec.height() / 1.4
        mainwind_w = rec.width() / 1.5
        del rec  # Saves memory
        self.setMaximumSize(QSize(mainwind_w / 3, mainwind_h))

    def update_clustering_parameters(self):
        self.clust_params_widget.update_clustering_info_and_params(self.clusteringChooser.get_selected_method_name())
        self.stack.setCurrentWidget(self.clust_params_widget)

    def get_user_params(self) :
        if self.stack.currentWidget() is not self.script_env_widget:
            return self.stack.currentWidget().export_user_params()


class ClusteringChooser(QtGui.QToolButton):
    # -- ! ATTRIBUTES SHARED by EVERY class instance ! --

    # ------ pyqt Signals ------
    # We will use signals to communicate between the widgets ClusteringParameters and ScriptEnv, that will be stacked in
    # an instance of ParameterScriptEnvStack

    showClustParamsWidget = pyqtSignal()
    showScriptEnvWidget = pyqtSignal()

    def __init__(self):
        super(ClusteringChooser, self).__init__()
        self.currently_selected = None
        self.setText("Choose a clustering algorithm")
        self.setStyleSheet("width: 250px; background-color: #fefee1;")
        self.setPopupMode(QtGui.QToolButton.MenuButtonPopup)

        self.clustering_algo_menu = QtGui.QMenu()

        Kmeans_choice = QtGui.QAction('&KMeans', self)
        Kmeans_choice.setStatusTip('Perform KMeans algorithm on dataset')
        Kmeans_choice.triggered.connect(lambda: self.updateLabel("KMeans", self.showClustParamsWidget))

        Agglomerative_choice = QtGui.QAction('&AgglomerativeClustering', self)
        Agglomerative_choice.setStatusTip('Perform Agglomerative Clustering algorithm on dataset')
        Agglomerative_choice.triggered.connect(lambda: self.updateLabel("AgglomerativeClustering", self.showClustParamsWidget))

        user_script_choice = QtGui.QAction('&Custom user script', self)
        user_script_choice.setStatusTip('Make a custom clustering script')
        user_script_choice.triggered.connect(lambda: self.updateLabel("Custom user script", self.showScriptEnvWidget))

        self.clustering_algo_menu.addAction(Kmeans_choice)
        self.clustering_algo_menu.addAction(Agglomerative_choice)
        self.clustering_algo_menu.addAction(user_script_choice)
        self.setMenu(self.clustering_algo_menu)

    def updateLabel(self, selected_clustering, signal_to_emit):
        self.currently_selected = selected_clustering
        self.setText(selected_clustering)
        set_selected_clustering_method(selected_clustering)
        signal_to_emit.emit()

    def get_selected_method_name(self):
        return self.currently_selected


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
        self.param_script_stack = None
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
        runClusteringButton.clicked.connect(lambda: self.runSelectedClust(self.clust_chooser.get_selected_method_name(), self.param_script_stack.get_user_params()))

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

        self.param_script_stack = ParameterScriptEnvStack(title_style, self.clust_chooser)

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
        print(param_dict)
        labs = run_clustering(selectedMethod, param_dict)
        self.table_displayer.fill_clust_labels(labs)
