PLUGIN_NAME = 'Substance to Maya'
PLUGIN_VERSION = '1.0'
TEXTURE_FOLDER = 'sourceImages'
INFOS = 'Tool licenced under GNU GPL 3\n\nReport bugs to tristan.legranche@gmail.com \n\ngithub.com/Strangenoise/SubstancePainterToMaya/'

PAINTER_IMAGE_EXTENSIONS = [
    'bmp', 'ico', 'jpeg', 'jpg', 'jng', 'pbm', 'pbmraw', 'pgm', 'pgmraw', 'png', 'ppm', 'ppmraw', 'targa',
    'tiff', 'tga', 'wbmp', 'xpm', 'gif', 'hdr', 'exr', 'j2k', 'jp2', 'pfm', 'webp', 'jpeg-xr', 'psd', 'tif'
]


BASE_COLOR = [
    'baseColor', 'BaseColor', 'basecolor', 'color', 'Color', 'albedo', 'Albedo'
]
HEIGHT = [
    'displace', 'Displace', 'Displacement', 'displacement', 'height', 'Height',
    'bump', 'Bump', 'BumpMap', 'bumpMap', 'displacementMap', 'DisplacementMap'
]
METALNESS = [
    'metal', 'Metal', 'metalness', 'Metalness'
]
NORMAL = [
    'normal', 'Normal', 'normalMap', 'NormalMap'
]
ROUGHNESS = [
    'roughness', 'Roughness', 'specularRoughness', 'SpecularRoughness', 'specular', 'Specular'
]
MATTE = [
    'Matte', 'matte'
]
OPACITY = [
    'Opacity', 'opacity', 'transparency', 'Transparency'
]
SUBSURFACE = [
    'subsurfaceColor', 'SubsurfaceColor', 'SSS', 'SSSColor', 'SSScolor', 'sss', 'sssColor', 'ssscolor'
]
EMISSION = [
    'emission', 'Emission', 'emissive', 'Emissive', 'light', 'Light'
]

DISPLACEMENT = [
    'displacement', 'displace', 'displ', 'disp', 'Disp', 'Displ', 'Displace', 'Displacement'
]

DELIMITERS = '-|_|@|\+| |\.'

