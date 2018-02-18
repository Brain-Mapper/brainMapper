# NAME
#        BrainMapper
#
# DESCRIPTION
#
#       The module 'BrainMapper' is the controller of our application : it links the user interface and the library
#       that handles NIfTIs
#
# HISTORY
#
# 28 november 2017 - Initial design and coding. (@Graziella-Husson, Graziella Husson)
# 12 february 2018 - Added documentation (@vz-chameleon, Valentina Zelaya)


from ourLib.niftiHandlers.nifimage import NifImage
from ourLib.niftiHandlers.imagecollection import ImageCollection
from ourLib.niftiHandlers.set import Set

from ourLib.dataExtraction import extractor as xt
from ourLib.dataExtraction.usable_data import UsableDataSet as uds
from ourLib import clustering as clust
from ourLib import calculations as calcul
from ourLib.excelImport import excelImport as imp

import os
import platform
import gc
import time
import json

# --- global variables ---
current_collec = None  # The current collection shown in edit view
selected = []  # All image collections selected by the user in main page (usefull for all views that use data)
toRM = []  # Contains all images to remove in edit view (can be used somewhere else)
currentUsableDataset = None

sets = []  # List of all sets (and sub sets) created (usefull to know if a name is already used)
clusteringsets = []  # List of sets created as a result for clustering, permit to remember wich one to create
calculsets = []  # List of sets created as a result for calculation, permit to remember wich one to create
currentSet = None  # The current set shown in main view
currentVizu = None  # The current collections shown in main view

# Dictionary of available clustering methods
app_clustering_available = {}
with open('ressources/clustering_data/clustering_algorithms_available.json', 'r') as fc:
    app_clustering_available = json.load(fc)

# Global variable for currently selected clustering method
currentClusteringMethod = None

# Global variables for calculation results
# currentCalculationResult = None


def open_nifti(path):
    """
    Opens a NIfTI file from path
    :param path: A string of the file path
    :return: NifImage instance
    """
    image = NifImage.from_file(path)
    return image


def do_image_collection(files):
    """
    Create an image collection from a lits of file path
    :param files: list of strings (file paths)
    :return: ImageCollection instance
    """
    coll = ImageCollection("default", currentSet)
    # We want an unique name for each collection
    # To do so we use the object ID
    name = str(coll).split("0x")
    name = name[1]
    coll.set_name(name[:-1])
    for file in files:
        image = open_nifti(str(file))
        coll.add(image)
    add_coll(coll)  # We add the collection create to selected by default
    currentSet.add_collection(coll)  # We add the collection created in the current set
    return coll


def add_coll(coll):
    """
    Add a collection to the selected collection list [global variable 'selected']
    :param coll: ImageCollection instance
    :return: Nothing
    """
    found = False
    for i in selected:
        if i.name == coll.name:
            found = True
    if not found :
        selected.append(coll)


def rm_coll(coll):
    """
    Remove a collection from the selected collection list [global variable 'selected']
    :param coll: ImageCollection instance
    :return: Nothing
    """
    found = False
    for i in selected:
        if i.name == coll.name:
            found = True
    if found :
        selected.remove(coll)


def get_selected():
    """
    Return the selected collections (useful for all views that use data)
    :return: global variable 'selected'
    """
    return selected


def export_nifti():
    print("Export into NIfTI...")
    print selected


def export_excel():
    print("Export into Excel...")
    print selected


def extract_data_from_selected():
    """
    Extract the interesting data from the selected image collections using extractor's module functions.
    Put this data in the global variable 'currentUsableDataSet'
    :return: Nothing. Global var 'currentUsableDataset' is modified
    """
    for x in selected:
        print(type(x))
    global currentUsableDataset
    currentUsableDataset = xt.extract_from_collection_list(selected)


