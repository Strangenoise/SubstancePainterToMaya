import maya.cmds as mc
import helper
reload(helper)

def addArnoldSubdivisions(material, ui):
    """
    Add render subdivisions of a certain type
    :param material: The material used to find which shapes to subdivide
    :return: None
    """

    # Get values from interface
    subdivType = ui.subdivType.currentIndex() + 1
    iterations = ui.subdivIter.text()

    # Find the shapes connected to the material
    shader = mc.listConnections(material + '.outColor', d=True)[0]
    meshes = mc.listConnections(shader, type='mesh')

    if meshes:

        # For all shapes add the render subdivisions
        for mesh in meshes:
            mc.setAttr(mesh + '.aiSubdivType', subdivType)
            mc.setAttr(mesh + '.aiSubdivIterations', int(iterations))

def createArnoldNormalMap(material, attributeName, forceTexture, imageNode, normalNode, bumpNode, colorCorrect):
    """
    Connect the normal map with the right nodes, even if a bump already exists
    :param material: The name of the material
    :param attributeName: The name of the material attribute to use
    :param forceTexture: Specify if the texture connection is forced
    :param imageNode: The file node to connect
    :return: None
    """

    # Create the normal utility
    normalNode = mc.shadingNode(normalNode, asUtility=True)

    # Connect the file node to the normal utility node
    helper.connectTexture(imageNode, '.outColor', normalNode, '.input', colorCorrect)

    # List the connections in the material input attribute
    connectedNodes = mc.listConnections(material + '.' + attributeName)

    # If there's connected nodes
    if connectedNodes:

        for node in connectedNodes:

            # If this is already a normal utility node
            if mc.objectType(node) == normalNode:

                # Connect the new utility instead if forceTexture is true
                mc.connectAttr(normalNode + '.outValue', material + '.' + attributeName,
                               force=forceTexture)

            # If it's a bump node
            elif mc.objectType(node) == bumpNode:

                # Get the input file of the bump node
                connectedBumpNodes = mc.listConnections(node + '.bumpMap')
                for connectedBumpNode in connectedBumpNodes:

                    # If it's a colorCorrect or a file node with '_file' in it's name
                    if '_file' in connectedBumpNode or 'colorCorrect' in connectedBumpNode:

                        # Connect the utility node in the bump node
                        mc.connectAttr(normalNode + '.outValue', node + '.normal',
                                       force=forceTexture)

                    else:

                        # Instead replace the bump node by the normal utility node
                        mc.connectAttr(normalNode + '.outValue', material + '.' + attributeName,
                                       force=forceTexture)

    # If there's no connections in the material attribute
    else:

        # Connect the normal utility to the material attribute
        mc.connectAttr(normalNode + '.outValue', material + '.' + attributeName,
                       force=forceTexture)

def createArnoldBumpMap(material, attributeName, forceTexture, imageNode, normalNode, bumpNode, colorCorrect):
    """
    Connect the bump map with the right nodes, even if a normal map already exists
    :param material: The name of the material
    :param attributeName: The name of the material attribute to use
    :param forceTexture: Specify if the texture connection is forced
    :param imageNode: The file node to connect
    :return: None
    """

    # Create the bump utility node
    bumpNode = mc.shadingNode(bumpNode, asUtility=True)

    # Connect the file node to the bump utility node
    helper.connectTexture(imageNode, '.outColorR', bumpNode, '.bumpMap', colorCorrect)

    # List all the connection in the material attribute
    connectedNodes = mc.listConnections(material + '.' + attributeName)

    # If there's connections
    if connectedNodes:

        for node in connectedNodes:

            # If it's a normal utility node
            if mc.objectType(node) == normalNode:

                # Connect the normal utility node to to bump utility
                mc.connectAttr(node + '.outValue', material + '.normal',
                               force=forceTexture)

                # Connect the bump node to the material attribute
                mc.connectAttr(bumpNode + '.outValue', material + '.' + attributeName,
                               force=forceTexture)

            # If it's not a normal utility node
            else:

                # Replace the connection by the bump node if the force texture is true
                mc.connectAttr(bumpNode + '.outValue', material + '.' + attributeName,
                               force=forceTexture)

    # If there's not connections
    else:

        # Connect the bump utility to the material attribute
        mc.connectAttr(bumpNode + '.outValue', material + '.' + attributeName,
                       force=forceTexture)

def connect(material, mapFound, itemPath, attributeName, attributeIndex, forceTexture, ui, launcher):
    # Add subdivisions
    if ui.checkbox5.isChecked():
        addArnoldSubdivisions(material, ui)

    # Create file node
    imageNode = helper.createFileNode(material, mapFound, itemPath)

    # Change file node parameters to Raw and add alphaIsLuminance
    if attributeName is not 'baseColor':
        try:
            mc.setAttr(imageNode + '.colorSpace', 'Raw', type='string')
        except:
            pass
        mc.setAttr(imageNode + '.alphaIsLuminance', True)

    # Specify the output attribute to use for the file nodes
    if attributeIndex in launcher.mapsListColorAttributesIndices:
        outputAttr = 'outColor'
    else:
        outputAttr = 'outColorR'

    # If height
    if attributeName == 'normalCamera' and outputAttr == 'outColorR':

        # If bump
        if ui.checkbox1.isChecked():
            createArnoldBumpMap(material, attributeName, forceTexture, imageNode, launcher.normalNode, launcher.bumpNode, ui.checkbox4.isChecked())

        # If displace
        if ui.checkbox2.isChecked():
            helper.createDisplacementMap(material, forceTexture, imageNode, ui.checkbox4.isChecked())

    # If normalMap
    elif attributeName == 'normalCamera' and outputAttr == 'outColor':

        createArnoldNormalMap(material, attributeName, forceTexture, imageNode, launcher.normalNode, launcher.bumpNode, ui.checkbox4.isChecked())

    # If it's another type of map
    else:
        helper.connectTexture(imageNode, '.' + outputAttr, material, '.' + attributeName, ui.checkbox4.isChecked())