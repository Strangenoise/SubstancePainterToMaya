from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from maya import OpenMayaUI as omui
import maya.mel as mel
import maya.cmds as mc
import os
import views
import config as cfg
reload(cfg)

class PainterToMayaUI(QtWidgets.QDialog):

    def __init__(self):

        super(PainterToMayaUI, self).__init__()

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
        self.mainWindow.setWindowFlags(QtCore.Qt.Window)

        # Create vertical layout
        self.layVMainWindowMain = QtWidgets.QVBoxLayout()
        self.layVMainWindowMain.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.mainWindow.setLayout(self.layVMainWindowMain)

        # Create horizontal layout
        self.layHMainWindowMain = QtWidgets.QHBoxLayout()
        self.layVMainWindowMain.insertLayout(0, self.layHMainWindowMain, stretch=1)

        # Create three vertical layouts
        self.leftPart = QtWidgets.QVBoxLayout()
        self.layHMainWindowMain.insertLayout(0, self.leftPart, stretch=1)
        self.middlePart = QtWidgets.QVBoxLayout()
        self.layHMainWindowMain.insertLayout(1, self.middlePart, stretch=1)
        self.rightPart = QtWidgets.QVBoxLayout()
        self.layHMainWindowMain.insertLayout(2, self.rightPart, stretch=1)

        # Project Path
        self.grpBrowseForProject = QtWidgets.QGroupBox('Project Path')
        self.grpBrowseForProject.setFixedWidth(300)
        self.leftPart.addWidget(self.grpBrowseForProject)

        self.projectFolderLayout = QtWidgets.QHBoxLayout()
        self.grpBrowseForProject.setLayout(self.projectFolderLayout)

        # Add Project Path widgets
        self.projectPath = QtWidgets.QLineEdit(self.actualWorkspace)
        self.projectPath.setToolTip('Set the path of your project')
        self.projectFolderLayout.addWidget(self.projectPath)

        self.changeProject = QtWidgets.QPushButton('Change')
        self.changeProject.clicked.connect(lambda: self.getProjectPath())
        self.changeProject.setToolTip('Change your project folder using a dialog window')
        self.projectFolderLayout.addWidget(self.changeProject)

        # Texture Folder
        self.grpBrowseForDirectory = QtWidgets.QGroupBox('Textures Folder')
        self.grpBrowseForDirectory.setFixedWidth(300)
        self.leftPart.addWidget(self.grpBrowseForDirectory)

        self.textureFolderLayoutV = QtWidgets.QVBoxLayout()
        self.grpBrowseForDirectory.setLayout(self.textureFolderLayoutV)

        self.textureFolderLayout = QtWidgets.QHBoxLayout()
        self.textureFolderLayoutV.insertLayout(0, self.textureFolderLayout, stretch=1)

        # Add Texture folder widgets
        self.texturePath = QtWidgets.QLineEdit()
        self.setTexturePath()
        self.texturePath.setToolTip('Set the path of your texture folder')
        self.textureFolderLayout.addWidget(self.texturePath)

        self.getSourceImagesButton = QtWidgets.QPushButton('Change')
        self.getSourceImagesButton.clicked.connect(lambda: self.getTextureFolder())
        self.textureFolderLayout.addWidget(self.getSourceImagesButton)
        self.getSourceImagesButton.setToolTip('Change your texture folder using a dialog window')

        self.checkboxSearchInSub = QtWidgets.QCheckBox('Search in subdirectories')
        self.checkboxSearchInSub.setChecked(False)
        self.textureFolderLayoutV.addWidget(self.checkboxSearchInSub)

        # Naming Convention
        self.grpNamingConvention = QtWidgets.QGroupBox('Naming Convention')
        self.grpNamingConvention.setFixedWidth(300)
        self.leftPart.addWidget(self.grpNamingConvention)

        self.namingConventionLayout = QtWidgets.QHBoxLayout()
        self.grpNamingConvention.setLayout(self.namingConventionLayout)

        self.comboNamingConvention = QtWidgets.QComboBox()
        self.comboNamingConvention.setToolTip('Empty')
        self.namingConventionLayout.addWidget(self.comboNamingConvention)

        self.editNamingConvention = QtWidgets.QPushButton('Edit')
        self.editNamingConvention.clicked.connect(lambda: self.editNamingConventions())
        self.namingConventionLayout.addWidget(self.editNamingConvention)
        self.editNamingConvention.setToolTip('Edit available naming conventions and set your preferred one')
        self.editNamingConvention.setToolTipDuration(2000)

        # Render Engine
        self.grpRenderEngine = QtWidgets.QGroupBox('Render Engine and Material')
        self.grpRenderEngine.setFixedWidth(300)
        self.leftPart.addWidget(self.grpRenderEngine)

        self.renderEngineLayout = QtWidgets.QHBoxLayout()
        self.grpRenderEngine.setLayout(self.renderEngineLayout)

        self.comboRenderEngine = QtWidgets.QComboBox()
        self.renderEngineLayout.addWidget(self.comboRenderEngine)

        # Materials
        self.grpMaterials = QtWidgets.QGroupBox('Materials')
        self.grpMaterials.setFixedWidth(300)
        self.leftPart.addWidget(self.grpMaterials)

        self.materialsLayout = QtWidgets.QVBoxLayout()
        self.grpMaterials.setLayout(self.materialsLayout)

        # Add Materials widgets
        self.grpRadioMaterials = QtWidgets.QButtonGroup()

        self.materialsRadio1 = QtWidgets.QRadioButton(
            'Use existing ones, and create new')
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
        self.grpLaunch.setFixedWidth(300)
        self.leftPart.addWidget(self.grpLaunch)

        self.launchLayout = QtWidgets.QVBoxLayout()
        self.grpLaunch.setLayout(self.launchLayout)

        # Add Launch widgets
        self.launchButton = QtWidgets.QPushButton('Search for textures')
        self.launchLayout.addWidget(self.launchButton)

        # Found Files
        self.grpFoundFiles = QtWidgets.QGroupBox('Found 0 Files')
        self.grpFoundFiles.setFixedWidth(300)
        self.middlePart.addWidget(self.grpFoundFiles)

        self.foundFilesLayout = QtWidgets.QVBoxLayout()
        self.grpFoundFiles.setLayout(self.foundFilesLayout)

        self.foundFilesSubLayout = QtWidgets.QHBoxLayout()
        self.foundFilesLayout.insertLayout(0, self.foundFilesSubLayout)

        self.lineEditEditFoundFiles = QtWidgets.QLineEdit(self.grpFoundFiles)
        self.lineEditEditFoundFiles.setPlaceholderText('Type to filter files...')
        self.lineEditEditFoundFiles.textChanged.connect(self.filterChanged)
        self.foundFilesSubLayout.addWidget(self.lineEditEditFoundFiles)

        self.listViewFoundFiles = views.ListView(self.grpFoundFiles)
        self.fileModel = views.TextureModel()
        self.proxyModel = QtCore.QSortFilterProxyModel(self)
        self.proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSortRole(QtCore.Qt.UserRole)
        self.proxyModel.setSourceModel(self.fileModel)
        self.listViewFoundFiles.setModel(self.proxyModel)
        self.listViewFoundFiles.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.foundFilesLayout.addWidget(self.listViewFoundFiles)

        self.labelFoundFiles = QtWidgets.QLabel(self.grpFoundFiles)
        self.labelFoundFiles.setText('To set files as used or unused :\n\nSelect the files in the list above\nand use the right click to open the context menu')
        self.labelFoundFiles.setAlignment(QtCore.Qt.AlignCenter)
        self.foundFilesLayout.addWidget(self.labelFoundFiles)

        # Found Maps
        self.grpFoundMaps = QtWidgets.QGroupBox('Found 0 Map Types')
        self.grpFoundMaps.setFixedWidth(300)
        self.rightPart.addWidget(self.grpFoundMaps)

        self.foundMapsLayout = QtWidgets.QVBoxLayout()
        self.grpFoundMaps.setLayout(self.foundMapsLayout)

        # Options
        self.grpOptions = QtWidgets.QGroupBox('Options')
        self.grpOptions.setFixedWidth(300)
        self.rightPart.addWidget(self.grpOptions)

        self.optionsLayout = QtWidgets.QVBoxLayout()
        self.grpOptions.setLayout(self.optionsLayout)

        self.optionsSubLayout1 = QtWidgets.QVBoxLayout()
        self.optionsLayout.insertLayout(1, self.optionsSubLayout1, stretch=1)

        self.optionsSubLayout2 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(2, self.optionsSubLayout2, stretch=1)

        self.optionsSubLayout3 = QtWidgets.QHBoxLayout()
        self.optionsLayout.insertLayout(3, self.optionsSubLayout3, stretch=1)

        # Options Widgets
        self.checkboxUDIMs = QtWidgets.QCheckBox('Use UDIMs')
        self.optionsSubLayout1.addWidget(self.checkboxUDIMs)

        self.checkbox1 = QtWidgets.QCheckBox('Use height as bump')
        self.checkbox1.setChecked(False)
        self.optionsSubLayout1.addWidget(self.checkbox1)

        self.checkbox2 = QtWidgets.QCheckBox('Use height as displace')
        self.checkbox2.setChecked(True)
        self.optionsSubLayout1.addWidget(self.checkbox2)

        self.checkbox3 = QtWidgets.QCheckBox('Force texture replacement')
        self.checkbox3.setChecked(True)
        self.checkbox3.setEnabled(False)
        self.checkbox3.setVisible(False)
        self.optionsSubLayout1.addWidget(self.checkbox3)

        self.checkbox4 = QtWidgets.QCheckBox('Add colorCorrect node after each file node')
        self.optionsSubLayout1.addWidget(self.checkbox4)

        # Proceed
        self.grpProceed = QtWidgets.QGroupBox('Proceed')
        self.rightPart.addWidget(self.grpProceed)

        self.proceedLayout = QtWidgets.QVBoxLayout()
        self.grpProceed.setLayout(self.proceedLayout)

        # Proceed widgets
        self.proceedButton = QtWidgets.QPushButton('Load & connect !')
        self.proceedLayout.addWidget(self.proceedButton)

        # Credits
        self.grpInfos = QtWidgets.QGroupBox('Credits')
        self.layVMainWindowMain.addWidget(self.grpInfos)

        self.infosLayout = QtWidgets.QVBoxLayout()
        self.grpInfos.setLayout(self.infosLayout)

        # Infos widgets
        self.infos = QtWidgets.QLabel(self.INFOS)
        self.infosLayout.addWidget(self.infos)
        self.infos.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)

        # Texture model context menu
        self.action_select = QtWidgets.QAction('Select the file(s)', self)
        self.action_select.triggered.connect(lambda: self.switchSelect(0))
        self.action_unselect = QtWidgets.QAction('Unselect the file(s)', self)
        self.action_unselect.triggered.connect(lambda: self.switchSelect(1))
        self.action_selectAll = QtWidgets.QAction('Select all', self)
        self.action_selectAll.triggered.connect(lambda: self.switchSelectAll(0))
        self.action_unSelectAll = QtWidgets.QAction('Unselect all', self)
        self.action_unSelectAll.triggered.connect(lambda: self.switchSelectAll(1))

        self.contextMenu = QtWidgets.QMenu(self)
        self.contextMenu.addAction(self.action_select)
        self.contextMenu.addAction(self.action_unselect)
        self.contextMenu.addSeparator()
        self.contextMenu.addAction(self.action_selectAll)
        self.contextMenu.addAction(self.action_unSelectAll)

        self.selectionModel = self.listViewFoundFiles.selectionModel()

        # Signals / slots
        self.listViewFoundFiles.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listViewFoundFiles.customContextMenuRequested.connect(self.show_list_textures_menu)

        # Hide some
        self.grpFoundFiles.setVisible(False)
        self.grpFoundMaps.setVisible(False)
        self.grpOptions.setVisible(False)
        self.grpProceed.setVisible(False)

        global window

        try:
            window.close()
            window.deleteLater()
        except:
            pass

        window = self.mainWindow
        self.mainWindow.show()
        print('UI opened')

    def show_list_textures_menu(self, pos):

        index = self.listViewFoundFiles.indexAt(pos)

        # self.action_selectAll.setEnabled()
        # self.action_unSelectAll.setEnabled()

        self.action_select.setEnabled(index.isValid())
        self.action_unselect.setEnabled(index.isValid())

        self.contextMenu.popup(self.listViewFoundFiles.viewport().mapToGlobal(pos))

    def filterChanged(self, text):
        self.proxyModel.setFilterWildcard("*" + text)

    def switchSelectAll(self, option, *args):
        # Get row count of proxy model
        rowCount = self.proxyModel.rowCount()

        for i in range(rowCount):
            index = self.proxyModel.index(i, 0)

            self.proxyModel.setData(index, option, QtCore.Qt.FontRole)

        if option == 0:
            self.listViewFoundFiles.initial_blink('select')
        else:
            self.listViewFoundFiles.initial_blink('unselect')
        self.listViewFoundFiles.blink()

    def switchSelect(self, option, *args):

        for index in self.selectionModel.selectedIndexes():
            self.proxyModel.setData(index, option, QtCore.Qt.FontRole)


    def stingraySwitch(self):

        if self.rendererRadio6.isChecked():
            self.materialsRadio1.setEnabled(False)
            self.materialsRadio2.setEnabled(False)

            self.materialsRadio3.setChecked(True)
        else:
            self.materialsRadio1.setEnabled(True)
            self.materialsRadio2.setEnabled(True)

    def getProjectPath(self):
        """
        Set the project path in the interface, the file dialog start in the base texture path of the project
        :return: The texture directory
        """

        # Open a file dialog
        mel.eval('SetProject;')

        # Update the project path in the interface
        self.actualWorkspace = mc.workspace(fullName=True)

        self.projectPath.setText(self.actualWorkspace)

        self.setTexturePath()

        return self.actualWorkspace

    def getTextureFolder(self):
        """
        Get the base texture path in the interface, the file dialog start in the base texture path of the project
        :return: The texture directory
        """

        # Open a file dialog
        if self.actualWorkspace in self.texturePath.text():
            opening_folder = self.actualWorkspace + self.texturePath.text()
        else:
            opening_folder = self.texturePath.text()

        if os.path.isdir(opening_folder):
            textureFolders = mc.fileDialog2(startingDirectory=opening_folder, fileMode=2, okCaption='Select')
        else:
            textureFolders = mc.fileDialog2(startingDirectory=self.actualWorkspace, fileMode=2, okCaption='Select')

        if textureFolders is None:
            return

        textureFolder = textureFolders[0] + '/'

        if self.actualWorkspace in textureFolder:
            textureFolder = textureFolder.replace(self.actualWorkspace, '')

        # Update the texture path in the interface
        self.texturePath.setText(textureFolder)

        return textureFolder

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

    def addRendermanSubdivisionsCheckbox(self):
        """
        Enable or disable subdivisions in the interface
        :return: None
        """

        # If subdivisions is checked
        if self.checkbox7.isChecked():
            self.subdivIterRenderman.setEnabled(True)
            self.subdivInterRenderman.setEnabled(True)

        # If subdivisions is not checked
        else:
            self.subdivIterRenderman.setEnabled(False)
            self.subdivInterRenderman.setEnabled(False)

    def addRedshiftSubdivisionsCheckbox(self):
        """

        :return:
        """
        # If subdivisions is checked
        if self.checkbox8.isChecked():
            self.subdivIterRedshift.setEnabled(True)
            self.subdivMin.setEnabled(True)
            self.subdivMax.setEnabled(True)

        # If subdivisions is not checked
        else:
            self.subdivIterRedshift.setEnabled(False)
            self.subdivMin.setEnabled(False)
            self.subdivMax.setEnabled(False)

    def editNamingConventions(self):

        return False

    def setTexturePath(self):

        sourceImagesFolder = '/' + mc.workspace(fileRuleEntry='sourceImages') + '/'

        if os.path.isdir(self.actualWorkspace + sourceImagesFolder):
            self.texturePath.setText(sourceImagesFolder)
        else:
            self.texturePath.setText('')

