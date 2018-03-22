
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import pylab
import csv

plt.rcParams['image.cmap'] = 'gray'
plt.rcParams['image.interpolation'] = 'nearest'

template_mni = nib.load('/Users/raphaelagathon/Desktop/PI_nifti/mni_icbm152_csf_tal_nlin_asym_09c.nii')
template_affine = template_mni.affine
template_shape = template_mni.get_data().shape

true_image = nib.load('/Users/raphaelagathon/Desktop/PI_nifti/P92 F M0 1.nii')
true_affine = true_image.affine
true_shape = true_image.get_data().shape

recreate_affine = template_affine
recreate_data = np.zeros(template_shape)

template_csv = '/Users/raphaelagathon/Desktop/PI_nifti/P92_export.csv'
file = open(template_csv, "rb")
try:
    reader = csv.reader(file)

    row = reader.next()
    for row in reader:
        recreate_data[int(float(row[6]))][int(float(row[7]))][int(float(row[8]))] = int(float(row[9]))
finally:

    file.close()


recreate_image = nib.Nifti1Image(recreate_data, recreate_affine)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(recreate_data[162, :, :])

axes[1].imshow(true_image.get_data()[162, :, :])
pylab.show()