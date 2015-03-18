App-config
=======================

Dynamic program with factories
------------------------------

As shown in the :ref:`Object-Service_example`, it is easy to change data and service to modify the application behavior by working on a mesh instead of an image. 
However, this is limited to one service working with one data. It is impossible to manage several objects/services to create complex software.

Then FW4SPL architecture provides a dynamic management of configurations to allow the use of multiple objects and services.

Dynamic program with application configuration
----------------------------------------------

In the ``fwService`` library, an application configuration parser
allows to parse XML files then creates and manages objects, services and
communications.

.. code:: c++

    // The parser
    void main (int argc , char * argv [])
    {
        string xmlAppConfigPath = argv [1];

        ::fwServices::AppConfigManager::sptr acm
                = ::fwServices::AppConfigManager::New();

        acm->setConfig(xmlAppConfigPath);
        acm->create(); // Creates objects and services from config.
        acm->start(); // Starts services specified in config.
        acm->update(); // Updates services specified in config.

        acm->stop(); // Stops services specified in config.
        acm->destroy(); // Destroy all services and then data.
    }

The following part correspond to the configuration XML file of the previous :ref:`Object-Service_example`.

.. code:: xml

    <object uid="image" type ="::fwData::MyData">

        <service uid="frame" impl="DefaultFrame" type="IFrame" >
            <!-- service configuration -->
        </service>

        <service uid="view" impl="MyCustomImageView"
                 type="::fwRender::IRender" >
            <!-- service configuration -->
        </service>

        <service uid="reader" impl="MyCustomImageReader"
                 type="::io::IReader" >
            <!-- service configuration -->
        </service>

        <!-- view listen now image modification -->
        <connect>
            <signal>image/objectModified</signal>
            <slot>view/receive</slot>
        </connect>

        <start uid="frame" />
        <start uid="view"/>
        <start uid="reader"/>

        <!-- Read the image on filesystem and notify 
             the view to refresh is content -->
        <update uid ="reader"/>

    </ object >

This is a simple example to show how to build an application with several objects and services thanks to a program and its configurations files.
