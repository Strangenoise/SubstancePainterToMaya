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
import maya.cmds as mc
import maya.OpenMaya as om
import UI as ui
import launch as mainLaunch
import helper
reload(ui)
reload(mainLaunch)
reload(helper)

# Variables
toolUI = ui.PainterToMayaUI()
toolUI.createUI()

# Add action to launch button
toolUI.launchButton.clicked.connect(lambda: launch(toolUI))

###################################
#
# Needed objects
#
# UI - ok
# Texture
# Renderer - ok
#
###################################

class rendererObject:

    def __init__(self):
        self.renderer = 'Arnold'

    def define(self):

        # Check for the render engine and load config file
        if self.ui.grpRadioRenderer.checkedId() == -2:
            import config_mtoa as config
            reload(config)
            self.renderer = 'Arnold'
            print 'Arnold'

        elif self.ui.grpRadioRenderer.checkedId() == -3:
            import config_vray as config
            reload(config)
            self.renderer = 'Vray'
            print 'Vray'

        elif self.ui.grpRadioRenderer.checkedId() == -4:
            import config_renderman_pxrdisney as config
            reload(config)
            self.renderer = 'PxrDisney'
            print 'Renderman - PxrDisney'

        elif self.ui.grpRadioRenderer.checkedId() == -5:
            import config_renderman_pxrsurface as config
            reload(config)
            self.renderer = 'PxrSurface'
            print 'Renderman - PxrSurface'

        self.mapsList = config.MAP_LIST
        self.mapsListRealAttributes = config.MAP_LIST_REAL_ATTRIBUTES
        self.mapsListColorAttributesIndices = config.MAP_LIST_COLOR_ATTRIBUTES_INDICES
        self.mapsDontUseIds = config.DONT_USE_IDS
        self.shaderToUse = config.SHADER_TO_USE
        self.normalNode = config.NORMAL_NODE
        self.bumpNode = config.BUMP_NODE

        self.baseColor = config.BASE_COLOR
        self.height = config.HEIGHT
        self.metalness = config.METALNESS
        self.normal = config.NORMAL
        self.roughness = config.ROUGHNESS
        self.matte = config.MATTE
        self.opacity = config.OPACITY
        self.subsurface = config.SUBSURFACE
        self.emission = config.EMISSION

def launch(toolUI):
    """
        Check for the chosen renderer
        Load specific config file
        Display second part of interface
        Launch the texture check
        :return: None
        """

    print '\nLAUNCH\n'

    mapsFound = []
    layoutPosition = 1
    allTextures = []
    mapsFoundElements = []

    # Create renderer
    renderer = rendererObject()
    renderer.ui = ui
    renderer.define()

    # Set variables

    # Display second part of the interface
    ui.grpFoundMaps.setVisible(True)
    ui.grpOptions.setVisible(True)

    arnoldUIElements = [ui.checkbox5, ui.subdivIterTitle, ui.subdivIter, ui.subdivTypeTitle, ui.subdivType]
    vrayUIElements = [ui.checkbox6, ui.subdivIterVrayTitle, ui.subdivIterVray, ui.subdivMaxVrayTitle,
                      ui.maxSubdivIterVray]
    rendermanUIElements = []

    if renderer == 'Arnold':
        for item in vrayUIElements:
            item.setVisible(False)

        for item in rendermanUIElements:
            item.setVisible(False)

        for item in arnoldUIElements:
            item.setVisible(True)

    elif renderer == 'Vray':
        for item in arnoldUIElements:
            item.setVisible(False)

        for item in rendermanUIElements:
            item.setVisible(False)

        for item in vrayUIElements:
            item.setVisible(True)

    elif renderer == 'PxrSurface' or renderer == 'PxrDisney':
        for item in arnoldUIElements:
            item.setVisible(False)

        for item in vrayUIElements:
            item.setVisible(False)

        for item in rendermanUIElements:
            item.setVisible(True)

    ui.grpProceed.setVisible(True)
    ui.launchButton.setText('Re-launch')

    clearLayout(ui.foundMapsLayout)

    # Populate the Found Maps part
    populateFoundMaps()

    ui.checkbox5.stateChanged.connect(lambda: ui.addArnoldSubdivisionsCheckbox())
    ui.checkbox6.stateChanged.connect(lambda: ui.addVraySubdivisionsCheckbox())

    return renderer

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





