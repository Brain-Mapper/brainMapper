from ourLib.niftiHandlers.nifimage import NifImage
from ourLib.niftiHandlers.imagecollection import ImageCollection
from ourLib.niftiHandlers.set import Set

from ourLib.dataExtraction import extractor as xt
from ourLib.dataExtraction.usable_data import UsableDataSet as uds
from ourLib import clustering as clust
from ourLib import calculations as calcul

from nibabel import Nifti1Image,load
from numpy import zeros
from csv import reader as csv_reader
import time

import os
import platform
import gc
import json

# --- global variables ---
current_collec = None  # The current collection shown in edit view
selected = []  # All image collections selected by the user in main page (usefull for all views that use data)
toRM = []  # Contains all images to remove in edit view (can be used somewhere else)
currentUsableDataset = None

sets = []  # List of all sets (and sub sets) created (usefull to know if a name is already used)
clusteringsets = []  # List of sets created as a result for clustering, permit to remember wich one to create
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
    # --- Opens a nifti file from path

    image = NifImage.from_file(path)
    # print(image.get_affine_matrix())
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
    add_coll(coll)  # We add the collection create to selected by default
    currentSet.add_collection(coll)  # We add the collection created in the current set
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
    elif selectedClusteringMethod == 'AgglomerativeClustering':
        labels = clust.perform_agglomerative_clustering(params_dict, clusterizable_dataset)
    else:
        print('clustering method not recognised')
        labels = ['']

    del clusterizable_dataset  # Deleting exported data : saves memory !!
    # gc.collect()  # Call the garbage collector

    return labels


def run_calculation(selectedAlgorithm, nifti_collection, arguments):
    if selectedAlgorithm == "Mean":
        file_result, output = calcul.mean_opperation(nifti_collection)
    if selectedAlgorithm == "Boolean Intersection":
        file_result, output = calcul.and_opperation(nifti_collection)
    if selectedAlgorithm == "Boolean Union":
        file_result, output = calcul.or_opperation(nifti_collection)
    if selectedAlgorithm == "Normalization":
        file_result, output = calcul.normalization_opperation(nifti_collection)
    if selectedAlgorithm == "Linear combination":
        file_result, output = calcul.linear_combination_opperation(nifti_collection, arguments)
    return file_result, output


def get_selected_from_name(name):
    # --- Return the selected collection named "name"

    for x in selected:
        if (name == x.name):
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
        if (i.name == name):
            return True
    return False


def exists_coll_in_sets(name):
    # --- Returns True if the collection's name "name" is already used in one of the sets we have

    sets = get_all_sets()
    for s in sets:
        collecs = s.get_coll()
        for i in collecs.values():
            if (i.name == name):
                return True
    return False


def add_image_coll(coll, files):
    # --- Add an image from a file path in a given collection

    for file in files:
        coll.add_from_file(str(file))


def delete_current_coll():
    # --- Delete the current collection from its set and from the app

    coll = get_current_coll()
    this_set = coll.getSetName()
    rm_coll(coll)
    reset_toRM()
    add_toRM(coll)  # We use toRM this time with a collection (toRM is rested just after used)
    set_current_coll(None)  # The current collection become None
    this_set.remove_collection(coll.name)
    print this_set.number_of_collection()  # To verify if the collection is well deleted from the data and not only from UI


def save_modifs():
    # --- Apply the changes the user made in the edit view (use toRM to know the images to remove from the current collection)

    global current_collec
    for i in toRM:
        current_collec.remove(i.filename)
    reset_toRM()


def exists_set(name):
    # --- Return True if the set's name "name" is already used by another set

    for i in sets:
        if (i.name == name):
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
    # --- Add my_set to the sets

    sets.append(my_set)

def rm_set(my_set):
    # --- Remove my_set from the sets
    sets.remove(my_set)


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
    this_set.renameCollinSet(old, name)
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

