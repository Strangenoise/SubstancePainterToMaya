import maya.cmds as mc
import os
from PySide2 import QtWidgets
import re

class foundMap:

    def __init__(self):

        filePath = ''
        textureName = ''
        mapName = ''
        mapOutput = ''
        shader = ''

def splitTextureName(delimiters, textureName):

    return re.split(delimiters, textureName)

def extractFromNomenclature(ui):
    """
    Check for the naming convention specified in the interface and extract elements
    :return: position of the texture set, separator of the texture set, position of the map, separator of the map
    """

    textureSetPos = mapPos = i = 0

    parts = splitTextureName(ui.DELIMITERS, ui.namingConvention.text())

    for part in parts:
        if part == '$textureSet':
            textureSetPos = i
        elif part == '$map':
            mapPos = i

        i += 1

    return textureSetPos, mapPos, len(parts)

def getMapFromName(mapName, renderer):
    """
    Check if the map name correspond to a known attribute
    :param mapName: The name of the map
    :return: Index of the associated attribute
    """

    for key, value in renderer.renderParameters.MAPS_INDICES.iteritems():
        if mapName in value[0]:
            return value[1]

    return 0

    '''
    elif renderer.name == 'Vray':
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

    elif renderer.name == 'PxrDisney':
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
    '''

def listTextures(ui, renderer, foundFiles):

    foundTextures = []
    mapsFound = []

    texturePath = ui.texturePath.text()

    # Extract elements from naming convention
    textureSetPos, mapPos, partsLen = extractFromNomenclature(ui)

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
                    split = splitTextureName(ui.DELIMITERS, texture)
                    mapName = split[mapPos]
                    textureSetName = split[textureSetPos]
                except:
                    mapName = None
                    textureSetName = None
                    split = ''

                if mapName and textureSetName:

                    if len(split) == partsLen + 1:

                        # If the map name is not already listed (e.i: baseColor)
                        if mapName not in mapsFound:

                            # Create map object
                            map = foundMap()
                            map.textureName = texture
                            map.filePath = filePath
                            map.extension = extension
                            map.textureSet = textureSetName

                            # Get associated attribute name
                            map.indice = getMapFromName(mapName, renderer)
                            map.mapName = mapName
                            map.mapInList = renderer.renderParameters.MAP_LIST[map.indice]

                            # Add map to foundTextures
                            foundTextures.append(map)

    return foundTextures

def populateFoundMaps(ui, renderer, foundTextures):

    layoutPosition = 0
    foundMapsName = []
    uiElements = []

    if foundTextures:
        for foundTexture in foundTextures:

            if foundTexture.mapName not in foundMapsName:

                # Create the layout
                foundMapsSubLayout2 = QtWidgets.QHBoxLayout()
                ui.foundMapsLayout.insertLayout(layoutPosition, foundMapsSubLayout2, stretch=1)

                # Create the widgets
                map1 = QtWidgets.QLineEdit(foundTexture.mapName)
                foundMapsSubLayout2.addWidget(map1)

                map1Menu = QtWidgets.QComboBox()
                map1Menu.addItems(renderer.renderParameters.MAP_LIST)
                map1Menu.setCurrentIndex(foundTexture.indice)
                foundMapsSubLayout2.addWidget(map1Menu)

                # Add ui element to uiElements
                uiElements.append([map1, map1Menu])

                foundMapsName.append(foundTexture.mapName)

                # Increment layout position
                layoutPosition += 1

    else:
        # Create the layout
        foundMapsSubLayout2 = QtWidgets.QHBoxLayout()
        ui.foundMapsLayout.insertLayout(layoutPosition, foundMapsSubLayout2, stretch=1)

        # Create the widgets
        map1 = QtWidgets.QLineEdit('No texture found, \ncheck Texture Folder and Naming Convention')
        foundMapsSubLayout2.addWidget(map1)

    return foundTextures, uiElements


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

def createFileNode(texture):
    """
    Creates a file node and a place2d node, set the texture of the file node and connect both of them
    :param material: The name of the material
    :param mapFound: The name of the texture map
    :param itemPath: The path of the texture map
    :return: Name of the file node
    """

    material = texture.textureSet
    textureName = texture.mapName
    itemPath = texture.filePath

    # Create a file node
    fileNode = mc.shadingNode('file', asTexture=True, isColorManaged=True, name=material + '_' + textureName + '_file')
    # Create a place2d node
    place2d = mc.shadingNode('place2dTexture', asUtility=True, name=material + '_' + textureName + '_place2d')

    # Set the file path of the file node
    mc.setAttr(fileNode + '.fileTextureName', itemPath, type='string')

    # Connect the file and the place2d nodes
    connectPlace2dTexture(place2d, fileNode)

    return fileNode

def connectPlace2dTexture(place2d, fileNode):
    """
    Connect the place2d to the file node
    :param place2d: The name of the place2d node
    :param fileNode: The name of the file node
    :return: None
    """

    # Connections to make
    connections = ['rotateUV', 'offset', 'noiseUV', 'vertexCameraOne', 'vertexUvThree', 'vertexUvTwo',
                   'vertexUvOne', 'repeatUV', 'wrapV', 'wrapU', 'stagger', 'mirrorU', 'mirrorV', 'rotateFrame',
                   'translateFrame', 'coverage']

    # Basic connections
    mc.connectAttr(place2d + '.outUV', fileNode + '.uvCoord')
    mc.connectAttr(place2d + '.outUvFilterSize', fileNode + '.uvFilterSize')

    # Other connections
    for attribute in connections:
        mc.connectAttr(place2d + '.' + attribute, fileNode + '.' + attribute)

