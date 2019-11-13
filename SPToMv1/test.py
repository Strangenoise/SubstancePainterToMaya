''' FOR THE MAP SET AND MESH '''

textureSet = ''
name = ''

textureSetStart = 0
nameStart = 0

textureSplit = re.split(ui.DELIMITERS, texture)

meshName, textureSet, mapName = splitNamingConvention(ui, texture)

print meshName, textureSet, mapName


if mapName and textureSetName:

        # If the map name is not already listed (e.i: baseColor)
        if mapName not in mapsFound:

            # Create map object
            map = foundMap()
            map.textureName = texture
            map.filePath = filePath
            map.extension = extension
            map.textureSet = textureSetName

            # Get associated attribute name
            map.indice = getMapFromName(mapName, renderer)
            map.mapName = mapName
            map.mapInList = renderer.renderParameters.MAP_LIST[map.indice]

            # Add map to foundTextures