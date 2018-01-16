from ourLib.niftiHandlers.nifimage import NifImage as ni
from ourLib.niftiHandlers.imagecollection import ImageCollection
from ourLib.niftiHandlers.set import Set

from ourLib.dataExtraction import extractor as xt
from ourLib import clustering as clust


import os
import platform
import threading as th
import json


# --- global variables ---
current_collec = None
selected = []
toRM = []
currentUsableDataset = None
sets = []
currentSet = None
currentVizu = None


# Dictionary of available clustering methods
app_clustering_available = {}
with open('ressources/clustering_data/clustering_algorithms_available.json', 'r') as fc:
    app_clustering_available = json.load(fc)

# Global variable for currently selected clustering method
currentClusteringMethod = None


def open_nifti(path):
    image = ni.from_file(path)
    print(image.get_affine_matrix())
    return image


def do_image_collection(files):
    coll = ImageCollection("default", currentSet)
    # We want an unique name for each collection
    # To do so we use the object ID
    name = str(coll).split("0x")
    name = name[1]
    coll.set_name(name[:-1])
    for file in files:
        image = open_nifti(str(file))
        coll.add(image)
    #extracted_data = xt.extract_from_collection(coll)
    #print(extracted_data)
    add_coll(coll)
    currentSet.add_collection(coll)
    return coll
    

def add_coll(coll):
    selected.append(coll)
    

def rm_coll(coll):
    selected.remove(coll)
    

def get_selected():
    return selected


def export_nifti():
    print("Export into NIfTI...")
    print selected


def export_excel():
    print("Export into Excel...")
    print selected


def extract_data_from_selected():
    """
    Extract the interesting data from the selected image collections using extractor's module functions
    :return: A UsableDataSet instance (see dataExtraction.usable_data)
    """
    for x in selected:
        print(type(x))
    global currentUsableDataset
    currentUsableDataset = xt.extract_from_collection_list(selected)


def get_current_usableDataset():
    return currentUsableDataset


def run_clustering(selectedClusteringMethod, params_list):
    if selectedClusteringMethod == 'kmeans':
        labels = clust.perform_kmeans(params_list[0], currentUsableDataset.export_as_clusterizable())
    else:
        print('clustering method not recognised')
        labels = ['']

    return labels

def get_selected_from_name(name):
    for x in selected:
        if(name == x.name):
            return x

def get_toRM():
    return toRM

def add_toRM(im):
    toRM.append(im)

def rm_toRM(im):
    toRM.remove(im)

def reset_toRM():
    del toRM[:]

def set_current_coll(coll):
    global current_collec
    current_collec = coll

def get_current_coll():
    global current_collec
    return current_collec

def set_current_coll_name(name):
    global current_collec
    current_collec.set_name(name)

def exists_selected(name):
    for i in selected:
        if(i.name == name):
            return True
    return False

def exists_coll_in_sets(name):
    sets = get_all_sets()
    for s in sets:
        collecs = s.get_coll()
        for i in collecs.values():
            if(i.name == name):
                return True
    return False

def add_image_coll(coll,files):
    for file in files:
        coll.add_from_file(str(file))

def delete_coll(coll):
    this_set = coll.getSetName()
    rm_coll(coll)
    reset_toRM()
    add_toRM(coll)
    this_set.remove_collection(coll.name)
    #print this_set.number_of_collection()

def save_modifs():
    global current_collec
    for i in toRM:
        current_collec.remove(i.filename)
    reset_toRM()

def exists_set(name):
    for i in sets:
        if(i.name == name):
            return True
    return False

def newSet(name):
    global currentSet
    new_set = Set(name)
    sets.append(new_set)
    currentSet = new_set
    return new_set

def set_current_set(new_set):
    global currentSet
    currentSet = new_set

def creation_date(path_to_file):
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
    sets.append(my_set)

def get_current_vizu():
    global currentVizu
    return currentVizu

def set_current_vizu(collView):
    global currentVizu
    currentVizu = collView

def get_current_set():
    global currentSet
    return currentSet

# --- currently selected clustering method ---
def set_selected_clustering_method(method_name):
    global currentClusteringMethod
    currentClusteringMethod = method_name

def get_all_sets():
    return sets 
