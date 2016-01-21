**********
fw4spl
**********

This repository contains the core libraries and bundles.

---------
Features
---------

 - Reader/Writer
    - VTK (images and meshes)
    - DICOM
    - ITK
    - atoms (in-houte data format)
 - Visualisation
    - 2D and 3D multi-planar reconstruction
    - volume rendering
    - 3D meshes

------------
Application
------------
**VRRender** is an application containing all the previous features.

.. figure:: ../media/SDB.png
    :align: center

    Main VRRender view.

.. figure:: ../media/MPR.png
    :align: center

    MPR view of a medical 3D image.
    
.. figure:: ../media/3D.png
    :align: center

    3D view of surfacic meshes.
    
.. figure:: ../media/VR.png
        :align: center

        Volume rendering
    
.. figure:: ../media/VR-3D.png
    :align: center

    Volume rendering mixed with 3D surfacic meshes.

----------
Tutorials
----------
You can find some tutorials to explain fw4spl concept.


========================================  ================================================================
 Name                                     Concept
========================================  ================================================================
:ref:`Tuto01Basic<tuto01>`                Basic application
:ref:`Tuto02DataServiceBasic<tuto02>`     Simple image reading and rendering
Tuto02DataServiceBasicCtrl                Simple image reading and rendering without XML configuration
:ref:`Tuto03DataService<tuto03>`          Image reading and rendering with signal communication
:ref:`Tuto04SignalSlot<tuto04>`           Scene point of view synchronisation with signal communication
:ref:`Tuto05Mesher<tuto05>`               Simple mesher from a 3D image
:ref:`Tuto06Filter<tuto06>`               Simple image filter
:ref:`Tuto08GenericScene<tuto08>`         Scene with multi-object rendering
Tuto09MesherWithGenericScene              Scene with multi-object rendering and simple mesher
Tuto10MatrixTransformInGS                 Example of matrix transformation
Tuto11LaunchBasicConfig                   Example to launch XML config in application
Tuto12Picker                              Example of scene picker
Tuto13Scene2D                             Example using the ``scene2d``bundle
Tuto14MeshGenerator                       Mesh features (point/cell color, normals, ...)
Tuto15Multithread                         Example of multi-threading using fw4spl worker
Tuto15MultithreadCtrl                     Second example of multi-threading using fw4spl worker
TutoGui                                   Example of fw4spl gui feature (toolbar, menu, action)
TutoPython                                Example of pyhton binding in fw4spl
TutoTrianConverterCtrl                    Utility converting .trian meshes to .vtk
========================================  ================================================================