import maya.cmds as mc
import os
from PySide2 import QtWidgets

class foundMap:

    def __init__(self):

        filePath = ''
        textureName = ''
        mapName = ''
        mapOutput = ''
        shader = ''


def extractFromNomenclature(ui):
    """
    Check for the naming convention specified in the interface and extract elements
    :return: position of the texture set, separator of the texture set, position of the map, separator of the map
    """

    textureSetPos = mapPos = 0
    textureSetSeparator = mapPosSeparator = '_'

    # For each delimiter
    for delimiter in ui.DELIMITERS:

        # Split the specified naming convention
        parts = ui.namingConvention.text().split(delimiter)

        # If there's a split
        if len(parts) > 1:

            # For each split
            for i in range(0, len(parts)):

                # If the split is <textureSet>
                if parts[i] == '$textureSet':
                    textureSetPos = i
                    textureSetSeparator = delimiter

                # Elif the split is <map>
                elif parts[i] == '$map':
                    mapPos = i
                    mapPosSeparator = delimiter

    return textureSetPos, textureSetSeparator, mapPos, mapPosSeparator

def getMapFromName(mapName, renderer):
    """
    Check if the map name correspond to a known attribute
    :param mapName: The name of the map
    :return: Index of the associated attribute
    """

    # Check for the render engine and load config file
    if renderer.renderer == 'Arnold':
        if mapName in renderer.baseColor:
            return 1
        elif mapName in renderer.height:
            return 2
        elif mapName in renderer.metalness:
            return 3
        elif mapName in renderer.normal:
            return 4
        elif mapName in renderer.roughness:
            return 5
        elif mapName in renderer.matte:
            return 54
        elif mapName in renderer.opacity:
            return 49
        elif mapName in renderer.subsurface:
            return 28
        elif mapName in renderer.emission:
            return 44
        else:
            return 0

    elif renderer.renderer == 'Vray':
        if mapName in renderer.baseColor:
            return 1
        elif mapName in renderer.height:
            return 2
        elif mapName in renderer.metalness:
            return 3
        elif mapName in renderer.normal:
            return 5
        elif mapName in renderer.roughness:
            return 4
        elif mapName in renderer.opacity:
            return 10
        elif mapName in renderer.subsurface:
            return 35
        else:
            return 0

    elif renderer.renderer == 'PxrDisney':
        if mapName in renderer.baseColor:
            return 1
        elif mapName in renderer.height:
            return 15
        elif mapName in renderer.metalness:
            return 5
        elif mapName in renderer.normal:
            return 15
        elif mapName in renderer.roughness:
            return 8
        elif mapName in renderer.subsurface:
            return 4
        else:
            return 0

    elif renderer.renderer == 'PxrSurface':
        if mapName in renderer.baseColor:
            return 1
        elif mapName in renderer.height:
            return 2
        elif mapName in renderer.metalness:
            return 4
        elif mapName in renderer.normal:
            return 3
        elif mapName in renderer.roughness:
            return 5
        elif mapName in renderer.opacity:
            return 87
        elif mapName in renderer.subsurface:
            return 61
        else:
            return 0

def listTextures(ui, foundFiles):

    foundTextures = []
    mapsFound = []

    texturePath = ui.texturePath.text()

    # Extract elements from naming convention
    textureSetPos, textureSetSeparator, mapPos, mapPosSeparator = extractFromNomenclature(ui)

    for texture in foundFiles:

        # Create the texture path
        filePath = os.path.join(texturePath, texture)

        # If item is a file
        if os.path.isfile(filePath):
            # Get item's extension
            extension = texture.split('.')[1]

            # If its a valid texture file
            if extension in ui.PAINTER_IMAGE_EXTENSIONS:

                # Get map's name from texture's name
                try:
                    mapName = texture.split(mapPosSeparator)[mapPos].split('.')[0]
                except:
                    mapName = None

                if mapName:

                    # If the map name is not already listed (e.i: baseColor)
                    if mapName not in mapsFound:

                        # Create map object
                        map = foundMap()
                        map.textureName = texture
                        map.filePath = filePath
                        map.extension = extension

                        # Get associated attribute name
                        map.mapName = getMapFromName(mapName)

                        # Add map to foundTextures
                        foundTextures.append(map)

    return foundTextures

def populateFoundMaps(ui, renderer, foundTextures):

    layoutPosition = 0

    if foundTextures:
        for foundTexture in foundTextures:

            # Create the layout
            foundMapsSubLayout2 = QtWidgets.QHBoxLayout()
            ui.foundMapsLayout.insertLayout(layoutPosition, foundMapsSubLayout2, stretch=1)

            # Create the widgets
            map1 = QtWidgets.QLineEdit(foundTexture.textureName)
            foundMapsSubLayout2.addWidget(map1)

            map1Menu = QtWidgets.QComboBox()
            map1Menu.addItems(renderer.mapsList)
            map1Menu.setCurrentIndex(foundTexture.mapName)
            foundMapsSubLayout2.addWidget(map1Menu)

            # Add ui element to map
            foundTexture.lineText = map1
            foundTexture.comboBox = map1Menu

            # Increment layout position
            layoutPosition += 1

    else:
        # Create the layout
        foundMapsSubLayout2 = QtWidgets.QHBoxLayout()
        ui.foundMapsLayout.insertLayout(layoutPosition, foundMapsSubLayout2, stretch=1)

        # Create the widgets
        map1 = QtWidgets.QLineEdit('No texture found, \ncheck Texture Folder and Naming Convention')
        foundMapsSubLayout2.addWidget(map1)

def displaySecondPartOfUI(ui, renderer):

    # Display second part of the interface
    ui.grpFoundMaps.setVisible(True)
    ui.grpOptions.setVisible(True)

    arnoldUIElements = ui.arnoldUIElements
    vrayUIElements = ui.vrayUIElements
    rendermanUIElements = ui.rendermanUIElements

    if renderer.name == 'Arnold':
        for item in vrayUIElements:
            item.setVisible(False)

        for item in rendermanUIElements:
            item.setVisible(False)

        for item in arnoldUIElements:
            item.setVisible(True)

    elif renderer.name == 'Vray':
        for item in arnoldUIElements:
            item.setVisible(False)

        for item in rendermanUIElements:
            item.setVisible(False)

        for item in vrayUIElements:
            item.setVisible(True)

    elif renderer.name == 'PxrSurface' or renderer.name == 'PxrDisney':
        for item in arnoldUIElements:
            item.setVisible(False)

        for item in vrayUIElements:
            item.setVisible(False)

        for item in rendermanUIElements:
            item.setVisible(True)

    ui.grpProceed.setVisible(True)
    ui.launchButton.setText('Re-launch')

def clearLayout(layout):
    """
    Empty specified pySide2 layout
    :param layout: Layout to clear
    :return: None
    """

    if layout is not None:
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                clearLayout(item.layout())