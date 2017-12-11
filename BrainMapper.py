from ourLib.niftiHandlers.nifimage import NifImage as ni
import threading as th

def open_nifti(path):
    image = ni.from_file(path)
    print(image.get_affine_matrix())
    # DO SOMETHING WITH THE IMAGE

    draw_thread = th.Thread(target=image.plot_img())
    draw_thread.start()
