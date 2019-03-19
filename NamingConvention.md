# Substance to Maya
## version 0.1
## Naming Convention

[Go back to documentation](README.md)

## How does it works
Based on the textureSet and the map you specified, the script search for one file containing these names.  
Based on that file, the script extract the position of your textureSets and maps in all your files with the same Naming Convention.

I.e for file = myStudio_Johnny-SHD_Body-BaseColor.png, textureSet = SHD_Body, map = BaseColor  
The script will look after files with that naming convention: part_textureSet_textureSet_map.extension

I.e for file = rollingTeapot_john_SHD_body-baseColor.png, textureSet = SHD_body, map = baseColor  
The script will look after files with that naming convention: part_part-textureSet_textureSet-map.extension

Be careful with the lower and CAPITAL cases of the names you provied.  
baseColor and BaseColor are not the same. 

Don't mess with these parameters or the file won't work !

## What if i've multiple Naming Conventions ?

You'll have to use the script multiple times.  
Set the Naming Convention for one of the naming conventions you have, use the script.  
Then set the naming convention for another one, click on Re-launch and continue.

Do this for every naming convention you have.

## Exemples of textureSet and map

#### List of files
- rollingTeapot_body_BaseColor.png
- rollingTeapot_arms_BaseColor.png
- rollingTeapot_arms_Height.png
- rollingTeapot_arms_Metalness.png
- myStudio_rollingTeapot_SHD_body_BaseColor.png
- myStudio_rollingTeapot_SHD_Arms_Metalness.png
- myStudio_rollingTeapot_SHD_Arms_SSS.png
- RollingTeapot_Body_1001_BaseColor.png

#### Ex 01
textureSet = body  
map = BaseColor

Used textures :
- rollingTeapot_body_BaseColor.png
- rollingTeapot_arms_BaseColor.png
- rollingTeapot_arms_Height.png
- rollingTeapot_arms_Metalness.png

Unused textures:
- myStudio_rollingTeapot_SHD_body_BaseColor.png
- myStudio_rollingTeapot_SHD_Arms_Metalness.png
- myStudio_rollingTeapot_SHD_Arms_SSS.png
- RollingTeapot_Body_1001_BaseColor.png

#### Ex 02
textureSet = SHD_body  
map = BaseColor

Used textures :
- myStudio_rollingTeapot_SHD_body_BaseColor.png
- myStudio_rollingTeapot_SHD_Arms_Metalness.png
- myStudio_rollingTeapot_SHD_Arms_SSS.png

Unused textures:
- rollingTeapot_body_BaseColor.png
- rollingTeapot_arms_BaseColor.png
- rollingTeapot_arms_Height.png
- rollingTeapot_arms_Metalness.png
- RollingTeapot_Body_1001_baseColor.png

#### Ex 03
textureSet = Body  
map = baseColor

Used textures :
- RollingTeapot_Body_1001_baseColor.png

Unused textures:
- rollingTeapot_body_BaseColor.png
- rollingTeapot_arms_BaseColor.png
- rollingTeapot_arms_Height.png
- rollingTeapot_arms_Metalness.png
- myStudio_rollingTeapot_SHD_body_BaseColor.png
- myStudio_rollingTeapot_SHD_Arms_Metalness.png
- myStudio_rollingTeapot_SHD_Arms_SSS.png


[Go back to documentation](README.md)