# -*- coding: utf-8 -*-

##############################################
#
# Created by : Tristan Le Granché
# Contact : tristan.legranche@gmail.com
# GitHub repository : https://github.com/Strangenoise/SubstancePainterToMaya
# Last edit made the : 11/13/2019
#
# LICENCE GNU GPL 3
#
# This file is part of SubstancePainterToMaya.
#
# SubstancePainterToMaya is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# SubstancePainterToMaya is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar.  If not, see https://www.gnu.org/licenses/.
#
##############################################

"""
TODO

2 - IN FOUND MAP TYPES
- Add displace in the map list attributes

4 - IN FOUND FILES
- Add the filter into Found Files
- Add the context menu into Found Files
- Add the ability to switch used/unused items in Found Files

5 - IN NAMING CONVENTION
- Set the naming convention edit window
- Add UDIMS into naming convention

"""

# Libraries
import os
import json
import importlib
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
import maya.cmds as mc
import maya.OpenMaya as om
import UI as ui
import helper
import views
reload(ui)
reload(helper)
reload(views)

# Load settings from json file
script_dir = os.path.dirname(os.path.realpath(__file__))

with open(script_dir + '/settings.json') as json_file:
    DATA = json.load(json_file)

json_file.close()

class rendererObject:

    def __init__(self):
        self.name = 'Arnold'

    def define(self):

        # Get selected render engine UI name
        ui_name = self.ui.comboRenderEngine.currentText()

        # Load render engines
        render_engines = DATA['render_engines']

        module_path = os.path.dirname(__file__)

        for render_engine in render_engines:
            if render_engine['ui_name'] == ui_name:
                full_module_name = 'SubstancePainterToMaya.SPToMv1.' + render_engine['config_file']
                config = importlib.import_module(full_module_name)
                reload(config)
                self.name = render_engine['name']
                break

        self.renderParameters = config.config()


def SPtoM():

    # Create the UI
    toolUI = ui.PainterToMayaUI()

    toolUI.createUI()
    toolUI.launchButton.clicked.connect(lambda: launch(toolUI))

    # Load the naming conventions
    naming_conventions = DATA['naming_conventions']

    for naming_convention in naming_conventions:
        toolUI.comboNamingConvention.addItem(naming_convention)

    toolUI.comboNamingConvention.setToolTip(toolUI.comboNamingConvention.currentText())

    # Load render engines
    render_engines = DATA['render_engines']

    for render_engine in render_engines:
        toolUI.comboRenderEngine.addItem(render_engine['ui_name'])

    toolUI.comboRenderEngine.setToolTip(toolUI.comboRenderEngine.currentText())

def launch(ui):

    print('\n LAUNCH \n')

    # Create the renderer
    renderer = rendererObject()
    renderer.ui = ui
    renderer.define()

    # Get project path
    projectPath = ui.projectPath.text()

    # Get textures path
    texturePath = ui.texturePath.text()
    if texturePath:
        if texturePath[0] == '/':
            texturePath = projectPath + texturePath
    else:
        texturePath = projectPath

    if os.path.isdir(texturePath):

        # Create all the map objects
        foundTextures = helper.listTextures(ui, texturePath, renderer)

        # Populate Tree View
        result = helper.populateFoundTextures(ui, foundTextures)

        # Empty foundMaps
        helper.clear_layout(ui.foundMapsLayout)

        if result:
            try:
                ui.useButton.clicked.disconnect()
            except:
                pass

            useTheseFiles(ui, foundTextures, renderer)
            ui.grpFoundFiles.setTitle('Found ' + str(len(foundTextures)) + ' Files')
        else:
            try:
                ui.useButton.clicked.disconnect()
            except:
                pass

            mc.warning('No texture found !')
            ui.grpFoundFiles.setTitle('Found ' + str(len(foundTextures)) + ' Files')
            ui.grpFoundMaps.setTitle('Found 0 Map Types')
            ui.grpFoundMaps.setVisible(False)
            ui.grpOptions.setVisible(False)
            ui.grpProceed.setVisible(False)

            return False

        # Change the button text
        ui.launchButton.setText('Search again for textures')

        # Show UI elements
        ui.grpFoundFiles.setVisible(True)
        ui.grpFoundMaps.setVisible(True)
        ui.grpOptions.setVisible(True)
        ui.grpProceed.setVisible(True)

    else:
        mc.warning('Specified texture folder doesn\'t exist !!! ')


def useTheseFiles(ui, foundTextures, renderer):

    textures = []
    final_textures = []
    mapTypes = []
    foundTypes = []

    print foundTextures

    for texture in ui.fileModel.items_list:
        for foundTexture in foundTextures:
            if texture.name == foundTexture.name:
                if foundTexture.mapName not in foundTypes:

                    mapName = foundTexture.mapName
                    indice = helper.getMapFromName(mapName, renderer)
                    mapInList = renderer.renderParameters.MAP_LIST[indice]

                    map = helper.Map(mapName, indice, mapInList)

                    mapTypes.append(map)
                    foundTypes.append(mapName)

                final_textures.append(foundTexture)

    uiElements = helper.populateFoundMaps(ui, renderer, mapTypes)

    helper.setRendererOptions(ui, renderer)

    ui.grpFoundMaps.setTitle('Found ' + str(len(mapTypes)) + ' Map Types')

    ui.proceedButton.clicked.connect(lambda: proceed(ui, final_textures, renderer, uiElements))


def proceed(ui, foundTextures, renderer, uiElements):

    print('\n PROCEED \n')

    # Import render definitions
    if renderer.name == 'Arnold':
        import helper_arnold as render_helper
        reload(render_helper)
        subdivisions = ui.checkbox5.isChecked()

    elif renderer.name == 'Vray':
        import helper_vray as render_helper
        reload(render_helper)
        subdivisions = ui.checkbox6.isChecked()

    elif renderer.name == 'PxrDisney':
        import helper_renderman as render_helper
        reload(render_helper)
        subdivisions = ui.checkbox7.isChecked()

    elif renderer.name == 'PxrSurface':
        import helper_renderman as render_helper
        reload(render_helper)
        subdivisions = ui.checkbox7.isChecked()

    elif renderer.name == 'Redshift':
        import helper_redshift as render_helper
        reload(render_helper)
        subdivisions = ui.checkbox8.isChecked()

    elif renderer.name == 'Stingray':
        import helper_stingray as render_helper
        reload(render_helper)
        subdivisions = False

    UDIMs = False

    if ui.checkboxUDIMs.isChecked():
        UDIMs = True

    # Connect textures
    for texture in foundTextures:

        if not texture.unselected:
            # Create file node and 2dPlacer
            fileNode = helper.createFileNode(texture, UDIMs)

            # Create material
            material, materialNotFound = helper.checkCreateMaterial(ui, texture, renderer)

            if materialNotFound:
                continue

            texture.textureSet = material
            texture.materialAttribute = renderer.renderParameters.MAP_LIST_REAL_ATTRIBUTES[texture.indice]

            render_helper.connect(ui, texture, renderer, fileNode)

            # Add subdivisions
            if subdivisions == True:
                render_helper.addSubdivisions(ui, texture)

    print('\n FINISHED \n')