

class config:

    def __init__(self):
        self.MAP_LIST = [
            '---- Choose', 'diffuse', 'height', 'normal', 'specularFaceColor', 'specularRoughness',
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
        self.MAP_LIST_REAL_ATTRIBUTES = [
            '---- Choose', 'diffuseColor', 'bumpMap', 'normalMap', 'specularFaceColor', 'specularRoughness',
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

        self.MAPS_INDICES = {
            'baseColor': [
                ['baseColor', 'BaseColor', 'basecolor', 'color', 'Color', 'albedo', 'Albedo', 'diffuse', 'Diffuse',
                 'diff', 'Diff'],
                1
            ],
            'height': [
                ['displace', 'Displace', 'Displacement', 'displacement', 'height', 'Height', 'bump', 'Bump', 'BumpMap',
                 'bumpMap', 'displacementMap', 'DisplacementMap'],
                2
            ],
            'metalness': [
                ['metal', 'Metal', 'metalness', 'Metalness', 'specularFaceColor', 'specularfacecolor', 'SpecularFaceColor'],
                4
            ],
            'normal': [
                ['normal', 'Normal', 'normalMap', 'NormalMap'],
                3
            ],
            'roughness': [
                ['roughness', 'Roughness', 'specularRoughness', 'SpecularRoughness', 'specular', 'Specular', 'spec',
                 'Spec'],
                5
            ],
            'opacity': [
                ['Opacity', 'opacity', 'transparency', 'Transparency', 'presence', 'Presence'],
                90
            ],
            'subsurface': [
                ['subsurfaceColor', 'SubsurfaceColor', 'SSS', 'SSSColor', 'SSScolor', 'sss', 'sssColor', 'ssscolor'],
                61
            ]
        }

        self.MAP_LIST_COLOR_ATTRIBUTES_INDICES = [1, 2, 3, 4, 8, 10, 12, 13, 17, 18, 20, 21, 25, 26, 28, 29, 33, 34, 39, 40, 43, 44, 51, 54, 56, 57, 61, 63, 68, 70, 75, 78, 79, 83, 84, 87, 89, 90]
        self.DONT_USE_IDS = [0, 6, 11, 19, 27, 35, 47, 52, 59, 69, 72, 82, 85, 88]
        self.SHADER = 'PxrSurface'
        self.NORMAL_NODE = 'PxrNormalMap'
        self.BUMP_NODE = 'PxrBump'
