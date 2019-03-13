import maya.cmds as mc
import os
from PySide2 import QtCore
from PySide2 import QtWidgets


class foundMap:

    def __init__(self):

        filePath = ''
        textureName = ''
        mapName = ''
        mapOutput = ''
        shader = ''


def createFileNode(material, mapFound, itemPath):
    """
    Creates a file node and a place2d node, set the texture of the file node and connect both of them
    :param material: The name of the material
    :param mapFound: The name of the texture map
    :param itemPath: The path of the texture map
    :return: Name of the file node
    """

    # Create a file node
    fileNode = mc.shadingNode('file', asTexture=True, isColorManaged=True, name=material + '_' + mapFound + '_file')
    # Create a place2d node
    place2d = mc.shadingNode('place2dTexture', asUtility=True, name=material + '_' + mapFound + '_place2d')

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

def connectColorManagement(fileNode):
    """
    Add color correct management to a file node
    :param fileNode: The file node's name
    :return: None
    """

    mc.connectAttr('defaultColorMgtGlobals.cmEnabled', fileNode + '.colorManagementEnabled')
    mc.connectAttr('defaultColorMgtGlobals.configFileEnabled', fileNode + '.colorManagementConfigFileEnabled')
    mc.connectAttr('defaultColorMgtGlobals.configFilePath', fileNode + '.colorManagementConfigFilePath')
    mc.connectAttr('defaultColorMgtGlobals.workingSpaceName', fileNode + '.workingSpace')

def connectTexture(textureNode, textureOutput, targetNode, targetInput, colorCorrect=False):
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
        mc.connectAttr(textureNode + textureOutput, colorCorrect + textureInput, force=True)

        # Connect the color correct to the material
        mc.connectAttr(colorCorrect + textureOutput, targetNode + targetInput, force=True)

    # Connect the file node output to to right material input
    else:
        mc.connectAttr(textureNode + textureOutput, targetNode + targetInput, force=True)


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



def createMaterial(material, materialToUse):

    # Create the material
    material = mc.shadingNode(materialToUse, asShader=True, name=material + '_shd')

    return material

def createShadingGroup( material):

    shadingEngineName = material.replace('_shd', '_SG')
    shadingEngine = mc.shadingNode('shadingEngine', asPostProcess=True, name=shadingEngineName)

    return shadingEngine

def connect(material, mapFound, itemPath, attributeName, attributeIndex, forceTexture, renderer, ui):

    # Check for the render engine and load config file
    if renderer.renderer == 'Arnold':
        import helper_arnold as helper
        reload(helper)

    elif renderer.renderer == 'Vray':
        import helper_vray as helper
        reload(helper)

    elif renderer.renderer == 'PxrDisney' or renderer.renderer == 'PxrSurface':
        import helper_renderman as helper
        reload(helper)


def createMaterialAndShadingGroup(material, renderer):
    """
    Create a material and it's shading group
    :param material: The material's name
    :return: The material's name
    """

    # Create the material
    material = createMaterial(material, renderer.shaderToUse)

    # Create the shading group
    shadingEngine = createShadingGroup(material)

    # Connect the material to the shading group
    mc.connectAttr(material + '.outColor', shadingEngine + '.surfaceShader')

    return material

def checkOrCreateMaterial(material, ui, renderer):
    """
    Based on the interface options, create or use existing materials
    :param material: The material's name
    :return: The material's name, if the material was found
    """

    materialNotFound = False

    # If create new materials if they doesn't exist, instead use existing ones
    if ui.grpRadioMaterials.checkedId() == -2:

        # If the material doesn't exist or if it's not of the right type
        if not mc.objExists(material) or not mc.objectType(material) == renderer.shaderToUse:

            # If a '_shd' version of the material doesn't exist
            if not mc.objExists(material + '_shd'):

                # Create the material
                material = createMaterialAndShadingGroup(material)

            else:

                # Or add '_shd' at the name of the material
                material += '_shd'

    # If create new ones
    elif ui.grpRadioMaterials.checkedId() == -3:

        # If the '_shd' version of the material doesn't exist
        if not mc.objExists(material + '_shd'):

            # Create the material
            material = createMaterialAndShadingGroup(material)

        else:

            # Or add '_shd' at the name of the material
            material += '_shd'

    # If use existing ones
    elif ui.grpRadioMaterials.checkedId() == -4:

        # If the material doesn't exist or if it's not of the right type
        if not mc.objExists(material) or not mc.objectType(material) == renderer.shaderToUse:
            # Specify that the material was not found
            materialNotFound = True

    return material, materialNotFound

def getMaterialFromName( name):
    """
    Get material's name from texture's name
    :param name: Name of the texture
    :return: The name of the material
    """

    # Extract from naming convention
    textureSetPos, textureSetSeparator, mapPos, mapPosSeparator = extractFromNomenclature()

    # Get the name from naming convention
    materialName = name.split(textureSetSeparator)[textureSetPos].split('.')[0]

    return materialName

def getShaderAttributeFromMapName(mapName, renderer):
    """
    From the map name, find the right material attribute to use
    :param mapName: The texture map's name
    :return: The name of the material attribute, the index of the material attribute
    """

    # For all the maps found elements
    for element in renderer.mapsFoundElements:

        # If the name of the element matches the texture's name
        if element[0].text() == mapName:
            # Get the attribute name and exist the loop
            attrName = renderer.mapsListRealAttributes[element[1].currentIndex()]
            break

    return attrName, element[1].currentIndex()



def populateFoundMaps(ui, renderer):
    """
    For all the texture files in the texture folder, create widgets in Found Maps part of the interface
    :return: None
    """

    mapsFound = []
    allTextures = []

    # Extract elements from naming convention
    textureSetPos, textureSetSeparator, mapPos, mapPosSeparator = extractFromNomenclature(ui)

    layoutPosition = 0

    for item in textureContent:

        # Create the texture path
        filePath = os.path.join(texturePath, item)

        # If item is a file
        if os.path.isfile(filePath):

            # Get item's extension
            extension = item.split('.')[1]

            # If its a valid texture file
            if extension in ui.PAINTER_IMAGE_EXTENSIONS:

                # Add item to all textures
                allTextures.append(item)

                # Get map's name from texture's name
                try:
                    mapName = item.split(mapPosSeparator)[mapPos].split('.')[0]
                except:
                    mapName = None


        '''

    # return mapsFound