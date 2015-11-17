.. _tuto03:

*************************************************
[*Tuto03DataService*] Display an image with menu
*************************************************

The third tutorial is similar to the previous application, but we add gui service like menus.

.. figure:: ../media/tuto03DataService.png
    :scale: 50
    :align: center


Prerequisites
--------------

Before to read this tutorial, you should have seen :
 * :ref:`tuto02`
 * :ref:`GUI`


Structure
----------

Properties.cmake
~~~~~~~~~~~~~~~~~

This file describes the project information and requirements :

.. code-block:: cmake

    set( NAME Tuto03DataService )
    set( VERSION 0.1 )
    set( TYPE APP )
    set( DEPENDENCIES  )
    set( REQUIREMENTS
        dataReg
        servicesReg
        gui
        guiQt
        io
        ioVTK
        uiIO # contains services to show dialogs for reader/writer selection
        visuVTK
        visuVTKQt
        vtkSimpleNegato
        launcher
        appXml
    )

    bundleParam(appXml PARAM_LIST config PARAM_VALUES tutoDataServiceConfig)


.. note::

    The Properties.cmake file of the application is used by CMake to compile the application but also to generate the
    ``profile.xml``: the file used to launch the application.


plugin.xml
~~~~~~~~~~~

This file is in the ``rc/`` directory of the application. It defines the services to run.

.. code-block:: xml

    <plugin id="Tuto03DataService" version="@DASH_VERSION@">
        <requirement id="servicesReg" />

        <extension implements="::fwServices::registry::AppConfig">
            <id>tutoDataServiceConfig</id>
            <config>

                <!-- The root data object in tutoDataService is a ::fwData::Image. -->
                <object type="::fwData::Image">

                    <!-- Frame service:
                        The frame creates a container fot the rendering service and a menu bar.
                        In this tutorial, the gui services will automatically start the services they register using the
                        'start="yes"' attribute.
                    -->
                    <service uid="myFrame" impl="::gui::frame::SDefaultFrame">
                        <gui>
                            <frame>
                                <name>tutoDataService</name>
                                <icon>Bundles/Tuto03DataService_0-1/tuto.ico</icon>
                                <minSize width="800" height="600" />
                            </frame>
                            <menuBar />
                        </gui>
                        <registry>
                            <menuBar sid="myMenuBar" start="yes" />
                            <view sid="myRendering" start="yes" />
                        </registry>
                    </service>

                    <!--
                        Menu bar service:
                        This service defines the list of the menus displayed in the menu bar.
                        Here, we have only one menu: File
                        Each <menu> declared into the <layout> tag, must have its associated <menu> into the <registry> tag.
                        The <layout> tags defines the displayed information, whereas the <registry> tags defines the
                        services information.
                    -->
                    <service uid="myMenuBar" impl="::gui::aspect::SDefaultMenuBar">
                        <gui>
                            <layout>
                                <menu name="File" />
                            </layout>
                        </gui>
                        <registry>
                            <menu sid="myMenu" start="yes" />
                        </registry>
                    </service>

                    <!--
                        Menu service:
                        This service defines the actions displayed in the "File" menu.
                        Here, it registers two actions: "Open file", and "Quit".
                        As in the menu bar service, each <menuItem> declared into the <layout> tag, must have its
                        associated <menuItem> into the <registry> tag.

                        It's possible to associate specific attributes for <menuItem> to configure their style, shortcut...
                        In this tutorial, the attribute 'specialAction' has the value "QUIT". On MS Windows, there's no
                        impact, but on Mac OS, this value installs the menuItem in the system menu bar, and on Linux this
                        value installs the default 'Quit' system icon in the menuItem.
                    -->
                    <service uid="myMenu" impl="::gui::aspect::SDefaultMenu">
                        <gui>
                            <layout>
                                <menuItem name="Open file" shortcut="Ctrl+O" />
                                <separator />
                                <menuItem name="Quit" specialAction="QUIT" shortcut="Ctrl+Q" />
                            </layout>
                        </gui>
                        <registry>
                            <menuItem sid="actionOpenFile" start="yes" />
                            <menuItem sid="actionQuit" start="yes" />
                        </registry>
                    </service>

                    <!--
                        Quit action:
                        The action service (::gui::action::SQuit) is a generic action that will close the application
                        when the user click on the menuItem "Quit".
                    -->
                    <service uid="actionQuit" impl="::gui::action::SQuit" />

                    <!--
                        Open file action:
                        This service (::gui::action::StarterActionService) is a generic action, it starts and update the
                        services given in the configuration when the user clicks on the action.
                        Here, the reader selector will be called when the actions is clicked.
                    -->
                    <service uid="actionOpenFile" impl="::gui::action::SStarter">
                        <start uid="myReaderPathFile" />
                    </service>

                    <!--
                        Reader selector dialog:
                        This is a generic service that show a dialog to display all the reader or writer available for its
                        associated data. By default it is configured to show reader. (Note: if there is only one reading
                        service, it is directly selected without dialog box.)
                        Here, it the only reader available to read a ::fwData::Image is ::ioVTK::ImageReaderService (see
                        Tuto02DataServiceBasic), so the selector will not be displayed.
                        When the service was chosen, it is started, updated and stopped, so the data is read.
                    -->
                    <service uid="myReaderPathFile" impl="::uiIO::editor::SIOSelector" />

                    <!--
                        3D visualization service of medical images:
                        Here, the service attribute 'autoConnect="yes"' allows the rendering to listen the modification of
                        the data image. So, when the image is loaded, the visualization will be updated.
                    -->
                    <service uid="myRendering" impl="::vtkSimpleNegato::SRenderer" autoConnect="yes" />

                    <!--
                        Here, we only start the frame because all the others services are managed by the gui service:
                        - the frame starts the menu bar and the redering service
                        - the menu bar starts the menu services
                        - the menus starts the actions
                    -->
                    <start uid="myFrame" />

                </object>

            </config>
        </extension>
    </plugin>
    

The framework provides some gui services:

Frame (``::gui::frame::DefaultFrame``)
    This service display a frame and creates menu bar, tool bar and container for views, rendering service, ...
    
View (``::gui::view::DefaultView``)
    This service creates sub-container and tool bar.
    
Menu bar (``::gui::aspect::DefaultMenuSrv``)
    A menu bar displays menus.

Tool bar (``::gui::aspect::DefaultToolBarSrv``)
    A tool bar displays actions, menus and editors.

Menu (``::gui::aspect::DefaultMenuSrv``)
    A menu displays actions and sub-menus.

Action (inherited from ``::fwGui::IActionSrv`` )
    An action is a service inherited from ``::fwGui::IActionSrv``. It is called when the user clicks on the associated 
    tool bar or menu.

Editors (inherited from ``::gui::editor::IEditor``)
    An editor is a service inherited from ``::gui::editor::IEditor``. It is used to creates your own gui container.


Run
----

To run the application, you must call the following line into the install or build directory:

.. code::

    bin/launcher Bundles/Tuto03DataService_0-1/profile.xml
