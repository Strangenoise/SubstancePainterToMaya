MAP_LIST = [
    '----0 Choose', 'diffuse', 'height', 'reflection', 'glossiness', 'normal', 'IOR',
    '----7 Basic', 'color', 'colorAmount', 'opacity', 'roughness', 'self-illumination',
    '----13 Reflection', 'reflectionColor', 'reflectionColorAmount', 'hilightGlossiness', 'reflectionGlossiness', 'fresnelIOR',
    'ggxTailFalloff',
    '----20 Anisotropy', 'anisotropy', 'anisotropyUVWGen', 'anisotropyRotation',
    '----24 Reflection - advanced', 'reflectionExitColor',
    '----26 Refraction', 'refractionColor', 'refractionColorAmount', 'refractionGlossiness', 'refractionIOR', 'fogColor', 'fogMult', 'fogBias',
    '----34 Subsurface scattering', 'translucencyColor',
    '----36 Bump and Normal mapping', 'bumpMap', 'normal', 'bumpMult', 'bumpDeltaScale',
    '----41 Don\'t use'
]

MAP_LIST_REAL_ATTRIBUTES = [
    '---- Choose', 'color', 'bumpMap', 'reflectionColor', 'reflectionGlossiness', 'normalMap', 'fresnelIOR',
    '---- Basic', 'color', 'diffuseColorAmount', 'opacityMap', 'roughnessAmount', 'illumColor',
    '---- Reflection', 'reflectionColor', 'reflectionColorAmount', 'hilightGlossiness', 'reflectionGlossiness', 'fresnelIOR',
    'ggxTailFalloff',
    '---- Anisotropy', 'anisotropy', 'anisotropyUVWGen', 'anisotropyRotation',
    '---- Reflection - advanced', 'reflectionExitColor',
    '---- Refraction', 'refractionColor', 'refractionColorAmount', 'refractionGlossiness', 'refractionIOR', 'fogColor', 'fogMult', 'fogBias',
    '---- Subsurface scattering', 'translucencyColor',
    '---- Bump and Normal mapping', 'bumpMap', 'normalMap', 'bumpMult', 'bumpDeltaScale',
    '---- Don\'t use'
]

BASE_COLOR = [
    'baseColor', 'BaseColor', 'basecolor', 'color', 'Color', 'albedo', 'Albedo', 'diffuse', 'Diffuse', 'diff', 'Diff'
]
HEIGHT = [
    'displace', 'Displace', 'Displacement', 'displacement', 'height', 'Height',
    'bump', 'Bump', 'BumpMap', 'bumpMap', 'displacementMap', 'DisplacementMap'
]
METALNESS = [
    'metal', 'Metal', 'metalness', 'Metalness', 'reflection', 'Reflection'
]
NORMAL = [
    'normal', 'Normal', 'normalMap', 'NormalMap'
]
ROUGHNESS = [
    'roughness', 'Roughness', 'specularRoughness', 'SpecularRoughness', 'specular', 'Specular', 'glossiness', 'glossy', 'Glossiness', 'Glossy', 'spec', 'Spec'
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

MAP_LIST_COLOR_ATTRIBUTES_INDICES = [1, 2, 3, 5, 10, 12, 14, 25, 27, 31, 34, 37]
DONT_USE_IDS = [0, 7, 13, 20, 24, 26, 34, 36, 41]
SHADER_TO_USE = 'VRayMtl'
NORMAL_NODE = 'VRayBumpMtl'
BUMP_NODE = 'VRayBumpMtl'
