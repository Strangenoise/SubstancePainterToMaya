import maya.cmds as mc
import helper
reload(helper)

def addSubdivisions(ui, texture):
    """
    Add render subdivisions of a certain type
    :param material: The material used to find which shapes to subdivide
    :return: None
    """

    material = texture.textureSet

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

def createNormalMap(texture, renderer, fileNode, colorCorrect, forceTexture=True):
    """
    Connect the normal map with the right nodes, even if a bump already exists
    :param material: The name of the material
    :param attributeName: The name of the material attribute to use
    :param forceTexture: Specify if the texture connection is forced
    :param imageNode: The file node to connect
    :return: None
    """

    normalNode = renderer.renderParameters.NORMAL_NODE
    bumpNode = renderer.renderParameters.BUMP_NODE
    material = texture.textureSet
    attributeName = texture.materialAttribute

    # Create the normal utility
    normalNode = mc.shadingNode(normalNode, asUtility=True)

    # Connect the file node to the normal utility node
    helper.connectTexture(fileNode, 'outColor', normalNode, 'input', colorCorrect)

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

def createBumpMap(texture, renderer, fileNode, colorCorrect, forceTexture=True):
    """
    Connect the bump map with the right nodes, even if a normal map already exists
    :param material: The name of the material
    :param attributeName: The name of the material attribute to use
    :param forceTexture: Specify if the texture connection is forced
    :param imageNode: The file node to connect
    :return: None
    """

    normalNode = renderer.renderParameters.NORMAL_NODE
    bumpNode = renderer.renderParameters.BUMP_NODE
    material = texture.textureSet
    attributeName = texture.materialAttribute

    # Create the bump utility node
    bumpNode = mc.shadingNode(bumpNode, asUtility=True)

    # Connect the file node to the bump utility node
    helper.connectTexture(fileNode, 'outColorR', bumpNode, 'bumpMap', colorCorrect)

    # List all the connection in the material attribute
    connectedNodes = mc.listConnections(material + '.' + attributeName)

    # If there's connections
    if connectedNodes:

        for node in connectedNodes:

            # If it's a normal utility node
            if mc.objectType(node) == normalNode:

                # Connect the normal utility node to to bump utility
                mc.connectAttr(node + '.outValue', bumpNode + '.normal',
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

def connect(ui, texture, renderer, fileNode):

    colorCorrect = ui.checkbox4.isChecked()
    useBump = ui.checkbox1.isChecked()
    useDisplace = ui.checkbox2.isChecked()

    # Change file node parameters to Raw and add alphaIsLuminance
    if texture.materialAttribute is not 'baseColor':
        try:
            mc.setAttr(fileNode + '.colorSpace', 'Raw', type='string')
        except:
            pass
        mc.setAttr(fileNode + '.alphaIsLuminance', True)

    # If height or normalMap
    if texture.materialAttribute == 'normalCamera':

        # If height
        if texture.output == 'outColorR':

            # If bump
            if useBump:
                createBumpMap(texture, renderer, fileNode, colorCorrect)

            # If displace
            if useDisplace:
                helper.createDisplacementMap(texture, fileNode, colorCorrect)

        # If normalMap
        elif texture.output == 'outColor':

            createNormalMap(texture, renderer, fileNode, colorCorrect)

    # If it's another type of map
    else:
        helper.connectTexture(fileNode, texture.output, texture.textureSet, texture.materialAttribute, colorCorrect)