def extract_data_as_centroids_from_selected():
    """
      Extract the interesting data from the selected image collections using extractor's module functions
      and only centroids as points from each file. (one centroid per file)
      Put this data in the global variable 'currentUsableDataSet'
      :return: Nothing. Global var 'currentUsableDataset' is modified
    """
    global currentUsableDataset
    currentUsableDataset = xt.extract_from_collection_list_using_centroids(selected)


def get_current_usableDataset():
    """
    Retrieve the UsableDataSet instance obtained by extracting data before clustering
    :return: a UsableDataSet instance
    """
    return currentUsableDataset


def run_clustering(selectedClusteringMethod, params_dict):
    """
    A function to run a type of clustering algorithm, triggered by run button from interface
    :param selectedClusteringMethod: a sring that is the name of the user selected clustering method
    :param params_dict: a dictionnary containing all necessary parameters for clustering and values given by the user
    :return: a list of clustering labels (to which cluster does one individual belong to)
    """
    clusterizable_dataset = currentUsableDataset.export_as_clusterizable()

    if selectedClusteringMethod == 'KMeans':
        labels = clust.perform_kmeans(params_dict, clusterizable_dataset)

    elif selectedClusteringMethod == 'KMedoids':
        labels = clust.perform_kmedoids(params_dict, clusterizable_dataset)

    elif selectedClusteringMethod == 'AgglomerativeClustering':
        labels = clust.perform_agglomerative_clustering(params_dict, clusterizable_dataset)

    elif selectedClusteringMethod == 'DBSCAN':
        labels = clust.perform_DBSCAN(params_dict, clusterizable_dataset)
    else:
        print('clustering method not recognised')
        labels = ['']

    del clusterizable_dataset  # Deleting exported data : saves memory !!
    # gc.collect()  # Call the garbage collector

    return labels


def run_calculation(selectedAlgorithm, nifti_collection, arguments):
    if selectedAlgorithm == "Addition":
        file_result, output = calcul.addition_opperation(nifti_collection)
    if selectedAlgorithm == "Boolean Intersection":
        file_result, output = calcul.and_opperation(nifti_collection)
    if selectedAlgorithm == "Boolean Union":
        file_result, output = calcul.or_opperation(nifti_collection)
    if selectedAlgorithm == "Centroide":
        file_result, output = calcul.baricentre_opperation(nifti_collection, arguments)
    if selectedAlgorithm == "Linear combination":
        file_result, output = calcul.linear_combination_opperation(nifti_collection, arguments)
    if selectedAlgorithm == "Mask":
        if len(nifti_collection) == 2:
            file_result, output = calcul.mask_opperation(nifti_collection[0], nifti_collection[1], 'Succes')
        else:
            file_result, output = calcul.mask_opperation(nifti_collection[0], nifti_collection[1], 'Error')
    if selectedAlgorithm == "Mean":
        file_result, output = calcul.mean_opperation(nifti_collection)
    if selectedAlgorithm == "Normalization":
        file_result, output = calcul.normalization_opperation(nifti_collection)
    if selectedAlgorithm == "Entropy":
        file_result, output = calcul.entropie_opperation(nifti_collection)
    if selectedAlgorithm == "Erosion":
        file_result, output = calcul.erosion_opperation(nifti_collection,arguments)
    if selectedAlgorithm == "Dilation":
        file_result, output = calcul.dilation_opperation(nifti_collection,arguments)
    if selectedAlgorithm == "Opening":
        file_result, output = calcul.opening_opperation(nifti_collection,arguments)
    if selectedAlgorithm == "Closing":
        file_result, output = calcul.closing_opperation(nifti_collection,arguments)
    if selectedAlgorithm == "Threshold":
        min = arguments[0]
        max = arguments[1]
        if min == "":
            min = "-100000.0"
        if max == "":
            max = "100000.0"
        file_result, output = calcul.threshold_opperation(nifti_collection,min,max)
    return file_result, output


def get_selected_from_name(name):
    """
    Returns the selected collection named "name" in the selected image collections list
    :param name: The collection that we look for (unique ID)
    :return: ImageCollection
    """
    for x in selected:
        if (name == x.name):
            return x


