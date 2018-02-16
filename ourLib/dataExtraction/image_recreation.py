# NAME
#        image_recreation
#
# DESCRIPTION
#
#
# HISTORY
#
# 14 feb 2018 - Initial design and coding. (@yoshcraft, Raphael A.)

from nibabel import save
from os import path
from os import makedirs


def image_recreation(folder_path, image_collection):

    for key in image_collection.nifimage_dict.keys():
        name = image_collection.nifimage_dict[key].get_name()

        save(image_collection.nifimage_dict[key].get_nib_image(), path.join(folder_path, path.basename(name).split('.')[0])+".nii.gz")


def image_recreation_from_list(folder_path, image_collection_list):

    for ic in image_collection_list:

        folder_path_ic = path.join(folder_path, ic.get_name())

        if not path.exists(folder_path_ic):
            makedirs(folder_path_ic)

        image_recreation(folder_path_ic, ic)



