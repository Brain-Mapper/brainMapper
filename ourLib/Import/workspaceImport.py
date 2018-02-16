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
from ourLib.niftiHandlers.set import Set
import BrainMapper
import os


def recursive_import(folder_path, actual_set, depth):
    list = os.listdir(folder_path)
    for item in list:
        if not item.startswith('.'):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                item_list = os.listdir(item_path)
                # case for the set
                n = 0
                hn = 0
                for sub_item in item_list:
                    n = n + os.path.isfile(os.path.join(item_path, sub_item))
                    if sub_item.startswith('.'):
                        hn = hn + 1
                # because whe have hn hidden file
                if n == hn:
                    # root place, no need to have parent
                    if depth != 0:
                        actual_set.add_empty_subset(item)
                        BrainMapper.add_workspace_set(actual_set.subset_dict[item])
                        actual_set.subset_dict[item].setParent(actual_set)
                        recursive_import(item_path, actual_set.subset_dict[item], depth + 1)
                    else:
                        new_set = Set(item)
                        BrainMapper.add_workspace_set(new_set)
                        recursive_import(item_path, new_set, depth + 1)
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
                hn = 0
                for sub_item in item_list:
                    n = n + os.path.isfile(os.path.join(item_path, sub_item))
                    if sub_item.startswith('.'):
                        hn = hn + 1
                # because whe have hn hidden file
                if n == hn:
                    if item in sets:

                        return "The Set " + item + " already exist."

                    sets.append(item)
                    recursive_import_control(item_path, sets)
                elif n < len(item_list):

                    return "The file " + item + " is outside of an imageCollection."
            else:
                return "The file " + item + " is outside of an imageCollection."



