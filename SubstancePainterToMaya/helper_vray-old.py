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


    # If height
    if attributeName == 'bumpMap':

        # If bump
        if ui.checkbox1.isChecked():



        # If displace
        if ui.checkbox2.isChecked():
            helper.createDisplacementMap(material, forceTexture, imageNode)

    # If normal Map
    elif attributeName == 'normalMap':



    # If it's another type of map
    else:
        helper.connectTexture(imageNode, '.' + outputAttr, material, '.' + attributeName, ui.checkbox4.isChecked())