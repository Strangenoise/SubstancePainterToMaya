import os
from PySide2 import QtCore
from PySide2 import QtWidgets
import maya.cmds as mc


class launcher:

    def __init__(self):

        self.mapsFound = []
        self.layoutPosition = 1
        self.allTextures = []
        self.mapsFoundElements = []
        self.renderer = 'Arnold'

        print '\nLAUNCH\n'

    def launch(self):
        """
        Check for the chosen renderer
        Load specific config file
        Display second part of interface
        Launch the texture check
        :return: None
        """

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

        # Set variables
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

        # Display second part of the interface
        self.ui.grpFoundMaps.setVisible(True)
        self.ui.grpOptions.setVisible(True)

        arnoldUIElements = [self.ui.checkbox5, self.ui.subdivIterTitle, self.ui.subdivIter, self.ui.subdivTypeTitle, self.ui.subdivType]
        vrayUIElements = [self.ui.checkbox6, self.ui.subdivIterVrayTitle, self.ui.subdivIterVray, self.ui.subdivMaxVrayTitle,
                          self.ui.maxSubdivIterVray]
        rendermanUIElements = []

        if self.renderer == 'Arnold':
            for item in vrayUIElements:
                item.setVisible(False)

            for item in rendermanUIElements:
                item.setVisible(False)

            for item in arnoldUIElements:
                item.setVisible(True)

        elif self.renderer == 'Vray':
            for item in arnoldUIElements:
                item.setVisible(False)

            for item in rendermanUIElements:
                item.setVisible(False)

            for item in vrayUIElements:
                item.setVisible(True)

        elif self.renderer == 'PxrSurface' or self.renderer == 'PxrDisney':
            for item in arnoldUIElements:
                item.setVisible(False)

            for item in vrayUIElements:
                item.setVisible(False)

            for item in rendermanUIElements:
                item.setVisible(True)

        self.ui.grpProceed.setVisible(True)
        self.ui.launchButton.setText('Re-launch')

        self.clearLayout(self.ui.foundMapsLayout)

        # Populate the Found Maps part
        self.populateFoundMaps()

        self.ui.checkbox5.stateChanged.connect(lambda: self.ui.addArnoldSubdivisionsCheckbox())
        self.ui.checkbox6.stateChanged.connect(lambda: self.ui.addVraySubdivisionsCheckbox())

    def clearLayout(self, layout):
        """
        Empty specified pySide2 layout
        :param layout: Layout to clear
        :return: None
        """

        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def getMapFromName(self, mapName):
        """
        Check if the map name correspond to a known attribute
        :param mapName: The name of the map
        :return: Index of the associated attribute
        """

        # Check for the render engine and load config file
        if self.renderer == 'Arnold':
            if mapName in self.baseColor:
                return 1
            elif mapName in self.height:
                return 2
            elif mapName in self.metalness:
                return 3
            elif mapName in self.normal:
                return 4
            elif mapName in self.roughness:
                return 5
            elif mapName in self.matte:
                return 54
            elif mapName in self.opacity:
                return 49
            elif mapName in self.subsurface:
                return 28
            elif mapName in self.emission:
                return 44
            else:
                return 0

        elif self.renderer == 'Vray':
            if mapName in self.baseColor:
                return 1
            elif mapName in self.height:
                return 2
            elif mapName in self.metalness:
                return 3
            elif mapName in self.normal:
                return 5
            elif mapName in self.roughness:
                return 4
            elif mapName in self.opacity:
                return 10
            elif mapName in self.subsurface:
                return 35
            else:
                return 0

        elif self.renderer == 'PxrDisney':
            if mapName in self.baseColor:
                return 1
            elif mapName in self.height:
                return 15
            elif mapName in self.metalness:
                return 5
            elif mapName in self.normal:
                return 15
            elif mapName in self.roughness:
                return 8
            elif mapName in self.subsurface:
                return 4
            else:
                return 0

        elif self.renderer == 'PxrSurface':
            if mapName in self.baseColor:
                return 1
            elif mapName in self.height:
                return 2
            elif mapName in self.metalness:
                return 4
            elif mapName in self.normal:
                return 3
            elif mapName in self.roughness:
                return 5
            elif mapName in self.opacity:
                return 87
            elif mapName in self.subsurface:
                return 61
            else:
                return 0

    def createMaterial(self, material, materialToUse):

        # Create the material
        material = mc.shadingNode(materialToUse, asShader=True, name=material + '_shd')

        return material

    def createShadingGroup(self, material):

        shadingEngineName = material.replace('_shd', '_SG')
        shadingEngine = mc.shadingNode('shadingEngine', asPostProcess=True, name=shadingEngineName)

        return shadingEngine

    def connect(self, material, mapFound, itemPath, attributeName, attributeIndex, forceTexture):

        # Check for the render engine and load config file
        if self.renderer == 'Arnold':
            import helper_arnold as helper
            reload(helper)

        elif self.renderer == 'Vray':
            import helper_vray as helper
            reload(helper)

        elif self.renderer == 'PxrDisney' or self.renderer == 'PxrSurface':
            import helper_renderman as helper
            reload(helper)

        helper.connect(material, mapFound, itemPath, attributeName, attributeIndex, forceTexture, self.ui, self)


    def createMaterialAndShadingGroup(self, material):
        """
        Create a material and it's shading group
        :param material: The material's name
        :return: The material's name
        """

        # Create the material
        material = self.createMaterial(material, self.shaderToUse)

        # Create the shading group
        shadingEngine = self.createShadingGroup(material)

        # Connect the material to the shading group
        mc.connectAttr(material + '.outColor', shadingEngine + '.surfaceShader')

        return material

    def checkOrCreateMaterial(self, material):
        """
        Based on the interface options, create or use existing materials
        :param material: The material's name
        :return: The material's name, if the material was found
        """

        materialNotFound = False

        # If create new materials if they doesn't exist, instead use existing ones
        if self.ui.grpRadioMaterials.checkedId() == -2:

            # If the material doesn't exist or if it's not of the right type
            if not mc.objExists(material) or not mc.objectType(material) == self.shaderToUse:

                # If a '_shd' version of the material doesn't exist
                if not mc.objExists(material + '_shd'):

                    # Create the material
                    material = self.createMaterialAndShadingGroup(material)

                else:

                    # Or add '_shd' at the name of the material
                    material += '_shd'

        # If create new ones
        elif self.ui.grpRadioMaterials.checkedId() == -3:

            # If the '_shd' version of the material doesn't exist
            if not mc.objExists(material + '_shd'):

                # Create the material
                material = self.createMaterialAndShadingGroup(material)

            else:

                # Or add '_shd' at the name of the material
                material += '_shd'

        # If use existing ones
        elif self.ui.grpRadioMaterials.checkedId() == -4:

            # If the material doesn't exist or if it's not of the right type
            if not mc.objExists(material) or not mc.objectType(material) == self.shaderToUse:
                # Specify that the material was not found
                materialNotFound = True

        return material, materialNotFound

    def getMaterialFromName(self, name):
        """
        Get material's name from texture's name
        :param name: Name of the texture
        :return: The name of the material
        """

        # Extract from naming convention
        textureSetPos, textureSetSeparator, mapPos, mapPosSeparator = self.extractFromNomenclature()

        # Get the name from naming convention
        materialName = name.split(textureSetSeparator)[textureSetPos].split('.')[0]

        return materialName

    def getShaderAttributeFromMapName(self, mapName):
        """
        From the map name, find the right material attribute to use
        :param mapName: The texture map's name
        :return: The name of the material attribute, the index of the material attribute
        """

        # For all the maps found elements
        for element in self.mapsFoundElements:

            # If the name of the element matches the texture's name
            if element[0].text() == mapName:
                # Get the attribute name and exist the loop
                attrName = self.mapsListRealAttributes[element[1].currentIndex()]
                break

        return attrName, element[1].currentIndex()

    def extractFromNomenclature(self):
        """
        Check for the naming convention specified in the interface and extract elements
        :return: position of the texture set, separator of the texture set, position of the map, separator of the map
        """


        textureSetPos = mapPos = 0
        textureSetSeparator = mapPosSeparator = '_'

        # For each delimiter
        for delimiter in self.delimiters:

            # Split the specified naming convention
            parts = self.ui.namingConvention.text().split(delimiter)

            # If there's a split
            if len(parts) > 1:

                # For each split
                for i in range(0, len(parts)):

                    # If the split is <textureSet>
                    if parts[i] == '$textureSet':
                        textureSetPos = i
                        textureSetSeparator = delimiter

                    # Elif the split is <map>
                    elif parts[i] == '$map':
                        mapPos = i
                        mapPosSeparator = delimiter

        return textureSetPos, textureSetSeparator, mapPos, mapPosSeparator

    def populateFoundMaps(self):
        """
        For all the texture files in the texture folder, create widgets in Found Maps part of the interface
        :return: None
        """

        # Extract elements from naming convention
        textureSetPos, textureSetSeparator, mapPos, mapPosSeparator = self.extractFromNomenclature()

        # List texture folder elements
        textureContent = os.listdir(self.ui.texturePath.text())

        layoutPosition = 0

        for item in textureContent:

            # Create the texture path
            itemPath = os.path.join(self.ui.texturePath.text(), item)

            # If item is a file
            if os.path.isfile(itemPath):

                # Get item's extension
                itemExtension = item.split('.')[1]

                # If its a valid texture file
                if itemExtension in self.PAINTER_IMAGE_EXTENSIONS:

                    # Add item to all textures
                    self.allTextures.append(item)

                    # Get map's name from texture's name
                    mapName = item.split(mapPosSeparator)[mapPos].split('.')[0]

                    # If the map name is not already listed (e.i: baseColor)
                    if mapName not in self.mapsFound:
                        # Get associated attribute name
                        correctMap = self.getMapFromName(mapName)

                        # Add the map to found maps
                        self.mapsFound.append(mapName)

                        # Create the layout
                        foundMapsSubLayout2 = QtWidgets.QHBoxLayout()
                        self.ui.foundMapsLayout.insertLayout(layoutPosition, foundMapsSubLayout2, stretch=1)

                        # Create the widgets
                        map1 = QtWidgets.QLineEdit(mapName)
                        foundMapsSubLayout2.addWidget(map1)

                        map1Menu = QtWidgets.QComboBox()
                        map1Menu.addItems(self.mapsList)
                        map1Menu.setCurrentIndex(correctMap)
                        foundMapsSubLayout2.addWidget(map1Menu)

                        # Add element to map found elements
                        self.mapsFoundElements.append([map1, map1Menu])

                        # Increment layout position
                        layoutPosition += 1
