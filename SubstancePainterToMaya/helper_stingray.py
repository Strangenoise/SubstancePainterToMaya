import maya.cmds as mc
import helper
reload(helper)

def connect(ui, texture, renderer, fileNode):

    colorCorrect = ui.checkbox4.isChecked()
    material = texture.textureSet

    helper.connectTexture(fileNode, texture.output, material, texture.materialAttribute, colorCorrect)

    if texture.materialAttribute == 'TEX_color_map':
        mc.setAttr(material + '.use_color_map', 1)
    elif texture.materialAttribute == 'TEX_normal_map':
        mc.setAttr(material + '.use_normal_map', 1)
    elif texture.materialAttribute == 'TEX_metallic_map':
        mc.setAttr(material + '.use_metallic_map', 1)
    elif texture.materialAttribute == 'TEX_roughness_map':
        mc.setAttr(material + '.use_roughness_map', 1)
    elif texture.materialAttribute == 'TEX_emissive_map':
        mc.setAttr(material + '.use_emissive_map', 1)
    elif texture.materialAttribute == 'TEX_ao_map':
        mc.setAttr(material + '.use_ao_map', 1)