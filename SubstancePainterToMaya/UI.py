from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
import maya.cmds as mc
import os
import config as cfg

class PainterToMayaUI:

    def __init__(self):

        self.actualWorkspace = mc.workspace(fullName=True)
        self.PLUGIN_NAME = self.PLUGIN_VERSION = self.TEXTURE_FOLDER = ''
        self.PLUGIN_NAME = cfg.PLUGIN_NAME
        self.PLUGIN_VERSION = cfg.PLUGIN_VERSION
        self.TEXTURE_FOLDER = cfg.TEXTURE_FOLDER
        self.INFOS = cfg.INFOS
        self.PAINTER_IMAGE_EXTENSIONS = cfg.PAINTER_IMAGE_EXTENSIONS
        self.DELIMITERS = cfg.DELIMITERS

        print('\n\n' + self.PLUGIN_NAME + ' version ' + self.PLUGIN_VERSION + '\n')

    def createUI(self):
        """
        Creates the UI
        :return: None
        """

        mayaMainWindowPtr = omui.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

        # Create our main window
        self.mainWindow = QtWidgets.QDialog()
        self.mainWindow.setParent(mayaMainWindow)
        self.mainWindow.setWindowTitle(self.PLUGIN_NAME + ' version ' + self.PLUGIN_VERSION)
        # self.mainWindow.setFixedSize(220,450)
        self.mainWindow.setWindowFlags(QtCore.Qt.Window)

        # Create vertical layout
        self.layVMainWindowMain = QtWidgets.QVBoxLayout()
        self.mainWindow.setLayout(self.layVMainWindowMain)

        # Create horizontal layout
        self.layHMainWindowMain = QtWidgets.QHBoxLayout()
        self.layVMainWindowMain.insertLayout(0, self.layHMainWindowMain, stretch=1)

        # Create two vertical layouts
        self.layVMainWindow01 = QtWidgets.QVBoxLayout()
        self.layHMainWindowMain.insertLayout(0, self.layVMainWindow01, stretch=1)
        self.layVMainWindow02 = QtWidgets.QVBoxLayout()
        self.layHMainWindowMain.insertLayout(1, self.layVMainWindow02, stretch=1)

        # Texture Folder
        self.grpBrowseForDirectory = QtWidgets.QGroupBox('Textures Folder')
        self.layVMainWindow01.addWidget(self.grpBrowseForDirectory)

        self.textureFolderLayout = QtWidgets.QHBoxLayout()
        self.grpBrowseForDirectory.setLayout(self.textureFolderLayout)

        # Add Texture folder widgets
        sourceImagesFolder = self.actualWorkspace + '/' + self.TEXTURE_FOLDER
        self.texturePath = QtWidgets.QLineEdit(sourceImagesFolder)
        self.textureFolderLayout.addWidget(self.texturePath)

        self.getButton = QtWidgets.QPushButton('Get')
        self.getButton.clicked.connect(lambda: self.getTextureFolder())
        self.textureFolderLayout.addWidget(self.getButton)

        # Naming Convention
        self.grpNamingConvention = QtWidgets.QGroupBox('Naming Convention')
        self.layVMainWindow01.addWidget(self.grpNamingConvention)

        self.namingConventionLayout = QtWidgets.QVBoxLayout()
        self.grpNamingConvention.setLayout(self.namingConventionLayout)

        self.namingConventionSubLayout1 = QtWidgets.QVBoxLayout()
        self.namingConventionLayout.insertLayout(1, self.namingConventionSubLayout1, stretch=1)

        self.namingConventionSubLayout2 = QtWidgets.QHBoxLayout()
        self.namingConventionLayout.insertLayout(2, self.namingConventionSubLayout2, stretch=1)

        self.namingConventionSubLayout3 = QtWidgets.QVBoxLayout()
        self.namingConventionLayout.insertLayout(3, self.namingConventionSubLayout3, stretch=1)

        # Add Naming Convention widgets
        self.nomenclatureInfo = QtWidgets.QLabel(
            'Match the naming convention of the export from Substance Painter\nUse $map where you put your map\'s name\n$textureSet is needed too.'
        )
        self.namingConventionSubLayout1.addWidget(self.nomenclatureInfo)
        self.nomenclatureInfo.setStyleSheet('padding: 0 0 0 0;')

        self.namingConvention = QtWidgets.QLineEdit('$mesh_$textureSet_$map')
        self.namingConventionSubLayout2.addWidget(self.namingConvention)

        self.setNamingConventionButton = QtWidgets.QPushButton('Set')
        self.setNamingConventionButton.clicked.connect(lambda: self.setNamingConvention())
        self.namingConventionSubLayout2.addWidget(self.setNamingConventionButton)

        self.namingConventionInfo = QtWidgets.QLabel('I.e: boy_shader_baseColor.png')
        self.namingConventionLayout.addWidget(self.namingConventionInfo)

        # Renderer
        self.grpRenderer = QtWidgets.QGroupBox('Renderer')
        self.layVMainWindow01.addWidget(self.grpRenderer)

        self.rendererLayout = QtWidgets.QVBoxLayout()
        self.grpRenderer.setLayout(self.rendererLayout)

        # Add Renderer widgets
        self.grpRadioRenderer = QtWidgets.QButtonGroup()
        self.rendererRadio1 = QtWidgets.QRadioButton('Arnold (aiStandardSurface)')
        self.grpRadioRenderer.addButton(self.rendererRadio1)
        self.rendererRadio2 = QtWidgets.QRadioButton('VRay (VrayMtl)')
        self.grpRadioRenderer.addButton(self.rendererRadio2)
        self.rendererRadio3 = QtWidgets.QRadioButton('Renderman (PxrDisney)')
        self.grpRadioRenderer.addButton(self.rendererRadio3)
        self.rendererRadio1.setChecked(True)
        self.rendererRadio4 = QtWidgets.QRadioButton('Renderman (PxrSurface)')
        self.grpRadioRenderer.addButton(self.rendererRadio4)

        self.rendererLayout.addWidget(self.rendererRadio1)
        self.rendererLayout.addWidget(self.rendererRadio2)
        self.rendererLayout.addWidget(self.rendererRadio3)
        self.rendererLayout.addWidget(self.rendererRadio4)

        # Materials
        self.grpMaterials = QtWidgets.QGroupBox('Materials')
        self.layVMainWindow01.addWidget(self.grpMaterials)

        self.materialsLayout = QtWidgets.QVBoxLayout()
        self.grpMaterials.setLayout(self.materialsLayout)

        # Add Materials widgets
        self.grpRadioMaterials = QtWidgets.QButtonGroup()

        self.materialsRadio1 = QtWidgets.QRadioButton(
            'Use existing ones, if they don\'t exist, create new ones')
        self.grpRadioMaterials.addButton(self.materialsRadio1)
        self.materialsRadio1.setChecked(True)

        self.materialsRadio2 = QtWidgets.QRadioButton('Create new ones')
        self.grpRadioMaterials.addButton(self.materialsRadio2)

        self.materialsRadio3 = QtWidgets.QRadioButton('Use existing ones')
        self.grpRadioMaterials.addButton(self.materialsRadio3)

        self.materialsLayout.addWidget(self.materialsRadio1)
        self.materialsLayout.addWidget(self.materialsRadio2)
        self.materialsLayout.addWidget(self.materialsRadio3)

        # Launch button
        self.grpLaunch = QtWidgets.QGroupBox('Check for textures')
        self.layVMainWindow01.addWidget(self.grpLaunch)

        self.launchLayout = QtWidgets.QVBoxLayout()
        self.grpLaunch.setLayout(self.launchLayout)

        # Add Launch widgets
        self.launchButton = QtWidgets.QPushButton('Launch')
        self.launchLayout.addWidget(self.launchButton)

        # Found Maps
        self.grpFoundMaps = QtWidgets.QGroupBox('Found Maps')
        self.layVMainWindow02.addWidget(self.grpFoundMaps)

        self.foundMapsLayout = QtWidgets.QVBoxLayout()
        self.grpFoundMaps.setLayout(self.foundMapsLayout)

        # Options
        self.grpOptions = QtWidgets.QGroupBox('Options')
        self.layVMainWindow02.addWidget(self.grpOptions)

        self.optionsLayout = QtWidgets.QVBoxLayout()
        self.grpOptions.setLayout(self.optionsLayout)

        self.optionsSubLayout1 = QtWidgets.QVBoxLayout()
        self.optionsLayout.insertLayout(1, self.optionsSubLayout1, stretch=1)

        self.optionsSubLayout2 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(2, self.optionsSubLayout2, stretch=1)

        self.optionsSubLayout3 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(3, self.optionsSubLayout3, stretch=1)

        # Options Widgets
        self.checkbox1 = QtWidgets.QCheckBox('Use height as bump')
        self.optionsSubLayout1.addWidget(self.checkbox1)

        self.checkbox2 = QtWidgets.QCheckBox('Use height as displace')
        self.checkbox2.setChecked(True)
        self.optionsSubLayout1.addWidget(self.checkbox2)

        self.checkbox3 = QtWidgets.QCheckBox('Force texture replacement')
        self.checkbox3.setChecked(True)
        self.checkbox3.setEnabled(False)
        self.optionsSubLayout1.addWidget(self.checkbox3)

        self.checkbox4 = QtWidgets.QCheckBox('Add colorCorrect node after each file node')
        self.optionsSubLayout1.addWidget(self.checkbox4)

        self.checkbox5 = QtWidgets.QCheckBox('Add subdivisions')
        self.optionsSubLayout2.addWidget(self.checkbox5)

        self.subdivTypeTitle = QtWidgets.QLabel('Type')
        self.optionsSubLayout2.addWidget(self.subdivTypeTitle)

        self.subdivType = QtWidgets.QComboBox()
        self.subdivType.addItems(['catclark', 'linear'])
        self.subdivType.setEnabled(False)
        self.optionsSubLayout2.addWidget(self.subdivType)

        self.subdivIterTitle = QtWidgets.QLabel('Iterations')
        self.optionsSubLayout2.addWidget(self.subdivIterTitle)

        self.subdivIter = QtWidgets.QLineEdit('1')
        self.subdivIter.setEnabled(False)
        self.optionsSubLayout2.addWidget(self.subdivIter)

        self.checkbox6 = QtWidgets.QCheckBox('Add subdivisions')
        self.optionsSubLayout3.addWidget(self.checkbox6)

        self.subdivIterVrayTitle = QtWidgets.QLabel('Edge Length')
        self.optionsSubLayout3.addWidget(self.subdivIterVrayTitle)

        self.subdivIterVray = QtWidgets.QLineEdit('4')
        self.subdivIterVray.setEnabled(False)
        self.optionsSubLayout3.addWidget(self.subdivIterVray)

        self.subdivMaxVrayTitle = QtWidgets.QLabel('Max Subdivs')
        self.optionsSubLayout3.addWidget(self.subdivMaxVrayTitle)

        self.maxSubdivIterVray = QtWidgets.QLineEdit('4')
        self.maxSubdivIterVray.setEnabled(False)
        self.optionsSubLayout3.addWidget(self.maxSubdivIterVray)

        # Proceed
        self.grpProceed = QtWidgets.QGroupBox('Proceed')
        self.layVMainWindow02.addWidget(self.grpProceed)

        self.proceedLayout = QtWidgets.QVBoxLayout()
        self.grpProceed.setLayout(self.proceedLayout)

        # Proceed widgets
        self.proceedButton = QtWidgets.QPushButton('Proceed')
        self.proceedLayout.addWidget(self.proceedButton)

        # Infos
        self.grpInfos = QtWidgets.QGroupBox('Credits')
        self.layVMainWindowMain.addWidget(self.grpInfos)

        self.infosLayout = QtWidgets.QVBoxLayout()
        self.grpInfos.setLayout(self.infosLayout)

        # Infos widgets
        self.infos = QtWidgets.QLabel(self.INFOS)
        self.infosLayout.addWidget(self.infos)
        self.infos.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        # Hide some
        self.grpFoundMaps.setVisible(False)
        self.grpOptions.setVisible(False)
        self.grpProceed.setVisible(False)

        # List specific renderer elements
        self.arnoldUIElements = [
            self.checkbox5, self.subdivIterTitle, self.subdivIter, self.subdivTypeTitle, self.subdivType
        ]
        self.vrayUIElements = [
            self.checkbox6, self.subdivIterVrayTitle, self.subdivIterVray,
            self.subdivMaxVrayTitle, self.maxSubdivIterVray
        ]
        self.rendermanUIElements = []

        global window

        try:
            window.close()
            window.deleteLater()
        except:
            pass

        window = self.mainWindow
        self.mainWindow.show()
        print('UI opened')


    def setNamingConvention(self):
        """
        Change the naming convention example
        :return: The naming convention example
        """

        text = 'I.e: '

        # Change the naming convention example
        if '$textureSet' in self.namingConvention.text() and '$map' in self.namingConvention.text():
            text += self.namingConvention.text()

            text = text.replace('$textureSet', 'shader')
            text = text.replace('$map', 'baseColor')
            text = text.replace('$mesh', 'boy')

            self.namingConventionInfo.setStyleSheet(
                'color:%s;' % 'white' +
                'font-weight:regular;'
            )

            text += '.png'

        else:
            text = 'Warning: $textureSet and $map are needed !'
            self.namingConventionInfo.setStyleSheet(
                'color:%s;' % 'yellow' +
                'font-weight:bold;'
            )

        self.namingConventionInfo.setText(text)

        return text

    def getTextureFolder(self):
        """
        Get the base texture path in the interface, the file dialog start in the base texture path of the project
        :return: The texture directory
        """

        # Get project
        projectDirectory = mc.workspace(rootDirectory=True, query=True)

        # Set base texture folder
        textureFolder = projectDirectory + '/' + self.TEXTURE_FOLDER

        if os.path.isdir(textureFolder):
            sourceImages = textureFolder
        else:
            sourceImages = projectDirectory

        # Open a file dialog
        result = mc.fileDialog2(startingDirectory=self.texturePath.text(), fileMode=2, okCaption='Select')

        if result is None:
            return

        workDirectory = result[0]

        # Update the texture path in the interface
        self.texturePath.setText(workDirectory)

        return workDirectory

    def addArnoldSubdivisionsCheckbox(self):
        """
        Enable or disable subdivisions in the interface
        :return: None
        """

        # If subdivisions is checked
        if self.checkbox5.isChecked():
            self.subdivType.setEnabled(True)
            self.subdivIter.setEnabled(True)

        # If subdivisions is not checked
        else:
            self.subdivType.setEnabled(False)
            self.subdivIter.setEnabled(False)

    def addVraySubdivisionsCheckbox(self):
        """
        Enable or disable subdivisions in the interface
        :return: None
        """

        # If subdivisions is checked
        if self.checkbox6.isChecked():
            self.subdivIterVray.setEnabled(True)
            self.maxSubdivIterVray.setEnabled(True)

        # If subdivisions is not checked
        else:
            self.subdivIterVray.setEnabled(False)
            self.maxSubdivIterVray.setEnabled(False)