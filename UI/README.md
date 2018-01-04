## brainMapper's User Interface

This user interface was delevelopped with PyQt4

### Depedencies
    - PyQt4


### Resources (Icons, images...)
To be able to make this a standalone app, we used a .qrc file named 'resources.qrc', containing the path to ui's resources :
```
<RCC>
  <qresource prefix="/">
    <file>ressources/logo.png</file>
    <file>ressources/help.png</file>
    <file>ressources/error.png</file>
  </qresource>

  <qresource prefix="/">
    <file>ressources/app_icons_png/writing.png</file>
    <file>ressources/app_icons_png/libreoffice.png</file>
    <file>ressources/app_icons_png/square.png</file>
    <file>ressources/app_icons_png/play.png</file>
    <file>ressources/app_icons_png/home-2.png</file>
    <file>ressources/app_icons_png/calculator.png</file>
    <file>ressources/app_icons_png/checking.png</file>
  </qresource>
</RCC>
```

To use them in the code, you must first use pyrcc4 to compile the .qrc file into a .py module that will be imported in the code

Each time you add a resource, you have to recompile the .qrc file

```
pyrcc4 -o resources.py resources.qrc
```

pyrcc4 usually comes with the standard PyQt4 library, but for some distributions, you will have to install the PyQt4-devel package

Once you have compiled resources.py with pyrcc4, to use resources such as icons in the code import resources.py and then access the images with
the following syntax :
```
#HEADER
import resources.py

# .....
editButton.setIcon(QtGui.QIcon(':ressources/app_icons_png/writing.png'))
```

### Compile as standalone app

Use pyinstaller



