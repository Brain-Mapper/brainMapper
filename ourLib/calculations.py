# NAME
#        calculations
#
# DESCRIPTION
#
#       The module 'calculations' contains methods for mathematical or preprocessing operations on
#       nifti image collections, sets or single files
#
# HISTORY
#
# 15 december 2017 - Initial design and coding. (@vz-chameleon, Valentina Z.)


# System imports
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
#import random

#####################################################################
#                        LOAD NIFTI & VIEWER                        #
#####################################################################

# Take as argument the nifti's path file and load this one
def load_nifti(nifti_file):
    img = nib.load(nifti_file)
    return img

def get_data(img):
    #data = copy.deepcopy(img.get_data())
    data=np.array(img.get_data(), copy=True)
    return data

# Viewer of nifti image axe X
def nifti_viewer_X(img,x):
    img_data = img.get_data()
    plt.matshow(img_data[x,:,:])
    plt.show()
    
# Viewer of nifti image axe Y
def nifti_viewer_Y(img,y):
    img_data = img.get_data()
    plt.matshow(img_data[:,y,:])
    plt.show()
    
# Viewer of nifti image axe Z
def nifti_viewer_Z(img,z):
    img_data = img.get_data()
    plt.matshow(img_data[:,:,z])
    plt.show()


#####################################################################
#                      DATA NIFTI EXTRACTION                        #
#####################################################################


def Extract_voxels_from_Nifti_file(file_name):
    img = load_nifti(file_name)
    data = get_data(img)
    list_voxels = []
    lx,ly,lz = data.shape
    for x in range(1,lx):
        if data[x].sum()>0:
            for y in range(1,ly):
                if data[x][y].sum()>0:
                    for z in range(1,lz):
                        if data[x][y][z]>0:
                            list_voxels.append([x,y,z])
    return list_voxels
    

#####################################################################
#                         NIFTI OPPERATION                          #
#####################################################################
def max_shape(Nifti_collection):
        max_X = 0
        max_Y = 0
        max_Z = 0
        for file in Nifti_collection:
            img = load_nifti(file)
            (x,y,z) = img.shape
            if x > max_X:
                max_X = x
            if y > max_Y:
                max_Y = y
            if z > max_Z:
                max_Z = z
        return (max_X,max_Y,max_Z)
        
#Clustering between differents nifti file    
def mean_opperation(Nifti_file_collection):    
    (lx,ly,lz) = max_shape(Nifti_file_collection)
    file_Nifti_clusterised = np.zeros(shape=(lx,ly,lz), dtype='f')
    for file in Nifti_file_collection:
        img = load_nifti(file)
        data = get_data(img)
        list_voxels = Extract_voxels_from_Nifti_file(file)
        for voxels in list_voxels:
            x = voxels[0]
            y = voxels[1]
            z = voxels[2]
            file_Nifti_clusterised[x][y][z] = file_Nifti_clusterised[x][y][z]+ data[x][y][z]/float(len(Nifti_file_collection))
    #On enregistre le cluster dans un nouveau fichier Nifti 
    #img = nib.Nifti1Image(file_Nifti_clusterised, np.eye(4))
    #nib.save(img,file_name)
    print('Mean process is successfull !')
    output =""
    return (file_Nifti_clusterised,output)


def or_opperation(Nifti_file_collection): 
    (lx,ly,lz) = max_shape(Nifti_file_collection)
    file_Nifti_clusterised = np.zeros(shape=(lx,ly,lz), dtype='f')
    for file in Nifti_file_collection:
        list_voxels = Extract_voxels_from_Nifti_file(file)
        for voxels in list_voxels:
            x = voxels[0]
            y = voxels[1]
            z = voxels[2]
            file_Nifti_clusterised[x][y][z] = 1
    #On enregistre le cluster dans un nouveau fichier Nifti 
    #img = nib.Nifti1Image(file_Nifti_clusterised, np.eye(4))
    #nib.save(img,file_name)
    print('Or opperation process is successfull !')
    output =""
    return (file_Nifti_clusterised,output)