def checkCreateMaterial(ui, texture, renderParamters):
    """
        Based on the interface options, create or use existing materials
        :param material: The material's name
        :return: The material's name, if the material was found
        """

    materialNotFound = False
    materialName = texture.textureSet
    materialType = renderParamters.SHADER

    # If create new materials if they doesn't exist, instead use existing ones
    if ui.grpRadioMaterials.checkedId() == -2:

        # If the material doesn't exist or if it's not of the right type
        if not mc.objExists(materialName) or not mc.objectType(materialName) == materialType:

            # If a '_shd' version of the material doesn't exist
            if not mc.objExists(materialName + '_shd'):

                # Create the material
                createMaterialAndShadingGroup(materialName, materialType)

            materialName += '_shd'

    # If create new ones
    elif ui.grpRadioMaterials.checkedId() == -3:

        # If the '_shd' version of the material doesn't exist
        if not mc.objExists(materialName + '_shd'):

            # Create the material
            createMaterialAndShadingGroup(materialName, materialType)

        materialName += '_shd'

    # If use existing ones
    elif ui.grpRadioMaterials.checkedId() == -4:

        # If the material doesn't exist or if it's not of the right type
        if not mc.objExists(materialName) or not mc.objectType(materialName) == materialType:
            # Specify that the material was not found
            materialNotFound = True

    return materialName, materialNotFound

def createMaterialAndShadingGroup(materialName, materialType):
    """
    Create a material and it's shading group
    :param material: The material's name
    :return: The material's name
    """

    # Create the material
    material = createMaterial(materialName, materialType)

    # Create the shading group
    shadingEngine = createShadingGroup(materialName)

    # Connect the material to the shading group
    mc.connectAttr(material + '.outColor', shadingEngine + '.surfaceShader')

    return materialName

def createMaterial(materialName, materialType):

    # Create the material
    material = mc.shadingNode(materialType, asShader=True, name=materialName + '_shd')

    return material

def createShadingGroup( materialName):

    shadingEngineName = materialName.replace('_shd', '_SG')
    shadingEngine = mc.shadingNode('shadingEngine', asPostProcess=True, name=shadingEngineName)

    return shadingEngine

def getTexturesToUse(renderer, foundTextures, uiElements):

    texturesToUse = []

    # Create and connect the textures
    for foundTexture in foundTextures:

        # Connect file node to material
        for uiElement in uiElements:
            if foundTexture.mapName == uiElement[0].text():
                foundTexture.attribute = uiElement[1].currentText()
                foundTexture.indice = uiElement[1].currentIndex()

        if foundTexture.indice in renderer.renderParameters.DONT_USE_IDS:
            foundTextures.remove(foundTexture)
        else:
            if foundTexture.indice in renderer.renderParameters.MAP_LIST_COLOR_ATTRIBUTES_INDICES:
                foundTexture.output = 'outColor'
            else:
                foundTexture.output = 'outColorR'

            texturesToUse.append(foundTexture)

    return texturesToUse

def connectTexture(textureNode, textureOutput, targetNode, targetInput, colorCorrect=False, forceTexture=True):
    """
    Connect the file node to the material
    :param textureNode: Name of the file node
    :param textureOutput: Output attribute of the file node we need to use
    :param targetNode: Name of the material node
    :param targetInput: Input attribute of the material node we need to use
    :return: None
    """

    # If use colorCorrect
    if colorCorrect == True:

        # Create a colorCorrect node
        colorCorrect = mc.shadingNode('colorCorrect', asUtility=True, isColorManaged=True, )

        textureInput = textureOutput.replace('out', 'in')

        # Connect the file node to the color correct
        mc.connectAttr(textureNode + '.' + textureOutput, colorCorrect + '.' + textureInput, force=forceTexture)

        # Connect the color correct to the material
        mc.connectAttr(colorCorrect + '.' + textureOutput, targetNode + '.' + targetInput, force=forceTexture)

    # Connect the file node output to to right material input
    else:
        mc.connectAttr(textureNode + '.' + textureOutput, targetNode + '.' + targetInput, force=forceTexture)


def createDisplacementMap(texture, fileNode, colorCorrect=False, forceTexture=True):
    """
    Connect displacement to the right shading engine(s)
    :param material: The name of the material
    :param forceTexture: Specify if the texture connection is forced
    :param imageNode: The file node to connect
    :return: None
    """

    # Create a displacement node
    displaceNode = mc.shadingNode('displacementShader', asShader=True)

    # Connect the texture to the displacement node
    connectTexture(fileNode, 'outColorR', displaceNode, 'displacement', colorCorrect)

    # Get the shading engine associated with given material
    shadingGroups = mc.listConnections(texture.textureSet + '.outColor')

    for shadingGroup in shadingGroups:

        # Connect the displacement node to all the found shading engines
        mc.connectAttr(displaceNode + '.displacement',
                       shadingGroup + '.displacementShader', force=forceTexture)
