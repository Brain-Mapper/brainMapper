# NAME
#        workspaceImport
#
# DESCRIPTION
#
#       The module 'workspaceImport.py' contains all the functions import from workspace
#
#
# HISTORY
#
# 12 feb 2018 - Initial coding. (@yoshcraft, Raphael A.)
# 14 feb 2018 - Add recursive_import_control function (@yoshcraft, Raphael A.)


from ourLib.niftiHandlers.nifimage import NifImage
import BrainMapper
import os


def recursive_import(folder_path, actual_set):
    list = os.listdir(folder_path)
    for item in list:
        if not item.startswith('.'):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                item_list = os.listdir(item_path)
                # case for the set
                n = 0
                for sub_item in item_list:
                    n = n + os.path.isfile(os.path.join(item_path, sub_item))
                # 1 because whe have one hidden file
                if n == 1:
                    actual_set.add_empty_subset(item)
                    BrainMapper.sets.append(actual_set.subset_dict[item])
                    actual_set.subset_dict[item].setParent(actual_set)
                    recursive_import(item_path, actual_set.subset_dict[item])
                # case for the imageCollection
                elif n == len(item_list):
                    actual_set.add_empty_collection(item, actual_set)
                    for sub_item in item_list:
                        if not sub_item.startswith('.'):
                            actual_set.collection_dict[item].add(NifImage.from_file(os.path.join(item_path, sub_item)))


def recursive_import_control(folder_path, sets):
    list = os.listdir(folder_path)
    for item in list:
        if not item.startswith('.'):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                item_list = os.listdir(item_path)
                # case for the set
                n = 0
                for sub_item in item_list:
                    n = n + os.path.isfile(os.path.join(item_path, sub_item))
                # 1 because whe have one hidden file
                if n == 1:
                    if item in sets:
                        return False

                    sets.append(item)
                    recursive_import_control(item_path, sets)
                elif n < len(item_list):

                    return False
            else:
                return False



