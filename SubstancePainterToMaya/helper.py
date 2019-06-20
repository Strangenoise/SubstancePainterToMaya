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

def before(value, a):
    # Find first part and return slice before it.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    return value[0:pos_a]

def splitNamingConvention(ui, textures):

    construction = []
    textureSetSeparator = '_'
    mapSeparator = '_'
    textureSet = ui.textureSet.text().encode("ascii")
    map = ui.map.text().encode("ascii")

    for texture in textures:

        if textureSet in texture and map in texture:

            beforeTextureSet = re.split(ui.DELIMITERS, before(texture, textureSet))
            beforeMapSet = re.split(ui.DELIMITERS, before(texture, map))
            extension = texture.split('.')[-1]

            if extension in ui.PAINTER_IMAGE_EXTENSIONS:
                textureSplit = re.split(ui.DELIMITERS, texture)

                textureSetSplit = re.split(ui.DELIMITERS, textureSet)
                textureSetSeparator = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]', '', textureSet)

                mapSplit = re.split(ui.DELIMITERS, map)
                mapSeparator = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789]', '', map)



                for i in range(0, len(textureSplit)):
                    if len(beforeTextureSet) <= i+1 <= (len(beforeTextureSet) + len(textureSetSplit))-1:
                        construction.append('textureSet')
                        continue

                    if len(beforeMapSet) <= i+1 <= (len(beforeMapSet) + len(mapSplit))-1:
                        construction.append('map')
                        continue

                    construction.append('part')

                break

    return construction, textureSetSeparator, mapSeparator

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


