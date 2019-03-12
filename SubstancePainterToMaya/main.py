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
import helper
reload(ui)
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
        self.name = 'Arnold'

    def define(self):

        # Check for the render engine and load config file
        if self.ui.grpRadioRenderer.checkedId() == -2:
            import config_mtoa as config
            reload(config)
            self.name = 'Arnold'
            print 'Arnold'

        elif self.ui.grpRadioRenderer.checkedId() == -3:
            import config_vray as config
            reload(config)
            self.name = 'Vray'
            print 'Vray'

        elif self.ui.grpRadioRenderer.checkedId() == -4:
            import config_renderman_pxrdisney as config
            reload(config)
            self.name = 'PxrDisney'
            print 'Renderman - PxrDisney'

        elif self.ui.grpRadioRenderer.checkedId() == -5:
            import config_renderman_pxrsurface as config
            reload(config)
            self.name = 'PxrSurface'
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


def SPtoM():

    # Create the UI
    toolUI = ui.PainterToMayaUI()
    toolUI.createUI()
    toolUI.launchButton.clicked.connect(lambda: launch(toolUI))

def launch(ui):

    print('\n LAUNCH \n')

    allTextures = []

    # Create the renderer
    renderer = rendererObject()
    renderer.ui = ui
    renderer.define()

    # Get all the texture files
    texturePath = ui.texturePath.text()
    foundFiles = os.listdir(texturePath)

    # Create all the map objects
    foundTextures = helper.listTextures(ui, renderer, foundFiles)

    # Remove elements from FoundMaps
    helper.clearLayout(ui.foundMapsLayout)

    # Populate the UI with the maps
    helper.populateFoundMaps(ui, renderer, foundTextures)

    # Display second part of the UI
    helper.displaySecondPartOfUI(ui, renderer)

    # Add connect to the proceed button
    ui.proceedButton.clicked.connect(lambda: proceed(ui, foundTextures, renderer))

def proceed(ui, foundTextures, renderer):

    print('\n PROCEED \n')

    # Create and connect the textures
    for foundTexture in foundTextures:

        # Find shader
        shader = helper.getShader(ui, foundTexture, renderer)

        print('Shader used is ' + shader)

        # Create file node and 2dPlacer
        fileNode = helper.createFileNode(foundTexture)

        print('File node created')

        # Connect connect file node
        connected = helper.connectFileNode(ui, foundTexture, renderer)

        if connected == True:
            print(foundTexture.textureName + ' connected')

        else:
            print(foundTexture.textureName + ' not connected')

    # Add subdivisions









