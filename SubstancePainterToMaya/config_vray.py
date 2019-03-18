

class config:

    def __init__(self):
        self.MAP_LIST = [
            '---- Choose', 'diffuse', 'height', 'reflection', 'glossiness', 'normal', 'IOR',
            '---- Basic', 'color', 'colorAmount', 'opacity', 'roughness', 'self-illumination',
            '---- Reflection', 'reflectionColor', 'reflectionColorAmount', 'hilightGlossiness', 'reflectionGlossiness', 'fresnelIOR',
            'ggxTailFalloff',
            '---- Anisotropy', 'anisotropy', 'anisotropyUVWGen', 'anisotropyRotation',
            '---- Reflection - advanced', 'reflectionExitColor',
            '---- Refraction', 'refractionColor', 'refractionColorAmount', 'refractionGlossiness', 'refractionIOR', 'fogColor', 'fogMult', 'fogBias',
            '---- Subsurface scattering', 'translucencyColor',
            '---- Bump and Normal mapping', 'bumpMap', 'normal', 'bumpMult', 'bumpDeltaScale',
            '---- Don\'t use'
        ]

        self.MAP_LIST_REAL_ATTRIBUTES = [
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

        self.MAPS_INDICES = {
            'baseColor': [
                ['baseColor', 'BaseColor', 'basecolor', 'color', 'Color', 'albedo', 'Albedo', 'diffuse', 'Diffuse', 'diff', 'Diff'],
                1
            ],
            'height': [
                ['displace', 'Displace', 'Displacement', 'displacement', 'height', 'Height', 'bump', 'Bump', 'BumpMap', 'bumpMap', 'displacementMap', 'DisplacementMap'],
                2
            ],
            'metalness': [
                [ 'metal', 'Metal', 'metalness', 'Metalness', 'reflection', 'Reflection'],
                3
            ],
            'normal': [
                ['normal', 'Normal', 'normalMap', 'NormalMap'],
                5
            ],
            'roughness': [
                ['roughness', 'Roughness', 'specularRoughness', 'SpecularRoughness', 'specular', 'Specular', 'glossiness', 'glossy', 'Glossiness', 'Glossy', 'spec', 'Spec'],
                4
            ],

            'opacity': [
                ['Opacity', 'opacity', 'transparency', 'Transparency'],
                10
            ],
            'subsurface': [
                ['subsurfaceColor', 'SubsurfaceColor', 'SSS', 'SSSColor', 'SSScolor', 'sss', 'sssColor', 'ssscolor'],
                35
            ]
        }

        self.MAP_LIST_COLOR_ATTRIBUTES_INDICES = [1, 2, 3, 5, 10, 12, 14, 25, 27, 31, 35, 37]
        self.DONT_USE_IDS = [0, 7, 13, 20, 24, 26, 32, 34, 36, 41]
        self.SHADER = 'VRayMtl'
        self.NORMAL_NODE = 'VRayBumpMtl'
        self.BUMP_NODE = 'VRayBumpMtl'
