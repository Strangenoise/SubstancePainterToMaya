##############################################
#
# SUBSTANCE PAINTER TO MAYA
#
# This tool is used to automatically connect Substance Painter textures to Arnold, VRay and Renderman for Maya.
#
# Created by Tristan Le Granche
# tristan.legranche@gmail.com
#
# Tool under licence CC-BY-NC
# Contact me for commercial use
#
# INSTALL
# Put the SubstancePainterToMaya folder in a PYTHONPATH folder (I.e: C:\Users\user\Documents\maya\scripts on Windows)
# Create a shelf button in Maya with the following Python command
# import SubstancePainterToMaya
# SubstancePainterToMaya.main.PainterToMaya()
#
# HOW TO USE
# 1. Click on the shelf button
# 2. Define the texture folder
# 3. Define the Naming Convention
# 4. Choose the renderer
# 5. Choose a materials option
# 6. Click on Launch
# 7. Specify where to plug each found maps
# 8. Choose some options
# 9. Click on Proceed
# 10. Enjoy !
#
# LIMITATIONS
# This version 0.1 only works with Arnold and uses aiStandardSurface shaders
#
# FOR MORE DETAILS
# Read the README.md file provided with the script
#
##############################################

# Libraries
import os
import config as cfg
import maya.cmds as mc
import maya.OpenMaya as om
import UI as ui
import launch as mainLaunch
reload(ui)
reload(mainLaunch)

# Variables
toolUI = ui.PainterToMayaUI()
toolUI.PLUGIN_NAME = cfg.PLUGIN_NAME
toolUI.PLUGIN_VERSION = cfg.PLUGIN_VERSION
toolUI.TEXTURE_FOLDER = cfg.TEXTURE_FOLDER
toolUI.INFOS = cfg.INFOS
toolUI.PAINTER_IMAGE_EXTENSIONS = cfg.PAINTER_IMAGE_EXTENSIONS

print('\n\n' + cfg.PLUGIN_NAME + ' version ' + cfg.PLUGIN_VERSION + '\n')

toolUI.createUI()

# Add action to launch button
toolUI.launchButton.clicked.connect(lambda: launch())

def launch():

    launcher = mainLaunch.launcher()
    launcher.ui = toolUI
    launcher.delimiters = cfg.DELIMITERS
    launcher.PAINTER_IMAGE_EXTENSIONS = cfg.PAINTER_IMAGE_EXTENSIONS
    launcher.launch()

    toolUI.proceedButton.clicked.connect(lambda: main(launcher))

def main(launcher):

    print '\nPROCEED\n'

    # Check if the textures need to be forced
    if toolUI.checkbox3.isChecked():
        forceTexture = True
    else:
        forceTexture = False

    # Get all textures
    for item in launcher.allTextures:

        # Create the texture path
        itemPath = os.path.join(toolUI.texturePath.text(), item)
        itemPath.replace('\\', '/')

        # For all maps name found
        for mapFound in launcher.mapsFound:
            if mapFound in item:

                # Get attributes from map name
                attributeName, attributeIndex = launcher.getShaderAttributeFromMapName(mapFound)

                if attributeIndex not in launcher.mapsDontUseIds:

                    material = launcher.getMaterialFromName(item)

                    # Check for material or create one
                    material, materialNotFound = launcher.checkOrCreateMaterial(material)

                    if materialNotFound:
                        print material + ' not found'

                    # If the material is found
                    else:
                        if mc.objExists(material):
                            launcher.connect(material, mapFound, itemPath, attributeName, attributeIndex,
                                           forceTexture)


                else:
                    print item + ' not used'

    print 'FINISHED'





