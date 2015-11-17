.. _tuto02:

*********************************************
[*Tuto02DataServiceBasic*] Display an image
*********************************************

The secons tutorial represents a basic application that display a medical 3D image. 

.. figure:: ../media/tuto02DataServiceBasic.png
    :scale: 50
    :align: center
    

Prerequisites
--------------

Before to read this tutorial, you should have seen :
 * :ref:`tuto01`
 

Structure
----------

Properties.cmake
~~~~~~~~~~~~~~~~~

This file describes the project information and requirements :

.. code-block:: cmake

    set( NAME Tuto02DataServiceBasic )
    set( VERSION 0.1 )
    set( TYPE APP )
    set( DEPENDENCIES  )
    set( REQUIREMENTS
        dataReg
        servicesReg
        gui
        guiQt
        io # contains the interface for reader and writer.
        ioVTK # contains the reader and writer for VTK files (image and mesh).
        visuVTK # loads VTK rendering library (fwRenderVTK).
        visuVTKQt # containsthe vtk Renderer window interactor manager using Qt.
        vtkSimpleNegato # contains a visualization service of medical image.
        launcher
        appXml
    )

    bundleParam(appXml PARAM_LIST config PARAM_VALUES tutoDataServiceBasicConfig)


.. note::

    The Properties.cmake file of the application is used by CMake to compile the application but also to generate the
    ``profile.xml``: the file used to launch the application. 
    

plugin.xml
~~~~~~~~~~~

This file is in the ``rc/`` directory of the application. It defines the services to run.
 
.. code-block:: xml

    <plugin id="Tuto02DataServiceBasic" version="@DASH_VERSION@">

        <extension implements="::fwServices::registry::AppConfig">
            <id>tutoDataServiceBasicConfig</id>
            <config>

                <!-- In tutoDataServiceBasic, the central data object is a ::fwData::Image. -->
                <object type="::fwData::Image">

                    <!--
                        Description service of the GUI:
                        The ::gui::frame::SDefaultFrame service automatically positions the various
                        containers in the application main window.
                        Here, it declares a container for the 3D rendering service.
                    -->
                    <service uid="myFrame" impl="::gui::frame::SDefaultFrame">
                        <gui>
                            <frame>
                                <name>tutoDataServiceBasic</name>
                                <icon>Bundles/Tuto02DataServiceBasic_0-1/tuto.ico</icon>
                                <minSize width="800" height="600" />
                            </frame>
                        </gui>
                        <registry>
                            <!-- Associate the container for the rendering service. -->
                            <view sid="myRendering" />
                        </registry>
                    </service>

                    <!--
                        Reading service:
                        The <file> tag defines the path of the image to load. Here, it is a relative 
                        path from the repository in which you launch the application.
                    -->
                    <service uid="myReaderPathFile" impl="::ioVTK::SImageReader">
                        <file>./TutoData/patient1.vtk</file>
                    </service>

                    <!--
                        Visualization service of a 3D medical image:
                        This service will render the 3D image.
                    -->
                    <service uid="myRendering" impl="::vtkSimpleNegato::SRenderer" />

                    <!--
                        Definition of the starting order of the different services:
                        The frame defines the 3D scene container, so it must be started first.
                        The services will be stopped the reverse order compared to the starting one.
                    -->
                    <start uid="myFrame" />
                    <start uid="myReaderPathFile" />
                    <start uid="myRendering" />

                    <!--
                        Definition of the service to update:
                        The reading service load the data on the update.
                        The render update must be called after the reading of the image.
                    -->
                    <update uid="myReaderPathFile" />
                    <update uid="myRendering" />

                </object>

            </config>
        </extension>

    </plugin>

    
For this tutorial, we have only one object ``::fwData::Image`` and three service:
 * ``::gui::frame::DefaultFrame``: frame service
 * ``::ioVTK::ImageReaderService``: reader for 3D VTK image
 * ``::vtkSimpleNegato::SRenderer``: render for 3D image
 
.. note::
    To avoid the ``<start uid="myRendering" />``, the frame service can automatically start the rendering service: you just need to add the attribute ``start="yes"`` in the <view> tag. 

Run
----

To run the application, you must call the following line in the install or build directory:

.. code::

    bin/launcher Bundles/Tuto02DataServiceBasic_0-1/profile.xml
