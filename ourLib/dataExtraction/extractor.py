# NAME
#        extractor
#
# DESCRIPTION
#
#       The module 'extractor.py' contains all the functions necessary to extract
#       the interesting data from NifTi files (the voxels with a non-zero intensity)
#       These interesting voxels are returned as a usable data array :
#           lines = nb_interesting_voxels
#           columns = X, Y, Z, Intensity
#
# HISTORY
#
# 8 december 2017 - Initial design and coding. (@vz-chameleon, Valentina Z.)
# 11 december 2017 - First attempts at masking  (@vz-chameleon, Valentina Z.)
# 18 december 2017 - Added Maxime's functions for data extraction (@maximeCluchague via @vz-chameleon)
# 5 january 2018 - Adding another data extraction function, depending on numpy (@vz-chameleon)
# 12 february 2018 - Added functions to extract data using centroids

# Lib dependency imports
import numpy as np
import sys
from os import path

if __package__ is None:
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
    from usable_data import UsableDataCollection, UsableDataSet
    from ..calculations import image_centroid
else:
    from ..dataExtraction.usable_data import UsableDataCollection, UsableDataSet


def extract(a_nifti_img_obj):
    """
    Extract data from a NIfTI file representation as an array of arrays
    :param a_nifti_img_obj: A NifImage instance
    :return: An array (nb_voxels_non_zero_intensity)x4 containing several arrays [X,Y,Z,Intensity]
    """
    # # Check if given param is NifImage class instance
    # if not isinstance(a_nifti_img_obj, NifImage):
    #     raise ValueError(
    #     'extract function takes a NifImage class instance but ' + a_nifti_img_obj.___class___ + ' instance was given')

    # Array stacking is memory consuming
    # We must create an array that will be the size of extracted data
    # shape : lines = number of voxels found for which intensity is superior to 0
    #           col = four columns : X,Y,Z and intensity (for now...)

    # Safe copy the data so you won't modify the original image data (see NifImage class)
    # finite=True is given as an argument to replace NaN or Inf values by zeros
    img_data = a_nifti_img_obj.get_copy_img_data(True)

    # img_data>0 returns a boolean mask the same size as the image with :
    #     False if voxel value is not >0, True if it is
    mask = img_data > 0
    # img_data[img_data>0].T gives out an array with only positive values in it

    nb_interesting_voxels = len(img_data[mask].T)

    usable_data = np.zeros(shape=(nb_interesting_voxels, 4))

    # --- Incorporating Maxime's search
    # (modified by vz-chameleon to return an array that can be used in clustering)

    lx, ly, lz = img_data.shape  # length of the three image axis
    c = 0  # counter for array construction

    for x in range(1, lx):

        # If there is at least one value NOT EQUAL to zero, the other dimensions are worth exploring
        if img_data[x].sum() > 0:
            for y in range(1, ly):
                if img_data[x][y].sum() > 0:
                    for z in range(1, lz):
                        voxel_intensity = img_data[x][y][z]
                        if voxel_intensity > 0:
                            usable_data[c] = [x, y, z, voxel_intensity]
                            c = c + 1

    del img_data  # deleting safe copy of image data saves a lot of memory !

    return usable_data


# This version is 0.01 seconds slower than the first one
def extract2(a_nifti_img_obj):
    # Safe copy the data so you won't modify the original image data (see NifImage class)
    # finite=True is given as an argument to replace NaN or Inf values by zeros
    img_data = a_nifti_img_obj.get_copy_img_data(True)

    # img_data>0 returns a boolean mask the same size as the image with :
    #     False if voxel value is not >0, True if it is
    mask = img_data > 0
    del img_data    # saves a LOT of memory

    usable_data = np.nonzero(mask)

    return usable_data


def extract_from_collection(a_nifti_imgcoll_obj):
    """
    Extract data from a NIfTI collection as a concatenated array of results from extract(nifiamge)
    :param a_nifti_imgcoll_obj: An ImageCollection instance
    :return: An array of arrays [X,Y,Z, Intensity]
    """
    # # Check if given param is ImageCollection class instance
    # if not a.__class__ is ImageCollection:
    #     raise ValueError(
    #         'extract_from_collection function takes a ImageCollection class instance but ' + str(type(a_nifti_imgcoll_obj)) + ' instance was given')
    collection_usable_data = UsableDataCollection(a_nifti_imgcoll_obj.get_name())

    # For each NifImage istance in the collection, extract data and stack results
    img_list = a_nifti_imgcoll_obj.get_img_list()
    
    for nifimg in img_list.items():
        collection_usable_data.add_extracted_data_entry(nifimg[1], extract(nifimg[1]))

    return collection_usable_data


def extract_from_collection_list(a_nifti_imgcoll_list):
    """
    Extract data from a NIfTI collection list containing several collections as a concatenated array of extract_from_collection(imgcoll)
    :param a_nifti_imgcoll_list:
    :return: An array of arrays [X,Y,Z,Intensity]
    """
    # # Check if all elements of list are ImageCollection class instances
    # print(isinstance(x, ImageCollection) for x in a_nifti_imgcoll_list)
    # print(all(ImageCollection is x.__class___ for x in a_nifti_imgcoll_list))
    # if not all(isinstance(x, ImageCollection) for x in a_nifti_imgcoll_list):
    #     raise ValueError('extract_from_collection_list function takes an ImageCollection instances list : at least one '
    #                      'of given list elements is not an ImageCollection instance ! ')

    clustering_usable_data = UsableDataSet('Test Dataset')

    for imgcoll in a_nifti_imgcoll_list:
        clustering_usable_data.add_usable_data_collection(extract_from_collection(imgcoll))

    return clustering_usable_data


# ---------------------------------------------------------------------
# -------------------------- Using centroids --------------------------
# ---------------------------------------------------------------------

def extract_from_collection_as_centroid(a_nifti_imgcoll_obj):
    """
    Extract data from a collection using centroids calculated using image_centroid functions from calculations module
    :param a_nifti_imgcoll_obj: An ImageCollection instance
    :return: A UsableDataCollection instance
    """
    # Import function that calculates the centroid of a NifImage instance is here to avoid circular imports
    from ..calculations import image_centroid
    collection_usable_data = UsableDataCollection(a_nifti_imgcoll_obj.get_name())
    # For each NifImage istance in the collection, extract data and stack results
    img_list = a_nifti_imgcoll_obj.get_img_list()

    # For each img, ad the result of calculations' module functions, image_centroid, to the usable data set
    for nifimg in img_list.items():
        collection_usable_data.add_extracted_data_entry(nifimg[1], image_centroid(nifimg[1]))

    return collection_usable_data


def extract_from_collection_list_using_centroids(a_nifti_imgcoll_list):
    """
    Extract data from a collection list using centroids as representation
    This function calls 'extract_from_collection_as_centroid(a_nifti_imgcoll)' function
    :param a_nifti_imgcoll_list: A list of ImageCollections instances
    :return: A UsableDataSet instance
    """
    centroids_usable_data = UsableDataSet('Clustering with centroids')

    for imgcoll in a_nifti_imgcoll_list:
        centroids_usable_data.add_usable_data_collection(extract_from_collection_as_centroid(imgcoll))

    return centroids_usable_data

