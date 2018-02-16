# NAME
#        excelImport
#
# DESCRIPTION
#
#       The module 'excelExport.py' contains all the functions export the data to the CSV format.
#
#
# HISTORY
#
# 12 feb 2018 - Initial coding. (@yoshcraft, Raphael A.)
# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
from nibabel import Nifti1Image,load
from numpy import zeros
from csv import reader as csv_reader
import time
from ourLib.niftiHandlers.imagecollection import ImageCollection
from ourLib.niftiHandlers.nifimage import NifImage


def simple_import(csv_file_path, template_mni_path, currentSet):
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
    
    filename = unicode(csv_file_path)
    file = open(filename, "rb")
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
                ni_image = NifImage(unicode(str(key)) + ".csv", recreate_image)

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
