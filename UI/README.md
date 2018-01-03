## brainMapper's User Interface

This user interface was delevelopped with PyQt4

### Depedencies
    - PyQt4


### Resources (Icons, images...)
To be able to make this a standalone app, we used a .qrc file named 'resources.qrc', containing the path to ui's resources
To use them in the code, you must first use pyrcc4 to compile the .qrc file into a .py module that will be imported in the code.

Each time you add a resource, you have to recompile the .qrc file

```
pyrcc4 -o resources.py resources.qrc

```

pyrcc4 usually comes with the standard PyQt4 library, but for some distributions, you will have to install the PyQt4-devel package

### Compile as standalone app

Use pyinstaller



