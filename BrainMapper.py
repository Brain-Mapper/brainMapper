from ourLib.niftiHandlers.nifimage import NifImage as ni
from ourLib.niftiHandlers.imagecollection import ImageCollection
from ourLib.niftiHandlers.set import Set

from ourLib.dataExtraction import extractor as xt
from ourLib import clustering as clust
from ourLib import calculations as calcul


import os
import platform
import gc
import json


# --- global variables ---
current_collec = None           # The current collection shown in edit view
selected = []                   # All image collections selected by the user in main page (usefull for all views that use data)
toRM = []                       # Contains all images to remove in edit view (can be used somewhere else)
currentUsableDataset = None

sets = []                       # List of all sets (and sub sets) created (usefull to know if a name is already used) 
currentSet = None               # The current set shown in main view
currentVizu = None              # The current collections shown in main view

# Dictionary of available clustering methods
app_clustering_available = {}
with open('ressources/clustering_data/clustering_algorithms_available.json', 'r') as fc:
    app_clustering_available = json.load(fc)

# Global variable for currently selected clustering method
currentClusteringMethod = None

# Global variables for calculation results
#currentCalculationResult = None



def open_nifti(path):
# --- Opens a nifti file from path

    image = ni.from_file(path)
    #print(image.get_affine_matrix())
    return image


def do_image_collection(files):
# --- Create an image collection from a lits of file path 

    coll = ImageCollection("default", currentSet)
    # We want an unique name for each collection
    # To do so we use the object ID
    name = str(coll).split("0x")
    name = name[1]
    coll.set_name(name[:-1])
    for file in files:
        image = open_nifti(str(file))
        coll.add(image)
    add_coll(coll)                      # We add the collection create to selected by default
    currentSet.add_collection(coll)     # We add the collection created in the current set
    return coll
    

def add_coll(coll):
# --- Add a collection to the selected ones

    selected.append(coll)
    

def rm_coll(coll):
# --- Remove a collection to the selected ones

    selected.remove(coll)
    

def get_selected():
# --- Return the selected collections (usefull for all views that use data)

    return selected


def export_nifti():
    print("Export into NIfTI...")
    print selected


def export_excel():
    print("Export into Excel...")
    print selected


def extract_data_from_selected():
# --- Extract the interesting data from the selected image collections using extractor's module functions
# --- :return: A UsableDataSet instance (see dataExtraction.usable_data)

    for x in selected:
        print(type(x))
    global currentUsableDataset
    currentUsableDataset = xt.extract_from_collection_list(selected)


def get_current_usableDataset():
    return currentUsableDataset


def run_clustering(selectedClusteringMethod, params_dict):

    clusterizable_dataset = currentUsableDataset.export_as_clusterizable()
    if selectedClusteringMethod == 'KMeans':
        labels = clust.perform_kmeans(params_dict, clusterizable_dataset)
    if selectedClusteringMethod == 'AgglomerativeClustering' :
        labels = clust.perform_agglomerative_clustering(params_dict, clusterizable_dataset)
    else:
        print('clustering method not recognised')
        labels = ['']

    del clusterizable_dataset   # Deleting exported data : saves memory !!
    # gc.collect()  # Call the garbage collector

    return labels


def run_calculation(algorithm,nifti_collection,arguments):
    if algorithm == "Mean":
        file_result,output = calcul.mean_opperation(nifti_collection)
    if algorithm == "Boolean Interserction":
        file_result,output = calcul.and_opperation(nifti_collection)
    if algorithm == "Boolean Union":
        file_result,output = calcul.or_opperation(nifti_collection)
    if algorithm == "Normalization":
        file_result,output = calcul.normalization_opperation(nifti_collection)
    if algorithm == "Linear combination":
        file_result,output = calcul.linear_combination_opperation(nifti_collection,arguments)
    return file_result,output


def get_selected_from_name(name):
# --- Return the selected collection named "name"

    for x in selected:
        if(name == x.name):
            return x


def get_toRM():
# --- Return list of images to remove (usefull for edit view -> save changes"

    return toRM


def add_toRM(im):
# --- Add an image to remove in the list toRM (usefull for all views that use data)

    toRM.append(im)


def rm_toRM(im):
# --- Remove an image to remove from the list toRM (usefull for all views that use data)

    toRM.remove(im)


def reset_toRM():
# --- Reset the list toRM (usefull for all views that use data and allow the list to be used somewhere else)

    del toRM[:]


def set_current_coll(coll):
# --- Set the current collection (usefull to show the collection selected in edit view)

    global current_collec
    current_collec = coll

def get_current_coll():
# --- Get te current collection

    global current_collec
    return current_collec

def set_current_coll_name(name):
# --- Set the current collection's name (usefull to rename the collection selected in edit view)

    cur = get_current_coll()
    cur.set_name(name)

def exists_selected(name):
# --- Returns True if the collection's name "name" is already used by an other one in selected

    for i in selected:
        if(i.name == name):
            return True
    return False

def exists_coll_in_sets(name):
# --- Returns True if the collection's name "name" is already used in one of the sets we have

    sets = get_all_sets()
    for s in sets:
        collecs = s.get_coll()
        for i in collecs.values():
            if(i.name == name):
                return True
    return False

def add_image_coll(coll,files):
# --- Add an image from a file path in a given collection

    for file in files:
        coll.add_from_file(str(file))

def delete_current_coll():
# --- Delete the current collection from its set and from the app

    coll = get_current_coll()
    this_set = coll.getSetName()
    rm_coll(coll)
    reset_toRM()
    add_toRM(coll)                          #We use toRM this time with a collection (toRM is rested just after used)
    set_current_coll(None)                  #The current collection become None
    this_set.remove_collection(coll.name)
    print this_set.number_of_collection()   #To verify if the collection is well deleted from the data and not only from UI

def save_modifs():
# --- Apply the changes the user made in the edit view (use toRM to know the images to remove from the current collection)

    global current_collec
    for i in toRM:
        current_collec.remove(i.filename)
    reset_toRM()

def exists_set(name):
# --- Return True if the set's name "name" is already used by another set

    for i in sets:
        if(i.name == name):
            return True
    return False

def newSet(name):
# --- Creates a new set a the name "name" and add it into the set list. Also change the current set with the new one

    global currentSet
    new_set = Set(name)
    sets.append(new_set)
    currentSet = new_set
    return new_set

def set_current_set(new_set):
# --- Set the current set with new_set

    global currentSet
    currentSet = new_set

def creation_date(path_to_file):
# --- Return the creation date for the file located at path_to_file

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
# --- Return the creation date for the file located at path_to_file

    sets.append(my_set)

def get_current_vizu():
# --- Return the currentVizu

    global currentVizu
    return currentVizu

def set_current_vizu(collView):
 # --- Set the current vizu with the vizu collView

    global currentVizu
    currentVizu = collView


def get_current_set():
# --- Return the current set

    global currentSet
    return currentSet


def get_all_sets():
# --- Return all the sets that exists in the app

    return sets 


def setColNameInSet(name):
# --- Rename the current collection with the name "name". Even in its set and in selected

    old = get_current_coll()
    rm_coll(old)
    this_set = old.getSetName()
    this_set.renameCollinSet(old,name)
    set_current_coll_name(name)
    cur_col = get_current_coll()
    add_coll(cur_col)


# --- currently selected clustering method ---
def set_selected_clustering_method(method_name):
    global currentClusteringMethod
    currentClusteringMethod = method_name


def get_selected_clustering_info():
    if currentClusteringMethod is not None:
        return app_clustering_available[currentClusteringMethod]
    else:
        return None

