from ourLib.niftiHandlers.nifimage import NifImage as ni
from ourLib.niftiHandlers.imagecollection import ImageCollection
from ourLib.dataExtraction import extractor as xt


import threading as th

global selected
selected = []

def open_nifti(path):
    image = ni.from_file(path)
    print(image.get_affine_matrix())
    # DO SOMETHING WITH THE IMAGE

    #draw_img_thread = th.Thread(target=image.plot_img())
    #draw_img_thread.start()

    #draw_glass_thread = th.Thread(target=image.plot_glass())
    #draw_glass_thread.start()
    return image

def do_image_collection(files):
    coll = ImageCollection()
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

