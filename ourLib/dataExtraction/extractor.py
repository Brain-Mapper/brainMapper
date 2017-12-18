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
# 18 december 2017 - Added Maxime's functions for data extraction (@maximeCluchague)

# Lib dependency imports
from niftiHandlers.imagecollection import ImageCollection
from niftiHandlers.nifimage import NifImage
import numpy as np
import inspect


def extract(a_nifti_img_obj):
    # Check if given param is NifImage class instance
    if not isinstance(a_nifti_img_obj, NifImage):
        raise ValueError(
            'extract function takes a NifImage class instance but ' + a_nifti_object.___class___ + ' instance was given')

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


def extract_from_collection(a_nifti_imgcoll_obj):
    # Check if given param is ImageCollection class instance
    if not isinstance(a_nifti_imgcoll_obj, ImageCollection):
        raise ValueError(
            'extract_from_collection function takes a ImageCollection class instance but ' + a_nifti_imgcoll_obj.___class___ + ' instance was given')

    res = np.zeros(shape=(1, 4)) # an empty line of zeros to start with

    # For each NifImage istance in the collection, extract data and stack results
    for nifimg in a_nifti_imgcoll_obj.get_img_list():
        res=np.concatenate((res, extract(nifimg)), axis=0)

    return res
