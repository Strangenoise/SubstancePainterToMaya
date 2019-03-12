import maya.cmds as mc
import helper
reload(helper)

def addVraySubdivisions(self, material):
    # Get values from interface
    maxSubdivs = int(self.maxSubdivIterVray.text())
    edgeLength = float(self.subdivIterVray.text())

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



def connect(material, mapFound, itemPath, attributeName, attributeIndex, forceTexture, ui, launcher):

    # Add subdivisions
    if ui.checkbox6.isChecked():
        addVraySubdivisions(material)

    # Create file node
    imageNode = helper.createFileNode(material, mapFound, itemPath)

    # Change file node parameters to Raw and add alphaIsLuminance
    if attributeName is not 'color':
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
    if attributeName == 'bumpMap':

        # If bump
        if ui.checkbox1.isChecked():

            bumpConnections = mc.listConnections(material + '.bumpMap')

            if mc.getAttr(material + '.bumpMapType') == 1 and bumpConnections:

                # Create bump material
                print material
                if '_shd' in material:
                    bumpMaterial = material.replace('_shd', '_bump')
                else:
                    bumpMaterial = material + '_bump'

                bumpMaterial = launcher.createMaterial(bumpMaterial, launcher.bumpNode)
                mc.setAttr(bumpMaterial + '.bumpMapType', 0)

                # Connect file to bump material
                helper.connectTexture(imageNode, '.' + outputAttr, bumpMaterial, '.' + 'bumpMap', ui.checkbox4.isChecked())

                # Connect bump material to original material shading group
                shadingGroups = mc.listConnections(material + '.outColor', destination=True)

                for shadingGroup in shadingGroups:
                    # Connect the displacement node to all the found shading engines
                    mc.connectAttr(bumpMaterial + '.outColor', shadingGroup + '.surfaceShader', force=forceTexture)

                # Connect material to bump material
                mc.connectAttr(material + '.outColor', bumpMaterial + '.base_material')

            else:
                helper.connectTexture(imageNode, '.' + outputAttr, material, '.' + 'bumpMap', ui.checkbox4.isChecked())
                mc.setAttr(material + '.bumpMapType', 0)

        # If displace
        if ui.checkbox2.isChecked():
            helper.createDisplacementMap(material, forceTexture, imageNode)

    # If normal Map
    elif attributeName == 'normalMap':

        bumpConnections = mc.listConnections(material + '.bumpMap')

        print bumpConnections

        if mc.getAttr(material + '.bumpMapType') == 0 and bumpConnections:

            # Create bump material
            print material
            if '_shd' in material:
                bumpMaterial = material.replace('_shd', '_bump')
            else:
                bumpMaterial = material + '_bump'

            bumpMaterial = launcher.createMaterial(bumpMaterial, launcher.bumpNode)
            mc.setAttr(bumpMaterial + '.bumpMapType', 1)

            # Connect file to bump material
            helper.connectTexture(imageNode, '.' + outputAttr, bumpMaterial, '.' + 'bumpMap', ui.checkbox4.isChecked())

            # Connect bump material to original material shading group
            shadingGroups = mc.listConnections(material + '.outColor', destination=True)

            for shadingGroup in shadingGroups:
                # Connect the displacement node to all the found shading engines
                mc.connectAttr(bumpMaterial + '.outColor', shadingGroup + '.surfaceShader', force=forceTexture)

            # Connect material to bump material
            mc.connectAttr(material + '.outColor', bumpMaterial + '.base_material')

        else:
            helper.connectTexture(imageNode, '.' + outputAttr, material, '.' + 'bumpMap')
            mc.setAttr(material + '.bumpMapType', 1)

    # If it's another type of map
    else:
        helper.connectTexture(imageNode, '.' + outputAttr, material, '.' + attributeName, ui.checkbox4.isChecked())