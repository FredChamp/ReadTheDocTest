.. _GUI:

Graphical User Interface
========================

Overview
--------

Graphical User Interface (GUI) is the process of displaying the graphical
components of an application. In fw4spl, the ``fwGui`` library provides abstract
tools to display components like windows, buttons, textfield, aso.

The software architecture provides a way of selecting different backends in order to manage the GUI components. As a result, the ``fwGuiQt`` library has been created to display components created using the Qt soup. Presently, this
backend is the only one supported by the applications.


Backend
-------

When creating an application, we need to specify which gui backend we want to use. To do so,
the chosen gui bundle must be activated and started in the profile.xml of the application. The
main gui bundle for any application is ``guiQt``. The ``gui`` bundle must be activated regardless
of the chosen backend.

.. code-block:: xml

    <activate id="gui" version="0-1" />
    <activate id="guiQt" version="0-1" />

    <!-- ... -->

    <start id="guiQt" />

**Warning :** The gui backend bundle must be started before any other bundle in the profile.xml.


Configuration
-------------

Frames
~~~~~~

The frame is the main component of a GUI. The main service used to represent a general frame is ``::fwGui::IFrameSrv``. The service ``::gui::frame::DefaultFrame`` is the default implementation for the main application frame. Every backend must provide its own implementation of this service.

The DefaultFrame service is configurable with different parameters :

* Application name
* Application icon
* Minimum window size
* GUI elements (toolbar, menubar, aso.)


.. code-block:: xml

    <service uid="mainFrame" type="::fwGui::IFrameSrv" 
        impl="::gui::frame::DefaultFrame" autoConnect="no" >
        <gui>
            <frame>
                <name>Application name</name>
                <icon>path_to_application_icon</icon>
                <minSize width="800" height="600"/>
            </frame>
            <menuBar />
            <toolBar >
                <toolBitmapSize height= "32" width="32" />
            </toolBar>
        </gui>
        <registry>
            <menuBar sid="menuBar" start="yes" />
            <toolBar sid="toolBar" start="yes" />
            <view sid="view" start="yes" />
        </registry>
    </service>


Menus and actions
~~~~~~~~~~~~~~~~~

The menu bar is used to organize application action groups. The main service used to display that kind of bar is ``::fwGui::IMenuBarSrv``. The service ``::gui::aspect::DefaultMenuBarSrv`` is the default implementation. Every backend must provide its own implementation of this service.

The configuration is used to associate a menu label with the service representing the menu.

.. code-block:: xml

    <service uid="menuBar" type="::fwGui::IMenuBarSrv"
        impl="::gui::aspect::DefaultMenuBarSrv" autoConnect="no" >
        <gui>
            <layout>
                <menu name="First Menu"/>
                <menu name="Second Menu"/>
            </layout>
        </gui>
        <registry>
            <menu sid="firstMenu" start="yes" />
            <menu sid="secondMenu" start="yes" />
        </registry>
    </service>


The main service used to display a menu is ``::fwGui::IMenuSrv``. The service ``::gui::aspect::DefaultMenuSrv`` is the default implementation. Every backend must provide its own implementation of this service.

The configuration is used to associate an action name and the service performing the action. An action can be configured with a shortcut, a style (default, check, radio) and/or an icon. Several special actions can also be
specified (QUIT, ABOUT, aso.).

.. code-block:: xml

    <service uid="myMenu" type="::fwGui::IMenuSrv"
        impl="::gui::aspect::DefaultMenuSrv" autoConnect="no" >
        <gui>
            <layout>
                <menuItem name="First Item" icon="icon_path" />
                <menuItem name="Checked Item" style="check" />
                <separator />
                <menuItem name="Quit" shortcut="Ctrl+Q" specialAction="QUIT" />
            </layout>
        </gui>
        <registry>
            <menuItem sid="actionFirstItem" start="no" />
            <menuItem sid="actionCheckedItem" start="no" />
            <menuItem sid="actionQuit" start="no" />
        </registry>
    </service>


A menu can also be displayed using a tool bar. The main service used to display a tool bar is ``::fwGui::IToolBarSrv``. The service ``::gui::aspect::DefaultToolBarSrv`` is the default implementation. Every backend must provide its own implementation of this service.

The configuration of a tool bar is the same as the one used to describe a menu.


Layouts
~~~~~~~

The layouts are used to organize the different parts of a GUI. The main service used to manage layouts is ``::fwGui::IGuiContainerSrv``. The service ``::gui::view::DefaultView`` is the default implementation. Every backend must provide its own implementation of this service.

Several types of layout can be used :

* Line layout
* Cardinal layout
* Tab layout


Every layout can be configured with a set of parameters (orientation, alignment, aso.).

.. code-block:: xml

    <service uid="subView" type="::gui::view::IView"
        impl="::gui::view::DefaultView" autoConnect="no" >
        <gui>
            <layout type="::fwGui::LineLayoutManager" >
                <orientation value="horizontal" />
                <view caption="view1" />
                <view caption="view2" />
            </layout>
        </gui>
        <registry>
            <view sid="subView1" start="yes" />
            <view sid="subView2" start="yes" />
        </registry>
    </service>


Multi-threading
---------------

The ``fwGui`` library has been designed to support multi-thread application. When a GUI component needs to be accessed, the function call must be encapsulated in a lambda declaration as shown in this example:

.. code-block:: cpp

        ::fwGui::registry::Worker::get()->postTask<void>(
        [&] {
                //TODO Write function calls
        }
        ).wait();

This encapsulation is required because all access to GUI components must be performed in the thread containing the GUI. It moves the function calls from the current thread, to the GUI thread.
