
class config:

    def __init__(self):
        self.MAP_LIST = [
            '---- Choose', 'baseColor', 'normal', 'metallic', 'roughness', 'emissive', 'Ao',
            '---- Don\'t use'
        ]

        self.MAP_LIST_REAL_ATTRIBUTES = [
            '---- Choose', 'TEX_color_map', 'TEX_normal_map', 'TEX_metallic_map', 'TEX_roughness_map', 'TEX_emissive_map', 'TEX_ao_map',
            '---- Don\'t use'
        ]

        self.MAPS_INDICES = {
            'baseColor': [
                ['baseColor', 'BaseColor', 'basecolor', 'color', 'Color','albedo', 'Albedo', 'diffuse', 'Diffuse', 'diff', 'Diff'],
                1
            ],
            'metalness': [
                ['metal', 'Metal', 'metalness', 'Metalness', 'metallic', 'Metallic'],
                3
            ],
            'normal': [
                ['normal', 'Normal', 'normalMap', 'NormalMap'],
                2
            ],
            'roughness': [
                ['roughness', 'Roughness', 'specularRoughness', 'SpecularRoughness', 'specular', 'Specular', 'spec', 'Spec'],
                4
            ],
            'Ao': [
                ['ao', 'Ao', 'AO', 'ambient', 'Ambient', 'occlusion', 'Occlusion', 'AmbientOcclusion', 'Ambientocclusion', 'ambientocclusion'],
                6
            ],
            'emission': [
                ['emission', 'Emission', 'emissive', 'Emissive', 'light', 'Light'],
                5
            ]
        }

        self.MAP_LIST_COLOR_ATTRIBUTES_INDICES = [1, 2, 3, 4, 5, 6]
        self.DONT_USE_IDS = [0, 7]
        self.SHADER = 'StingrayPBS'
