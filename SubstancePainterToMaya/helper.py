import maya.cmds as mc

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

def createDisplacementMap(material, forceTexture, imageNode, colorCorrect=False):
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
    connectTexture(imageNode, '.outColorR', displaceNode, '.displacement', colorCorrect)

    # Get the shading engine associated with given material
    shadingGroups = mc.listConnections(material + '.outColor')

    for shadingGroup in shadingGroups:

        # Connect the displacement node to all the found shading engines
        mc.connectAttr(displaceNode + '.displacement',
                       shadingGroup + '.displacementShader', force=forceTexture)