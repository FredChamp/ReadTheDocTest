***********
fw4spl-ext
***********

This repository contains additional functionalities and proofs of concept.

---------
Features
---------

 - additional DICOM reader/writer
    - PACS connection
    - 3D mesh segmentation reader/writer
    - DICOM filter for reader
 - navigation along a spline
 - timeline
 - network communication via openigtlink
 

------------
Application
------------

**VRRenderExt** is an application containing the **VRRender** features and also the additional fw4spl-ext features.

------------------
Proofs of concept
------------------

==============================  ================================================================
 Name                           Concept
==============================  ================================================================
PoC06Scene2DTF                   Simple use of ``scene2d`` bundle
PoC07TimeLine                    Timeline use with consumer/producer
PoC08Igtl                        Network communication with openigtlink
==============================  ================================================================


----------
Examples
----------

==============================  ================================================================
 Name                           Concept
==============================  ================================================================
Ex01VolumeRendering              Example of volume rendering using transfer function
Ex02ImageMix                     Example of image blend
Ex03Registration                 Example of simple rigid image-mesh registration
Ex04ImagesRegistration           Example of simple rigid image-image registration
==============================  ================================================================