def max_value(list):    
    max = list[0]
    for e in list:
        if e > max:
            max = e
    return max

def min_value(list):    
    min = list[0]
    for e in list:
        if e < min:
            min = e
    return min


def and_opperation(Nifti_file_collection): 
    (lx,ly,lz) = max_shape(Nifti_file_collection)
    file_Nifti_clusterised = np.zeros(shape=(lx,ly,lz), dtype='f')
    list_pix = []
    for file in Nifti_file_collection:
        list_voxels = Extract_voxels_from_Nifti_file(file)
        for voxels in list_voxels:
            x = voxels[0]
            y = voxels[1]
            z = voxels[2]
            if not list_pix.__contains__([x,y,z]):
                list_pix.append([x,y,z])
            file_Nifti_clusterised[x][y][z] = file_Nifti_clusterised[x][y][z] + 1
    #On enregistre le cluster dans un nouveau fichier Nifti 
    #img = nib.Nifti1Image(file_Nifti_clusterised, np.eye(4))
    #nib.save(img,file_name)
    for e in list_pix:
        if file_Nifti_clusterised[e[0]][e[1]][e[2]] < len(Nifti_file_collection):
            file_Nifti_clusterised[e[0]][e[1]][e[2]] = 0
        else:
            file_Nifti_clusterised[e[0]][e[1]][e[2]] = 1
    print('And opperation process is successfull ! File result : \''+file_name+'\'')
    output =""
    return (file_Nifti_clusterised,output)

def linear_combination_opperation(Nifti_file_collection,coef):
    max_coef = max_value(coef)
    (lx,ly,lz) = max_shape(Nifti_file_collection)
    file_Nifti_clusterised = np.zeros(shape=(lx,ly,lz), dtype='f')
    i = 0
    for file in Nifti_file_collection:
        img = load_nifti(file)
        data = get_data(img)
        list_voxels = Extract_voxels_from_Nifti_file(file)
        for voxels in list_voxels:
            x = voxels[0]
            y = voxels[1]
            z = voxels[2]
            file_Nifti_clusterised[x][y][z] = file_Nifti_clusterised[x][y][z]+ data[x][y][z]*float(coef[i])
        i = i+1
    #On enregistre le cluster dans un nouveau fichier Nifti 
    #img = nib.Nifti1Image(file_Nifti_clusterised, np.eye(4))
    #nib.save(img,file_name)
    #print('\nLinear combination process was successfull ! File result : \''+file_name+'\'')
    output =""
    return (file_Nifti_clusterised,output)

def normalization_opperation(Nifti_file_collection):
    (lx,ly,lz) = max_shape(Nifti_file_collection)
    file_Nifti_clusterised = np.zeros(shape=(lx,ly,lz), dtype='f')
    for file in Nifti_file_collection:
        img = load_nifti(file)
        data = get_data(img)
        list_voxels = Extract_voxels_from_Nifti_file(file)
	somme_value = sum(list_voxels)
        for voxels in list_voxels:
            x = voxels[0]
            y = voxels[1]
            z = voxels[2]
            file_Nifti_clusterised[x][y][z] = data[x][y][z]/float(somme_value)
        #On enregistre le cluster dans un nouveau fichier Nifti 
        img = nib.Nifti1Image(file_Nifti_clusterised, np.eye(4))
        nib.save(img,file)
    print('Normalized process is successfull !')
    output =""
    return (file_Nifti_clusterised,output)


#Extract volume of voxel's center of gravity from a nifti file 
def baricentre_calculation_opperation(list_voxels):
    mean_x = 0
    mean_y = 0
    mean_z = 0
    for e in list_voxels:
        mean_x = mean_x + e[0]
        mean_y = mean_y + e[1]
        mean_z = mean_z + e[2]
    mean_x = mean_x/len(list_voxels)
    mean_y = mean_y/len(list_voxels)
    mean_z = mean_z/len(list_voxels)
    return(mean_x,mean_y,mean_z)

# Lib dependency imports
