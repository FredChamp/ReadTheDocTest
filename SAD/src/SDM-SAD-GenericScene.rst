Generic Scene
============

Overview
------------------------

A generic scene in FW4SPL is visualization feature to visualize several elements like meshes or images in a scene. 
The scene is based on VTK. The main task of the generic scene is to manage all visualization services of the different elements contained in the scene.
The generic scene is universal and therefore applicable for divers visualization tasks. 
As used in FW4SPL, the scene generic configures a VTK scene with a simple xml configuration.
Hence, FW4SPL is mainly used for medical assignments, the generic scene can be seen as fusion of a negatoscope and the 3D model visualization. 

Components
------------------------

Manager
~~~~~~~~

The VtkRenderService is the manager service of the VTK scene. 
This service works on an object of type `fwData::Composite`. 
The associated object contains all objects to display. The manager retrieves its specified container.
The VTK context (vtkRender and vtkRenderWindow) is installed in the container of the manager.
The manager listens to the object signals of the associated `fwData::Composite` object. The transferred signals inform the manager if objects in the `fwData::Composite` have been added, removed or changed. 
In response to the modifications within the `fwData::Composite` object the manager supervises the starting and stopping of the visualization services (adaptors explained below), which are specified in its configuration.
Thus, an object is added or removed to the `fwData::Composite` object, the corresponding adaptor which works on this object is started or stopped.

Adaptor
~~~~~~~~

An adaptor is a service to manipulate or display a FW4SPL data. Services representing an adaptor are managed by a generic scene (VtkRenderService).
The adaptors are the gateway between FW4SPL objects and VTK objects. 
To respect the principles of the framework, adaptors are kept as generic as possible. 
Therefore they are reusable in further applications or even adaptors.


