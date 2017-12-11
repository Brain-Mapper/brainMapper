from ourLib.niftiHandlers.nifimage import NifImage as ni
import threading as th

def open_nifti(path):
    image = ni.from_file(path)
    print(image.get_affine_matrix())
    # DO SOMETHING WITH THE IMAGE

    draw_img_thread = th.Thread(target=image.plot_img())
    draw_img_thread.start()

    draw_glass_thread = th.Thread(target=image.plot_glass())
    draw_glass_thread.start()