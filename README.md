# brainMapper
![alt text](https://github.com/TELECOMNancy/brainMapper/blob/master/UI/ressources/logo.png)

An open source application that aims to automatize treatments to create a brain function atlas - Industrial Project 

## About this project
This is an Industrial Project in collaboration with the Central Hospital of Nancy (France).
Its aim was to create a tool to automatize the image treatment and clustering application on patients' medical data (NIfTI images, brain region-function associations, etc). This would then allow to create a brain function atlas that can be exported and shared in the neurosciences community.

This tool has thus two components :
 - A Python library that ensures all treatments of NIfTI Images and that is the core of this software. It can be used and incorporated into other applications of your making
 - A PyQt interface according to the needs of CHRU neurosurgeons
 
## Authors
This project was designed and developped by :
Version 1 : 
```
Raphael Agathon
Maxime Cluchague
Graziella Husson (@Graziella-Husson)
Valentina Zelaya (@vz-chameleon)
```

Version 2 : 
```
Marie Adler
Aurélien Benoît
Thomas Grassellini
Lucie Martin
```

## Getting Started
### To install on Linux and Mac (Unix-based) :
 - 
 - 
 
### To install on Windows :
 - Install anaconda for windows: https://www.anaconda.com/download/. Tick the option "Add Anaconda to my PATH variable".
 - In a terminal :
```
conda install python=2.7
activate root
conda install -c anaconda pyqt=4.11.4
conda install numpy
conda install scikit-learn
conda install pyqtgraph
conda install pyopengl
conda install -c conda-forge nibabel
```
 - Download the .zip project on the GitHub repository. Decompress it, and create a .bat file (carefull with the extensions in windows, sometime a .txt will be added and you cannot see it.).
 - In the .bat file (This file has to be in the same folder than the decompressed .zip.):
```
cd brainMapper-master/UI
python UI.py
```
 - Create a .bat shortcut on your Desktop.
 
## License

This project is licensed under the GPL-3 License. All other versions of this software should be released under the same license

## Acknowledgments

* Hat tip to Dr Fabien Rech 
