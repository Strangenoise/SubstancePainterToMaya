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
    maxSubdivs = int(ui.maxSubdivIterVray.text())
    edgeLength = float(ui.subdivIterVray.text())

    # Find the shapes connected to the material
    shader = mc.listConnections(material + '.outColor', d=True)[0]
    meshes = mc.listConnections(shader, type='mesh')
    shapes = mc.listRelatives(meshes, s=True)

    if shapes:

        # For all shapes add the render subdivisions
        for mesh in shapes:
            mc.select(mesh, replace=True)
            mc.vray("addAttributesFromGroup", mesh, "vray_subdivision", 1)
            mc.vray("addAttributesFromGroup", mesh, "vray_subquality", 1)
            mc.setAttr(mesh + '.vrayOverrideGlobalSubQual', 1)
            mc.setAttr(mesh + '.vrayMaxSubdivs', maxSubdivs)
            mc.setAttr(mesh + '.vrayEdgeLength', edgeLength)
            mc.select(mesh, d=True)

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

    bumpConnections = mc.listConnections(material + '.bumpMap')

    if mc.getAttr(material + '.bumpMapType') == 0 and bumpConnections:

        # Create bump material
        print material
        if '_shd' in material:
            bumpMaterial = material.replace('_shd', '_bump')
        else:
            bumpMaterial = material + '_bump'

        bumpMaterial = helper.createMaterial(bumpMaterial, bumpNode)
        mc.setAttr(bumpMaterial + '.bumpMapType', 1)

        # Connect file to bump material
        helper.connectTexture(fileNode, texture.output, bumpMaterial, 'bumpMap', colorCorrect)

        # Connect bump material to original material shading group
        shadingGroups = mc.listConnections(material + '.outColor', destination=True)

        for shadingGroup in shadingGroups:

            if mc.objectType(shadingGroup) == 'shadingEngine':
                # Connect the displacement node to all the found shading engines
                mc.connectAttr(bumpMaterial + '.outColor', shadingGroup + '.surfaceShader', force=forceTexture)

        # Connect material to bump material
        mc.connectAttr(material + '.outColor', bumpMaterial + '.base_material')

    else:
        helper.connectTexture(fileNode, texture.output, material, 'bumpMap')
        mc.setAttr(material + '.bumpMapType', 1)

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

    bumpConnections = mc.listConnections(material + '.bumpMap')

    if mc.getAttr(material + '.bumpMapType') == 1 and bumpConnections:

        # Create bump material
        if '_shd' in material:
            bumpMaterial = material.replace('_shd', '_bump')
        else:
            bumpMaterial = material + '_bump'

        bumpMaterial = helper.createMaterial(bumpMaterial, bumpNode)
        mc.setAttr(bumpMaterial + '.bumpMapType', 0)

        # Connect file to bump material
        helper.connectTexture(fileNode, texture.output, bumpMaterial, 'bumpMap', colorCorrect)

        # Connect bump material to original material shading group
        shadingGroups = mc.listConnections(material + '.outColor', destination=True)

        for shadingGroup in shadingGroups:

            if mc.objectType(shadingGroup) == 'shadingEngine':
                # Connect the displacement node to all the found shading engines
                mc.connectAttr(bumpMaterial + '.outColor', shadingGroup + '.surfaceShader', force=forceTexture)

        # Connect material to bump material
        mc.connectAttr(material + '.outColor', bumpMaterial + '.base_material')

    else:
        helper.connectTexture(fileNode, texture.output, material, 'bumpMap', colorCorrect)
        mc.setAttr(material + '.bumpMapType', 0)

def connect(ui, texture, renderer, fileNode):

    colorCorrect = ui.checkbox4.isChecked()
    useBump = ui.checkbox1.isChecked()
    useDisplace = ui.checkbox2.isChecked()

    # Change file node parameters to Raw and add alphaIsLuminance
    if texture.materialAttribute is not 'color':
        try:
            mc.setAttr(fileNode + '.colorSpace', 'Raw', type='string')
        except:
            pass
        mc.setAttr(fileNode + '.alphaIsLuminance', True)

    # If height
    if texture.materialAttribute == 'bumpMap':

            # If bump
            if useBump:
                createBumpMap(texture, renderer, fileNode, colorCorrect)

            # If displace
            if useDisplace:
                helper.createDisplacementMap(texture, fileNode, colorCorrect)

    # If normalMap
    elif texture.materialAttribute == 'normalMap':

        texture.materialAttribute = 'bumpMap'
        createNormalMap(texture, renderer, fileNode, colorCorrect)

    # If it's another type of map
    else:
        if texture.materialAttribute == 'translucencyColor':
            mc.setAttr(texture.textureSet + '.sssOn', 1)

        helper.connectTexture(fileNode, texture.output, texture.textureSet, texture.materialAttribute, colorCorrect)