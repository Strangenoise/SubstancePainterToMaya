
class config:

    def __init__(self):
        self.MAP_LIST = [
            '---- Choose', 'diffuse', 'height', 'metalness', 'normal', 'specRoughness',
            '---- Diffuse', 'diffuse_color', 'diffuse_weight', 'diffuse_roughness',
            '----  Backlighting / Translucency', 'transl_color', 'transl_weight',
            '---- Reflection', 'refl_color', 'refl_weight', 'refl_roughness', 'refl_aniso', 'refl_aniso_rotation',
            'refl_ior30', 'refl_ior31', 'refl_ior32', 'refl_k30', 'refl_k31', 'refl_k32', 'refl_reflectivity', 'refl_edge_tint', 'refl_reflectivity', 'refl_metalness', 'refl_ior',
            '---- Refraction / Transmission', 'refr_color', 'refr_weight', 'refr_abbe',
            '---- Sub - Surface', 'refr_transmittance', 'refr_absorption_scale', 'ss_scatter_coeff', 'ss_amount',
            '---- Multiple Scattering', 'ms_amount', 'ms_color0', 'ms_weight0', 'ms_radius0', 'ms_color1', 'ms_weight1', 'ms_radius1', 'ms_color2', 'ms_weight2', 'ms_radius2',
            '---- Coating', 'coat_color', 'coat_weight', 'coat_roughness', 'coat_samples', 'coat_ior30', 'coat_ior31', 'coat_ior32',
            'coat_reflectivity', 'coat_ior', 'coat_transmittance', 'coat_thickness', 'coat_bump_input',
            '---- Overall', 'overall_color', 'opacity_color', 'emission_color', 'emission_weight', 'bump_input',
            '---- Don\'t use'
        ]

        self.MAP_LIST_REAL_ATTRIBUTES = [
            '---- Choose', 'diffuse_color', 'bump_input', 'refl_metalness', 'bump_input', 'refl_roughness',
            '---- Diffuse', 'diffuse_color', 'diffuse_weight', 'diffuse_roughness',
            '----  Back - lighting / Translucency', 'transl_color', 'transl_weight', 'Reflection', 'refl_color', 'refl_weight', 'refl_roughness', 'refl_aniso', 'refl_aniso_rotation',
            'refl_ior30', 'refl_ior31', 'refl_ior32', 'refl_k30', 'refl_k31', 'refl_k32', 'refl_reflectivity', 'refl_edge_tint', 'refl_reflectivity', 'refl_metalness', 'refl_ior',
            '---- Refraction / Transmission', 'refr_color', 'refr_weight', 'refr_abbe',
            '---- Sub - Surface', 'refr_transmittance', 'refr_absorption_scale', 'ss_scatter_coeff', 'ss_amount',
            '---- Multiple Scattering', 'ms_amount', 'ms_color0', 'ms_weight0', 'ms_radius0', 'ms_color1', 'ms_weight1', 'ms_radius1', 'ms_color2', 'ms_weight2', 'ms_radius2',
            '---- Coating', 'coat_color', 'coat_weight', 'coat_roughness', 'coat_samples', 'coat_ior30', 'coat_ior31', 'coat_ior32', 'coat_reflectivity', 'coat_ior', 'coat_transmittance', 'coat_thickness', 'coat_bump_input',
            '---- Overall', 'overall_color', 'opacity_color', 'emission_color', 'emission_weight', 'bump_input',
            '---- Don\'t use'
        ]

        self.MAPS_INDICES = {
            'baseColor': [
                ['baseColor', 'BaseColor', 'basecolor', 'color', 'Color','albedo', 'Albedo', 'diffuse', 'Diffuse', 'diff', 'Diff'],
                1
            ],
            'height': [
                ['displace', 'Displace', 'Displacement', 'displacement', 'height', 'Height','bump', 'Bump', 'BumpMap', 'bumpMap', 'displacementMap', 'DisplacementMap'],
                2
            ],
            'metalness': [
                ['metal', 'Metal', 'metalness', 'Metalness'],
                3
            ],
            'normal': [
                ['normal', 'Normal', 'normalMap', 'NormalMap'],
                4
            ],
            'roughness': [
                ['roughness', 'Roughness', 'specularRoughness', 'SpecularRoughness', 'specular', 'Specular', 'spec', 'Spec'],
                5
            ],
            'opacity': [
                ['Opacity', 'opacity', 'transparency', 'Transparency'],
                64
            ],
            'emission': [
                ['emission', 'Emission', 'emissive', 'Emissive', 'light', 'Light'],
                67
            ]
        }

        self.MAP_LIST_COLOR_ATTRIBUTES_INDICES = [1, 2, 4, 7, 11, 14, 25, 26, 27, 31, 35, 37, 41, 44, 47, 51, 58, 60, 64, 65, 66, 68]
        self.DONT_USE_IDS = [0, 6, 10, 13, 30, 34, 39, 50, 63, 69]
        self.SHADER = 'RedshiftMaterial'
        self.NORMAL_NODE = 'RedshiftBumpMap'
        self.BUMP_NODE = 'RedshiftBumpMap'
        self.DISPLACE_NODE = 'RedshiftDisplacement'