def listTextures(ui, renderer, foundFiles, allTextureSets):

    foundTextures = []
    mapsFound = []

    # Get the texture path
    texturePath = ui.texturePath.text()

    # Get naming convention elements
    construction, textureSetSeparator, mapSeparator = splitNamingConvention(ui, foundFiles)

    for texture in foundFiles:

        if not allTextureSets:
            if not ui.textureSet.text().encode("ascii") in texture:
                continue

        # Create the texture path
        filePath = os.path.join(texturePath, texture)

        # If item is a file
        if os.path.isfile(filePath):
            # Get item's extension
            extension = texture.split('.')[-1]

            # If its a valid texture file
            if extension in ui.PAINTER_IMAGE_EXTENSIONS:

                textureSet = ''
                name = ''

                textureSetStart = 0
                nameStart = 0

                textureSplit = re.split(ui.DELIMITERS, texture)

                if len(construction) == len(textureSplit):

                    for i in range(0, len(construction)):

                        if construction[i] == 'textureSet':
                            if textureSetStart > 0:
                                textureSet += textureSetSeparator[textureSetStart - 1]
                            textureSet += textureSplit[i]
                            textureSetStart += 1

                        if construction[i] == 'map':
                            if nameStart > 0:
                                name += mapSeparator[nameStart - 1]
                            name += textureSplit[i]
                            nameStart += 1

                mapName = name
                textureSetName = textureSet

                if mapName and textureSetName:

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
                ui.foundMapsLayout.insertLayout(-1, foundMapsSubLayout2, stretch=1)

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
    ui.scroll.setVisible(True)

    if renderer.name == 'Arnold':
        # Arnold subdivisions
        ui.checkbox5 = QtWidgets.QCheckBox('Add subdivisions')
        ui.optionsSubLayout2.addWidget(ui.checkbox5)
        ui.checkbox5.stateChanged.connect(lambda: ui.addArnoldSubdivisionsCheckbox())

        ui.subdivTypeTitle = QtWidgets.QLabel('Type')
        ui.optionsSubLayout2.addWidget(ui.subdivTypeTitle)

        ui.subdivType = QtWidgets.QComboBox()
        ui.subdivType.addItems(['catclark', 'linear'])
        ui.subdivType.setEnabled(False)
        ui.optionsSubLayout2.addWidget(ui.subdivType)

        ui.subdivIterTitle = QtWidgets.QLabel('Iterations')
        ui.optionsSubLayout2.addWidget(ui.subdivIterTitle)

        ui.subdivIter = QtWidgets.QLineEdit('1')
        ui.subdivIter.setEnabled(False)
        ui.optionsSubLayout2.addWidget(ui.subdivIter)

    elif renderer.name == 'Vray':
        # Vray subdivisions
        ui.checkbox6 = QtWidgets.QCheckBox('Add subdivisions')
        ui.optionsSubLayout2.addWidget(ui.checkbox6)
        ui.checkbox6.stateChanged.connect(lambda: ui.addVraySubdivisionsCheckbox())

        ui.subdivIterVrayTitle = QtWidgets.QLabel('Edge Length')
        ui.optionsSubLayout2.addWidget(ui.subdivIterVrayTitle)

        ui.subdivIterVray = QtWidgets.QLineEdit('4')
        ui.subdivIterVray.setEnabled(False)
        ui.optionsSubLayout2.addWidget(ui.subdivIterVray)

        ui.subdivMaxVrayTitle = QtWidgets.QLabel('Max Subdivs')
        ui.optionsSubLayout2.addWidget(ui.subdivMaxVrayTitle)

        ui.maxSubdivIterVray = QtWidgets.QLineEdit('4')
        ui.maxSubdivIterVray.setEnabled(False)
        ui.optionsSubLayout2.addWidget(ui.maxSubdivIterVray)

    elif renderer.name == 'PxrSurface' or renderer.name == 'PxrDisney':
        # Renderman Subdivisions
        ui.checkbox7 = QtWidgets.QCheckBox('Add subdivisions')
        ui.optionsSubLayout2.addWidget(ui.checkbox7)
        ui.checkbox7.stateChanged.connect(lambda: ui.addRendermanSubdivisionsCheckbox())

        ui.subdivIterRendermanTitle = QtWidgets.QLabel('scheme')
        ui.optionsSubLayout2.addWidget(ui.subdivIterRendermanTitle)

        ui.subdivIterRenderman = QtWidgets.QComboBox()
        ui.subdivIterRenderman.addItems(['Catmull', 'Loop', 'Bilinear'])
        ui.subdivIterRenderman.setEnabled(False)
        ui.optionsSubLayout2.addWidget(ui.subdivIterRenderman)

        ui.subdivInterRendermanTitle = QtWidgets.QLabel('Interpolation')
        ui.optionsSubLayout2.addWidget(ui.subdivInterRendermanTitle)

        ui.subdivInterRenderman = QtWidgets.QComboBox()
        ui.subdivInterRenderman.addItems(['No', 'Sharp creases and corners', 'Sharp creases'])
        ui.subdivInterRenderman.setEnabled(False)
        ui.optionsSubLayout2.addWidget(ui.subdivInterRenderman)

    elif renderer.name == 'Redshift':
        # Renderman Subdivisions
        ui.checkbox8 = QtWidgets.QCheckBox('Add subdivisions')
        ui.optionsSubLayout2.addWidget(ui.checkbox8)
        ui.checkbox8.stateChanged.connect(lambda: ui.addRedshiftSubdivisionsCheckbox())

        ui.subdivIterRedshiftTitle = QtWidgets.QLabel('scheme')
        ui.optionsSubLayout2.addWidget(ui.subdivIterRedshiftTitle)

        ui.subdivIterRedshift = QtWidgets.QComboBox()
        ui.subdivIterRedshift.addItems(['Cat + Loop', 'Cat'])
        ui.subdivIterRedshift.setEnabled(False)
        ui.optionsSubLayout2.addWidget(ui.subdivIterRedshift)

        ui.subdivMinTitle = QtWidgets.QLabel('Min Edge Length')
        ui.optionsSubLayout2.addWidget(ui.subdivMinTitle)

        ui.subdivMin = QtWidgets.QLineEdit('4.00')
        ui.subdivMin.setEnabled(False)
        ui.optionsSubLayout2.addWidget(ui.subdivMin)

        ui.subdivMaxTitle = QtWidgets.QLabel('Max Subdivs')
        ui.optionsSubLayout2.addWidget(ui.subdivMaxTitle)

        ui.subdivMax = QtWidgets.QLineEdit('6')
        ui.subdivMax.setEnabled(False)
        ui.optionsSubLayout2.addWidget(ui.subdivMax)

    if renderer.name == 'Stingray':
        ui.checkbox1.setVisible(False)
        ui.checkbox2.setVisible(False)
        ui.checkbox4.setVisible(False)
        ui.checkbox1.setChecked(False)
        ui.checkbox2.setChecked(False)
        ui.checkbox4.setChecked(False)

    else:
        ui.checkbox1.setVisible(True)
        ui.checkbox2.setVisible(True)
        ui.checkbox4.setVisible(True)


    ui.grpProceed.setVisible(True)
    ui.launchButton.setText('Re-launch')

    return ui

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

def createFileNode(texture, UDIMS):
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

    if UDIMS:
        mc.setAttr(fileNode + '.uvTilingMode', 3)

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

def checkCreateMaterial(ui, texture, renderer):
    """
        Based on the interface options, create or use existing materials
        :param material: The material's name
        :return: The material's name, if the material was found
        """

    materialNotFound = False
    materialName = texture.textureSet
    materialType = renderer.renderParameters.SHADER

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

    mc.select(materialName)

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
    shadingEngine = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name=shadingEngineName)

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
            continue

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

    shadingGroups = None

    # Create a displacement node
    displaceNode = mc.shadingNode('displacementShader', asShader=True)

    # Connect the texture to the displacement node
    connectTexture(fileNode, 'outColorR', displaceNode, 'displacement', colorCorrect)

    # Get the shading engine associated with given material
    shadingGroups = mc.listConnections(texture.textureSet + '.outColor')

    for shadingGroup in shadingGroups:

        if mc.objectType(shadingGroup) == 'shadingEngine':
            # Connect the displacement node to all the found shading engines
            mc.connectAttr(displaceNode + '.displacement',
                           shadingGroup + '.displacementShader', force=forceTexture)
