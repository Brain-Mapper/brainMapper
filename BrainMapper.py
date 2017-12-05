from ourLib.niftiHandlers.nifimage import NifImage as ni

def open_nifti(path):
    image = ni.from_file(path)
    print(image.get_affine_matrix())
    # DO SOMETHING WITH THE IMAGE