def makeClusterResultSet(a_usable_dataset, label):
    new_set = uds.extract_set_images_by_cluster(a_usable_dataset, label, 'ressources/template_mni/mni_icbm152_t1_tal_nlin_asym_09a.nii')
    add_set(new_set)
    clusteringsets.append(new_set)

def getClusterResultSets():
    return clusteringsets

def rmClusterResultSets(s):
    clusteringsets.remove(s)

def simple_import(csv_file_path, template_mni_path):
    """
    Method to import imageColection from a excel file.
    For this :method we considere that :
    - generated nifti have the same shape than the MNI152 one.
    - generated nifti have the same affine than the MNI152 one.

    The generated nifti and the imageCollection are not save with this method. they are just laod.
    So nifimage object have their strict file name as file name

    :param csv_file_path: path of the csv file.
    :param template_shape:
    :param template_affine:
    :return: imageCollection
    """
    file = open(csv_file_path, "rb")
    print(1)

    simple_header = [
        u'File_Name_Nifti',
        u'Surgeon_ID',
        u'Patient_ID',
        u'Localisation',
        u'Point_Name',
        u'Type_Of_Answer',
        u'X',
        u'Y',
        u'Z',
        u'Intensity'
    ]

    clustering_header = [
        u'Image Coll ID',
        u'Origin filename',
        u'X',
        u'Y',
        u'Z',
        u'Intensity',
        u'Assigned cluster'
    ]

    try:
        reader = csv_reader(file)

        row = reader.next()
        print(row)

        # part for a simple import
        if row == simple_header:
            print('yes')
            point_dict = dict()

            template_data = load(template_mni_path)
            template_affine = template_data.affine
            template_shape = template_data.shape

            coll = ImageCollection("default", currentSet)
            # We want an unique name for each collection
            # To do so we use the object ID
            name = str(coll).split("0x")
            name = name[1]
            coll.set_name(name[:-1])

            for row in reader:
                point = [int(float(row[6])), int(float(row[7])), int(float(row[8])), int(float(row[9]))]
                # regroup all points of the same file
                if row[0] in point_dict.keys():
                    point_dict[row[0]].append(point)
                else:
                    point_dict[row[0]] = []
                    point_dict[row[0]].append(point)

            # recreate nifti image from this points
            for key in point_dict.keys():

                recreate_affine = template_affine
                recreate_data = zeros(template_shape)

                for point in point_dict[key]:
                    recreate_data[point[0], point[1], point[2]] = point[3]

                recreate_image = Nifti1Image(recreate_data, recreate_affine)
                ni_image = NifImage(key + ".csv", recreate_image)

                # put nifti images into a imageCollection
                coll.add(ni_image)

        # pat for clustering import
        elif row == clustering_header:
            print('yes')
            point_dict = dict()

            template_data = load(template_mni_path)
            template_affine = template_data.affine
            template_shape = template_data.shape

            coll = ImageCollection("default", currentSet)
            # We want an unique name for each collection
            # To do so we use the object ID
            name = str(coll).split("0x")
            name = name[1]
            coll.set_name(name[:-1])

            for row in reader:
                point = [int(float(row[2])), int(float(row[3])), int(float(row[4])), int(float(row[5]))]
                # regroup all points of the same file
                if row[6] in point_dict.keys():
                    point_dict[row[6]].append(point)
                else:
                    point_dict[row[6]] = []
                    point_dict[row[6]].append(point)

                    # recreate nifti image from this points
                    for key in point_dict.keys():

                        recreate_affine = template_affine
                        recreate_data = zeros(template_shape)

                        for point in point_dict[key]:
                            recreate_data[point[0], point[1], point[2]] = point[3]

                        recreate_image = Nifti1Image(recreate_data, recreate_affine)
                        ni_image = NifImage("Cluster_" + key + ".csv", recreate_image)

                        # put nifti images into a imageCollection
                        coll.add(ni_image)


        else:
            print('Please use a valid csv file')

    finally:

        file.close()
    return coll
