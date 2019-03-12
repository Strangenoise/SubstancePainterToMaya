MAP_LIST = [
    '---- Choose', 'diffuse', 'height', 'normal', 'specRoughness', 'roughSpecularRoughness',
    '---- Diffuse', 'diffuseGain', 'diffuseColor', 'diffuseRoughness', 'diffuseBumpNormal',
    '---- Primary specular', 'specularFaceColor', 'specularEdgeColor', 'specularFresnelShape', 'specularRoughness', 'specularAnisotropy', 'specularAnisotropyDirection', 'specularBumpNormal',
    '---- Rough specular', 'roughSpecularFaceColor', 'roughSpecularEdgeColor', 'roughSpecularFresnelShape', 'roughSpecularRoughness', 'roughSpecularAnisotropy', 'roughSpecularAnisotropyDirection', 'roughSpecularBumpNormal',
    '---- Clear coat', 'clearcoatFaceColor', 'clearcoatEdgeColor', 'clearcoatFresnelShape', 'clearcoatRoughness', 'clearcoatAnisotropy', 'clearcoatAnisotropyDirection', 'clearcoatBumpNormal'
    '---- Iridescence', 'iridescenceFaceGain', 'iridescenceEdgeGain', 'iridescenceFresnelShape', 'iridescencePrimaryColor', 'iridescenceSecondaryColor', 'iridescenceRoughness', 'iridescenceAnisotropy', 'iridescenceAnisotropyDirection', 'iridescenceBumpNormal', 'iridescenceCurve', 'iridescenceScale',
    '---- Fuzz', 'fuzzGain', 'fuzzColor', 'fuzzConeAngle', 'fuzzBumpNormal',
    '---- Subsurface', 'subsurfaceGain', 'subsurfaceColor', 'subsurfaceDmfp', 'subsurfaceDmfpColor', 'subsurfacePostTint', 'subsurfaceDiffuseSwitch',
    '---- Single scatter', 'singlescatterGain', 'singlescatterColor', 'singlescatterMfp', 'singlescatterMfpColor', 'singlescatterDirectionality', 'singlescatterIor', 'singlescatterBlur', 'singlescatterDirectGain', 'singlescatterDirectGainTint',
    '---- Scattering globals', 'irradianceTint', 'irradianceRoughness',
    '---- Glass', 'refractionGain', 'reflectionGain', 'refractionColor', 'glassRoughness', 'glassAnisotropy', 'glassAnisotropyDirection', 'glassBumpNormal', 'glassIor', 'mwIor',
    '---- Interior', 'ssAlbedo', 'extinction',
    '---- Glow', 'glowGain', 'glowColor',
    '---- Globals', 'bumpNormal', 'shadowColor', 'presence',
    '---- Don\'t use'
]
MAP_LIST_REAL_ATTRIBUTES = [
    '---- Choose', 'diffuse', 'height', 'bumpNormal', 'specRoughness', 'roughSpecularRoughness',
    '---- Diffuse', 'diffuseGain', 'diffuseColor', 'diffuseRoughness', 'diffuseBumpNormal',
    '---- Primary specular', 'specularFaceColor', 'specularEdgeColor', 'specularFresnelShape', 'specularRoughness', 'specularAnisotropy', 'specularAnisotropyDirection', 'specularAnisotropyDirection', 'specularBumpNormal',
    '---- Rough specular', 'roughSpecularFaceColor', 'roughSpecularEdgeColor', 'roughSpecularFresnelShape', 'roughSpecularRoughness', 'roughSpecularAnisotropy', 'roughSpecularAnisotropyDirection', 'roughSpecularBumpNormal',
    '---- Clear coat', 'clearcoatFaceColor', 'clearcoatEdgeColor', 'clearcoatFresnelShape', 'clearcoatRoughness', 'clearcoatAnisotropy', 'clearcoatAnisotropyDirection', 'clearcoatBumpNormal'
    '---- Iridescence', 'iridescenceFaceGain', 'iridescenceEdgeGain', 'iridescenceFresnelShape', 'iridescencePrimaryColor', 'iridescenceSecondaryColor', 'iridescenceRoughness', 'iridescenceAnisotropy', 'iridescenceAnisotropyDirection', 'iridescenceBumpNormal', 'iridescenceCurve', 'iridescenceScale',
    '---- Fuzz', 'fuzzGain', 'fuzzColor', 'fuzzConeAngle', 'fuzzBumpNormal',
    '---- Subsurface', 'subsurfaceGain', 'subsurfaceColor', 'subsurfaceDmfp', 'subsurfaceDmfpColor', 'subsurfacePostTint', 'subsurfaceDiffuseSwitch',
    '---- Single scatter', 'singlescatterGain', 'singlescatterColor', 'singlescatterMfp', 'singlescatterMfpColor', 'singlescatterDirectionality', 'singlescatterIor', 'singlescatterBlur', 'singlescatterDirectGain', 'singlescatterDirectGainTint',
    '---- Scattering globals', 'irradianceTint', 'irradianceRoughness',
    '---- Glass', 'refractionGain', 'reflectionGain', 'refractionColor', 'glassRoughness', 'glassAnisotropy', 'glassAnisotropyDirection', 'glassBumpNormal', 'glassIor', 'mwIor',
    '---- Interior', 'ssAlbedo', 'extinction',
    '---- Glow', 'glowGain', 'glowColor',
    '---- Globals', 'bumpNormal', 'shadowColor', 'presence',
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
    'metal', 'Metal', 'metalness', 'Metalness'
]
NORMAL = [
    'normal', 'Normal', 'normalMap', 'NormalMap'
]
ROUGHNESS = [
    'roughness', 'Roughness', 'specularRoughness', 'SpecularRoughness', 'specular', 'Specular', 'spec', 'Spec'
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

MAP_LIST_COLOR_ATTRIBUTES_INDICES = [1, 2, 3, 8, 10, 12, 13, 17, 18, 20, 21, 25, 26, 28, 29, 33, 34, 39, 40, 43, 44, 51, 54, 56, 57, 61, 63, 68, 70, 75, 78, 79, 83, 84, 87, 89, 90]
DONT_USE_IDS = [0, 6, 11, 19, 27, 35, 47, 52, 59, 69, 72, 82, 85, 88]
SHADER_TO_USE = 'PxrSurface'
NORMAL_NODE = ''
BUMP_NODE = ''
