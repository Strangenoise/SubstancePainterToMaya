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
    subdivType = ui.subdivIterRedshift.currentIndex() + 1
    min = ui.subdivMin.text()
    max = ui.subdivMax.text()

    # Find the shapes connected to the material
    shader = mc.listConnections(material + '.outColor', d=True)[0]
    meshes = mc.listConnections(shader, type='mesh')

    if meshes:

        # For all shapes add the render subdivisions
        for mesh in meshes:
            mc.setAttr(mesh + '.rsEnableSubdivision', 1)
            mc.setAttr(mesh + '.rsMinTessellationLength', float(min))
            mc.setAttr(mesh + '.rsMaxTessellationSubdivs', int(max))

def createDisplacementMap(texture, renderer, fileNode, colorCorrect, forceTexture=True):

    print('displacement')

    shadingGroups = None
    displacementNode = renderer.renderParameters.DISPLACE_NODE

    # Create a displacement node
    displaceNode = mc.shadingNode(displacementNode, asShader=True)

    # Connect the texture to the displacement node
    connectTexture(fileNode, 'outColor', displaceNode, 'texMap', colorCorrect)

    # Get the shading engine associated with given material
    shadingGroups = mc.listConnections(texture.textureSet + '.outColor')

    for shadingGroup in shadingGroups:

        if mc.objectType(shadingGroup) == 'shadingEngine':
            # Connect the displacement node to all the found shading engines
            mc.connectAttr(displaceNode + '.out',
                           shadingGroup + '.rsDisplacementShader', force=forceTexture)

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
    connectTexture(fileNode, 'outColor', normalNode, 'input', colorCorrect)
    mc.setAttr(normalNode + '.inputType', 1)

    # List the connections in the material input attribute
    connectedNodes = mc.listConnections(material + '.' + attributeName)

    # If there's connected nodes
    if connectedNodes:

        for node in connectedNodes:

            print(node)

            if mc.objectType(node) == bumpNode:

                # If it's a bump node
                if mc.getAttr(node + '.inputType') == 0:

                    # Get the input file of the bump node
                    connectedBumpNodes = mc.listConnections(node + '.input')
                    for connectedBumpNode in connectedBumpNodes:

                        print connectedBumpNode

                        # If it's a colorCorrect or a file node with '_file' in it's name
                        if '_file' in connectedBumpNode or 'ColorCorrection' in connectedBumpNode:

                            # Create a bump blender
                            bumpBlend = mc.shadingNode('RedshiftBumpBlender', asTexture=True)

                            # Connect the bump node to the bump blender
                            mc.connectAttr(node + '.out', bumpBlend + '.baseInput',
                                           force=forceTexture)

                            # Connect the normal node to the bump blender
                            mc.connectAttr(normalNode + '.out', bumpBlend + '.bumpInput0',
                                           force=forceTexture)

                            # Connect the bump blender to the material
                            mc.connectAttr(bumpBlend + '.outColor', material + '.' + attributeName,
                                           force=forceTexture)

                        else:

                            # Instead replace the bump node by the normal utility node
                            mc.connectAttr(normalNode + '.out', material + '.' + attributeName,
                                           force=forceTexture)

                else:

                    # Connect the normal utility to the material attribute
                    mc.connectAttr(normalNode + '.out', material + '.' + attributeName,
                                   force=forceTexture)

            else:

                # Connect the normal utility to the material attribute
                mc.connectAttr(normalNode + '.out', material + '.' + attributeName,
                               force=forceTexture)

    # If there's no connections in the material attribute
    else:

        # Connect the normal utility to the material attribute
        mc.connectAttr(normalNode + '.out', material + '.' + attributeName,
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
    print('bump')
    normalNode = renderer.renderParameters.NORMAL_NODE
    bumpNode = renderer.renderParameters.BUMP_NODE
    material = texture.textureSet
    attributeName = texture.materialAttribute

    # Create the normal utility
    bumpNode = mc.shadingNode(bumpNode, asUtility=True)

    # Connect the file node to the normal utility node
    connectTexture(fileNode, 'outColor', bumpNode, 'input', colorCorrect)
    mc.setAttr(bumpNode + '.inputType', 0)

    # List the connections in the material input attribute
    connectedNodes = mc.listConnections(material + '.' + attributeName)

    # If there's connected nodes
    if connectedNodes:

        for node in connectedNodes:

            if mc.objectType(node) == bumpNode:

                # If it's a normal node
                if not mc.getAttr(node + '.inputType') == 0:

                    # Get the input file of the bump node
                    connectedBumpNodes = mc.listConnections(node + '.input')
                    for connectedBumpNode in connectedBumpNodes:

                        # If it's a colorCorrect or a file node with '_file' in it's name
                        if '_file' in connectedBumpNode or 'ColorCorrection' in connectedBumpNode:

                            # Create a bump blender
                            bumpBlend = mc.shadingNode('RedshiftBumpBlender', asTexture=True)

                            # Connect the bump node to the bump blender
                            mc.connectAttr(node + '.out', bumpBlend + '.baseInput',
                                           force=forceTexture)

                            # Connect the normal node to the bump blender
                            mc.connectAttr(bumpNode + '.out', bumpBlend + '.bumpInput0',
                                           force=forceTexture)

                            # Connect the bump blender to the material
                            mc.connectAttr(bumpBlend + '.outColor', material + '.' + attributeName,
                                           force=forceTexture)

                        else:

                            # Instead replace the bump node by the normal utility node
                            mc.connectAttr(bumpNode + '.out', material + '.' + attributeName,
                                           force=forceTexture)

                else:

                    # Connect the normal utility to the material attribute
                    mc.connectAttr(bumpNode + '.out', material + '.' + attributeName,
                                   force=forceTexture)

            else:

                # Connect the normal utility to the material attribute
                mc.connectAttr(bumpNode + '.out', material + '.' + attributeName,
                               force=forceTexture)

    # If there's no connections in the material attribute
    else:

        # Connect the normal utility to the material attribute
        mc.connectAttr(bumpNode + '.out', material + '.' + attributeName,
                       force=forceTexture)

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
        colorCorrect = mc.shadingNode('RedshiftColorCorrection', asTexture=True, isColorManaged=True, )

        textureInput = textureOutput.replace('outColor', 'input')
        ccTextureOutput = textureOutput.replace('outColor', 'outColor')

        # Connect the file node to the color correct
        mc.connectAttr(textureNode + '.' + textureOutput, colorCorrect + '.' + textureInput, force=forceTexture)

        # Connect the color correct to the material
        mc.connectAttr(colorCorrect + '.' + ccTextureOutput, targetNode + '.' + targetInput, force=forceTexture)

    # Connect the file node output to to right material input
    else:
        mc.connectAttr(textureNode + '.' + textureOutput, targetNode + '.' + targetInput, force=forceTexture)

def connect(ui, texture, renderer, fileNode):

    colorCorrect = ui.checkbox4.isChecked()
    useBump = ui.checkbox1.isChecked()
    useDisplace = ui.checkbox2.isChecked()

    # Change material brdf and fresnel mode
    mc.setAttr(texture.textureSet + '.refl_brdf', 1)
    mc.setAttr(texture.textureSet + '.refl_fresnel_mode', 2)
    "aiStandardSurface5.refl_brdf"

    # Change file node parameters to Raw and add alphaIsLuminance
    if texture.materialAttribute is not 'diffuse_color':
        try:
            mc.setAttr(fileNode + '.colorSpace', 'Raw', type='string')
        except:
            pass
        mc.setAttr(fileNode + '.alphaIsLuminance', True)

    # If height or normalMap
    if texture.attribute == 'height':

        # If bump
        if useBump:
            createBumpMap(texture, renderer, fileNode, colorCorrect)

        # If displace
        if useDisplace:
            createDisplacementMap(texture, renderer, fileNode, colorCorrect)

    # If normalMap
    elif texture.attribute == 'normal':

        createNormalMap(texture, renderer, fileNode, colorCorrect)

    # If it's another type of map
    else:
        connectTexture(fileNode, texture.output, texture.textureSet, texture.materialAttribute, colorCorrect)