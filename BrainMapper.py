from ourLib.niftiHandlers.nifimage import NifImage as ni
from ourLib.niftiHandlers.imagecollection import ImageCollection

from ourLib.dataExtraction import extractor as xt
from ourLib import clustering as clust

import json

# --- global variables ---
current_collec = None
selected = []
toRM = []
currentUsableDataset = None


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
    coll = ImageCollection("default")
    # We want an unique name for each collection
    # To do so we use the object ID
    name = str(coll).split("0x")
    coll.set_name("<"+name[1])
    for file in files:
        image = open_nifti(str(file))
        coll.add(image)
    #extracted_data = xt.extract_from_collection(coll)
    #print(extracted_data)
    add_coll(coll)
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

def add_image_coll(coll,files):
    for file in files:
        coll.add_from_file(str(file))

def delete_coll(coll):
    print "delete " + str(coll.name)

def save_modifs():
    global current_collec
    print current_collec.get_img_list()
    for i in toRM:
        current_collec.remove(i.filename)
    print current_collec.get_img_list()
    reset_toRM()


# --- currently selected clustering method ---
def set_selected_clustering_method(method_name):
    global currentClusteringMethod
    currentClusteringMethod = method_name
