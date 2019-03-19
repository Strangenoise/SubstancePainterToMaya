# Substance to Maya
## version 0.1
## Arnold exemple

[Go back to documentation](README.md)

1 - A scene is opened

![open scene](pics/03_openScene.jpg)

2 - With existing materials

![existing materials](pics/05_existingMaterials_vray.jpg)

3 - I launch the tool

![install_path](pics/06_launchTool.jpg)

4 - I use the predefined texture folder (project/sourceImages) in my case, use **Get** to use another one

![install_path](pics/07_textureFolder.jpg)

Here's the content of my folder

![install_path](pics/08_textureFolderContent.jpg)

5 - I enter the textureSet and the map of one of my textures in the Naming Convention part

![install_path](pics/09_setNamingConvention.jpg)

6 - I choose my render engine

![install_path](pics/09a_setRenderer_vray.jpg)

7 - I choose to create new materials if there's no existing one

![install_path](pics/09b_material.jpg)

8 - I click on launch to search for the textures.

![install_path](pics/09c_launch.jpg)

You can now see the list of the found maps, for each map you can specify in which VRayMtl parameter you want to plug it.  
See that a Coat, Sheen and Emission have been found, let ---- Choose so they will not be used, or choose another parameter.      
For more usual maps, the parameters are already set (but you can change them if you want)  
As I usually work with Arnold, I created Metalness and Roughness, used as Reflection and Glossiness.  
    
![install_path](pics/10_launch_vray.jpg)  

9 - I set the options (all in this case, so I will use height in bump and displace, force the texture replacement, add a colorCorrect after each file node and add subdivisions to the models)
    
![install_path](pics/11_setOptions_vray.jpg)  

10 - I click on proceed to launch the procedure
  
![install_path](pics/12_proceed.jpg)  

11 - Here is the result, textures are applied
  
![install_path](pics/13_result_vray.jpg)  

12 - In the Hypershade I can see all the new nodes
  
![install_path](pics/14_hypershade_vray.jpg)  

13 - A material in details, with the colorCorrects, the connection for bump and normalMap, the displacement
  
![install_path](pics/15_materialDetails_vray.jpg)  

14 - A created material, Lambert1 was defined as a name in my textureSets (see the texture folder content), because Lambert1 isn't an VRayMtl, because Lambert1 doesn't exist a new material Lambert1_shd has been created
  
![install_path](pics/16_createdMaterial_vray.jpg)  

15 - The models with already existing materials now have the subdivisions specified in the options
  
![install_path](pics/17_subdivisions_vray.jpg)  


[Go back to documentation](README.md)
