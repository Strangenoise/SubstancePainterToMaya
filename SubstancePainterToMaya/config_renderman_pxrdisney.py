

class config:

    def __init__(self):
        self.MAP_LIST = [
            '---- Choose', 'baseColor', 'emitColor', 'subsurface', 'subsurfaceColor', 'metallic', 'specular', 'specularTint', 'roughness', 'anisotropic', 'sheen', 'sheenTint', 'clearcoat', 'clearcoatGloss', 'presence', 'normalMap', 'bumpMap',
            '---- Don\'t use'
        ]
        self.MAP_LIST_REAL_ATTRIBUTES = [
            '---- Choose', 'baseColor', 'emitColor', 'subsurface', 'subsurfaceColor', 'metallic', 'specular', 'specularTint', 'roughness', 'anisotropic', 'sheen', 'sheenTint', 'clearcoat', 'clearcoatGloss', 'presence', 'normalMap', 'bumpMap',
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
                16
            ],
            'metalness': [
                ['metal', 'Metal', 'metalness', 'Metalness'],
                5
            ],
            'normal': [
                ['normal', 'Normal', 'normalMap', 'NormalMap'],
                15
            ],
            'roughness': [
                ['roughness', 'Roughness', 'specularRoughness', 'SpecularRoughness', 'specular', 'Specular', 'spec',
                 'Spec'],
                8
            ],
            'opacity': [
                ['Opacity', 'opacity', 'transparency', 'Transparency', 'presence', 'Presence'],
                14
            ],
            'subsurface': [
                ['subsurfaceColor', 'SubsurfaceColor', 'SSS', 'SSSColor', 'SSScolor', 'sss', 'sssColor', 'ssscolor'],
                4
            ]
        }

        self.MAP_LIST_COLOR_ATTRIBUTES_INDICES = [1, 2, 4, 15]
        self.DONT_USE_IDS = [0, 17]
        self.SHADER = 'PxrDisney'
        self.NORMAL_NODE = 'PxrNormalMap'
        self.BUMP_NODE = 'PxrBump'
