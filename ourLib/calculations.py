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
# 16 january 2018 - Initial design and coding. (@maximeCluchague, Maxime C.)



import numpy as np
import nibabel as nib
from os import path
# Take as argument the nifti's path file and load this one
def load_nifti(nifti_file):
    img = nib.load(nifti_file)
    return img

def get_data(img):
    data=np.array(img.get_data(), copy=True)
    return data

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
    
def Extract_voxels_from_Nifti_file(file_name):
    img = load_nifti(file_name)
    data = get_data(img)
    
    mask = data > 0
    nb_interesting_voxels = len(data[mask].T)
    list_voxels = np.zeros(shape=(nb_interesting_voxels, 3))
    
    lx,ly,lz = data.shape
    c = 0
    for x in range(1,lx):
        if data[x].sum()>0:
            for y in range(1,ly):
                if data[x][y].sum()>0:
                    for z in range(1,lz):
                        if data[x][y][z]>0:
                            list_voxels[c]=[int(x),int(y),int(z)]
                            c=c+1
    return list_voxels.astype(int)
    
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

def save_nifti(data_nifti,filename):
	img = nib.Nifti1Image(data_nifti, np.eye(4))
  	nib.save(img,filename)        
  
def extract_name_without_path(list_path):
    list_name=""
    for filename in list_path:
        (x,name)=path.split(filename)
        list_name=list_name+"\'"+name+"\' "
    return list_name
  
def addition_opperation(Nifti_file_collection):    
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
            file_Nifti_clusterised[x][y][z] = file_Nifti_clusterised[x][y][z]+ data[x][y][z]
    print('Addition process is successfull !')
    output ="[Algorithm] > Addition\n[Input] > Nifti(s) file(s) : "+extract_name_without_path(Nifti_file_collection)+"\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {"+str(lx)+", "+str(ly)+", "+str(lz)+"}"
    return (file_Nifti_clusterised,output)

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
    print('Mean process is successfull !')
    output ="[Algorithm] > Mean\n[Input] > Nifti(s) file(s) : "+extract_name_without_path(Nifti_file_collection)+"\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {"+str(lx)+", "+str(ly)+", "+str(lz)+"}"
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
    print('Or opperation process is successfull !')
    output ="[Algorithm] > Boolean Union\n[Input] > Nifti(s) file(s) : "+extract_name_without_path(Nifti_file_collection)+"\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {"+str(lx)+", "+str(ly)+", "+str(lz)+"}"
    return (file_Nifti_clusterised,output)

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
    for e in list_pix:
        if file_Nifti_clusterised[e[0]][e[1]][e[2]] < len(Nifti_file_collection):
            file_Nifti_clusterised[e[0]][e[1]][e[2]] = 0
        else:
            file_Nifti_clusterised[e[0]][e[1]][e[2]] = 1
    print('And opperation process is successfull !')
    output ="[Algorithm] > Boolean Intersection\n[Input] > Nifti(s) file(s) : "+extract_name_without_path(Nifti_file_collection)+"\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {"+str(lx)+", "+str(ly)+", "+str(lz)+"}"
    return (file_Nifti_clusterised,output)

def linear_combination_opperation(Nifti_file_collection,coef):
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
    print('Linear combination process is successfull !')
    output ="[Algorithm] > Linear combination\n[Input] > Nifti(s) file(s) : "+extract_name_without_path(Nifti_file_collection)+"\n[Arguments] > None\n[Output] > One Nifti file with dimensions : {"+str(lx)+", "+str(ly)+", "+str(lz)+"}"
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
    print('Normalized process is successfull !')
    output ="[Algorithm] > Normalization\n[Input] > Nifti(s) file(s) : "+extract_name_without_path(Nifti_file_collection)+"\n[Arguments] > None\n[Output] > One Nifti file for each input file"
    return (file_Nifti_clusterised,output)

#Extract volume of voxel's center of gravity from a nifti file 
def baricentre_opperation(Nifti_file_collection,arguments):
    def baricentre_calculation_opperation(NiftiName,list_voxels):
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
        output = "File \'"+NiftiName+"\' | Centroid (x:"+str(mean_x)+", y:"+str(mean_y)+" ,z:"+ str(mean_z)+")"
        return(output)
    output ="[Algorithm] > Centroid[Input] > Nifti(s) file(s)\n[Arguments] > None\n[Output] > \n"
    (lx,ly,lz) = max_shape(Nifti_file_collection)
    for file in Nifti_file_collection:
        list_voxels = Extract_voxels_from_Nifti_file(file)
        (x,name)=path.split(file)
        output = output+baricentre_calculation_opperation(name,list_voxels)+"\n"
    return None,output
# Lib dependency imports
    
def entropie_opperation(Nifti_file_collection):
    def entropie(data,list_voxels,nbPixTot):
        symbol = []
        occurForEachSymbol=[]
        for e in list_voxels:
            if symbol.__contains__(data[e[0]][e[1]][e[2]]):
                indice = symbol.index(data[e[0]][e[1]][e[2]])
                occurForEachSymbol[indice] = occurForEachSymbol[indice] + 1
            else:
                symbol.append(data[e[0]][e[1]][e[2]])
                occurForEachSymbol.append(0)
        numberOfOccur = sum(occurForEachSymbol)
        print symbol
        print occurForEachSymbol
        entropie = 0
        for i in occurForEachSymbol:
            Pi = float(i)/float(nbPixTot)
            entropie = entropie - Pi*np.log2(Pi)
        print nbPixTot-numberOfOccur
        print nbPixTot
        print "\n"
        proba0 = float(nbPixTot-numberOfOccur)/float(nbPixTot)
        entropie = entropie - proba0*np.log2(proba0)
        return entropie
    (lx,ly,lz) = max_shape(Nifti_file_collection)
    output ="[Algorithm] > Entropy\n[Input] > Nifti(s) file(s) : "+extract_name_without_path(Nifti_file_collection)+"\n[Arguments] > None\n[Output] >\n"
    for file in Nifti_file_collection:
        img = load_nifti(file)
        data = get_data(img)
        list_voxels = Extract_voxels_from_Nifti_file(file)
        (x,name)=path.split(file)
        output = output+"File \'"+name+"\' | Entropy = "+str(entropie(data,list_voxels,lx*ly*lz))+"\n"
    print('Mean process is successfull !')
    
    return (None,output)
    
            