def get_toRM():
    """
    :return: Returns list of images to remove (useful for edit view -> save changes)
    """
    return toRM


def add_toRM(im):
    """
    Add an image to remove in the list toRM (useful for all views that use data)
    :param im: NifImage instance
    :return: Nothing
    """
    toRM.append(im)


def rm_toRM(im):
    """
    Remove an image to remove from the list toRM (useful for all views that use data)
    :param im: NifImage instance
    :return: Nothing
    """
    toRM.remove(im)


def reset_toRM():
    """
    Reset the list toRM (usefull for all views that use data and allow the list to be used somewhere else)
    :return: Nothing
    """
    del toRM[:]


def set_current_coll(coll):
    """
    Set the current collection [global variable] (usefull to show the collection selected in edit view)
    :param coll: ImageCollection instance
    :return: nothing
    """
    global current_collec
    current_collec = coll


def get_current_coll():
    """
    Get the current collection [global variable]
    :return: Global variable current_collec
    """
    global current_collec
    return current_collec


def set_current_coll_name(name):
    """
    Set the current collection's name (useful to rename the collection selected in edit view)
    :param name: A string that will be the new name of the collection
    :return: Nothing
    """
    cur = get_current_coll()
    cur.set_name(name)


def exists_selected(name):
    """
    Returns True if the collection's name "name" is already used by an other one in selected collections list (global var 'selected')
    :param name: The collections' name to be tested
    :return: Boolean
    """
    for i in selected:
        if (i.name == name):
            return True
    return False


def exists_coll_in_sets(name):
    """
    Returns True if the collection's name "name" is already used in one of the sets we have
    :param name: The collections' name to be tested
    :return: Boolean
    """
    sets = get_all_sets()
    for s in sets:
        collecs = s.get_coll()
        for i in collecs.values():
            if (i.name == name):
                return True
    return False


def add_image_coll(coll, files):
    """
    Add all images from a file paths list in a given collection
    :param coll: ImageCollection instance
    :param files: A list of file path's = Images to add
    :return: Nothing (modifies given collection)
    """
    for file in files:
        coll.add_from_file(str(file))


def delete_current_coll():
    """
    Delete the current collection from its set and from the app
    :return: Nothing
    """
    coll = get_current_coll()
    this_set = coll.getSetName()
    rm_coll(coll)
    reset_toRM()
    add_toRM(coll)  # We use toRM this time with a collection (toRM is rested just after used)
    set_current_coll(None)  # The current collection become None
    this_set.remove_collection(coll.name)
    print this_set.number_of_collection()  # To verify if the collection is well deleted from the data and not only from UI


def save_modifs():
    """
    Apply the changes the user made in the edit view (use toRM to know the images to remove from the current collection)
    :return: Nothing
    """
    global current_collec
    for i in toRM:
        current_collec.remove(i.filename)
    reset_toRM()


def exists_set(name):
    """
    Return True if the set's name "name" is already used by another set
    :param name: The tested set's name
    :return: Boolean
    """
    for i in sets:
        if (i.name == name):
            return True
    return False


def newSet(name):
    """
    Creates a new set a the name "name" and add it into the set list. Also change the current set with the new one
    :param name: The new set's name
    :return: Set instance
    """
    global currentSet
    new_set = Set(name)
    sets.append(new_set)
    currentSet = new_set
    return new_set


def set_current_set(new_set):
    """
    Set the current set with new_set
    :param new_set: The set to which we have to set the current set
    :return: Nothing (changes global 'currentSet')
    """
    global currentSet
    currentSet = new_set


