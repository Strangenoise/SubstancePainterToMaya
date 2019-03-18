# Substance to Maya
## version 0.1
## Arnold exemple

[Go back to documentation](README.md)

1 - A scene is opened  

![open scene](pics/03_openScene.jpg)
  
2 - With existing materials

![existing materials](pics/05_existingMaterials.jpg)  

3 - I launch the tool
  
![install_path](pics/06_launchTool.jpg)  

4 - I use the predefined texture folder (project/sourceImages) in my case, use **Get** to use another one
  
![install_path](pics/07_textureFolder.jpg)  

5 - I let the naming convention by default because my texture files are matching it (mesh_textureSet_map.png)
  
![install_path](pics/08_textureFolderContent.jpg)  

6 - I click on launch to search for the textures.  
You can now see the list of the found maps, for each map you can specify in which aiStandardSurface parameter you want to plug it.  
See that a uvSnap and UVSnapshot000 have been found, I let the dropdown menu on ---- Choose so they will not be used  
For more usual maps, the parameters are already set (but you can change them if you want)
    
![install_path](pics/10_launch.jpg)  

7 - I set the options (all in this case, so I will use height in bug and displace, force the texture replacement, add a colorCorrect after each file node and add subdivisions to the models)
    
![install_path](pics/11_setOptions.jpg)  

8 - I click on proceed to launch the procedure
  
![install_path](pics/12_proceed.jpg)  

9 - Here is the result, textures are applied
  
![install_path](pics/13_result.jpg)  

10 - In the Hypershade I can see all the new nodes
  
![install_path](pics/14_hypershade.jpg)  

11 - A material in details, with the colorCorrects, the connection for bump and normalMap, the displacement
  
![install_path](pics/15_materialDetails.jpg)  

12 - A created material, Lambert1 was defined as a name in my textureSets (see the texture folder content), because Lambert1 isn't an aiStandardShader, a new one is created with the name Lambert1_shd
  
![install_path](pics/16_createdMaterial.jpg)  

13 - The models with already existing materials now have the subdivisions specified in the options
  
![install_path](pics/17_subdivisions.jpg)  

14 - The wireframe render (subdivisions power !)
  
![install_path](pics/18_subdivisions02.jpg)  

15 - And the final result (quickly made for this documentation)
  
![install_path](pics/19_render.jpg)  