def creation_date(path_to_file):
    """
    Return the creation date for the file located at path_to_file
    :param path_to_file: string of file path
    :return: Date
    """
    filename, file_extension = os.path.splitext(path_to_file)
    if file_extension == ".csv":
        print(time.time())
        return time.time()
    else:
        if platform.system() == 'Windows':
            return os.path.getctime(path_to_file)
        else:
            stat = os.stat(path_to_file)
            try:
                return stat.st_birthtime
            except AttributeError:
                # We're probably on Linux.
                return stat.st_mtime


def add_set(my_set):
    """
    Add my_set to the sets list
    :param my_set: Set Instance to add
    :return: Nothing
    """
    sets.append(my_set)


def rm_set(my_set):
    """
    Remove my_set from the sets list
    :param my_set: Set instance to remove
    :return: Nothing
    """
    sets.remove(my_set)


def get_current_vizu():
    """
    Return the currentVisualisation (variable currentVizu)
    :return:
    """
    global currentVizu
    return currentVizu


def set_current_vizu(collView):
    """
    Set the current vizu with the vizu collView
    :param collView:
    :return:
    """
    global currentVizu
    currentVizu = collView


def get_current_set():
    """
    Return the current set [global var 'currentSet']
    :return:
    """
    global currentSet
    return currentSet


def get_all_sets():
    """
    :return: Return all the sets that exists in the app [global var 'sets']
    """
    return sets

def getSetByName(name):
    """
    :return: the set that have the name 'name' in sets list. If it doesn't exist, return None
    """
    for i in sets:
        if i.get_name() == name :
            return i
    return None
    

def setColNameInSet(name):
    """
    Rename the current collection with the name "name". Even in its set and in selected
    :param name: new name for collection
    :return:
    """
    old = get_current_coll()
    rm_coll(old)
    this_set = old.getSetName()
    this_set.renameCollinSet(old, name)
    set_current_coll_name(name)
    cur_col = get_current_coll()
    add_coll(cur_col)


def set_selected_clustering_method(method_name):
    """
    Set the currently selected clustering method
    :param method_name: A string (the clustering method name)
    :return: Nothing (sets global current clustering method)
    """
    global currentClusteringMethod
    currentClusteringMethod = method_name


def get_selected_clustering_info():
    """
    Get the selected clustering method information from method dictionnary (loaded from json file)
    :return:
    """
    if currentClusteringMethod is not None:
        return app_clustering_available[currentClusteringMethod]
    else:
        return None


def makeClusterResultSet(a_usable_dataset, label):
    """
    Make results from clustering as sets and image collections
    :param a_usable_dataset: The data of the set, a UsableDataSet instance
    :param label: cluster label
    :return:
    """
    new_set = uds.extract_set_images_by_cluster(a_usable_dataset, label,
                                                'ressources/template_mni/mni_icbm152_t1_tal_nlin_asym_09a.nii')
    add_set(new_set)
    clusteringsets.append(new_set)


def getClusterResultSets():
    """
    :return: Global variable clustering sets, containing the clustering results as a set
    """
    return clusteringsets


def rmClusterResultSets(s):
    """
    Remove a set from clustering results set
    :param s: The set to remove
    :return: Nothing
    """
    clusteringsets.remove(s)

# ---- IMPORT ----
def simple_import(csv_file_path, template_mni_path):
    coll = imp.simple_import(csv_file_path, template_mni_path, currentSet)
    add_coll(coll)
    return coll

def makePoints(clustering_usable_dataset, label):
    return uds.extract_points(clustering_usable_dataset, label)

def makeCalculResultSet(res_set):
    add_set(res_set)
    calculsets.append(res_set)

def getCalculResultSets():
    """
    :return: Global variable calculation sets, containing the calculation results as a set
    """
    return calculsets


def rmCalculResultSets(s):
    """
    Remove a set from calculation results set
    :param s: The set to remove
    :return: Nothing
    """
    calculsets.remove(s)


def rmAllCalculResultSets():
    """
    Remove all sets from calculation results set
    :return: Nothing
    """
    for i in getCalculResultSets():
        calculsets.remove(i)
    for i in getCalculResultSets():
        calculsets.remove(i)
