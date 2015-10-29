Object-Service concept
======================

Introduction
------------

Inside the Object Oriented Programming (OOP) paradigm, an object is an instance of a class
which contains all its data and methods (such as reading, writing, visualizations, image analysis, etc.). 
This philosophy works well, provided that the classes do not change with time.
However, in this situation, the maintenance of source code is difficult.

In order to make this maintenance easier, FW4SPL architecture relies on an Object-Service
paradigm where data and their methods are separated into different code units.

Object
-------

Objects represent data used in the framework. 
They can be simple (boolean, integer, string, etc.) or advanced structures 
(image, mesh, video, patient, etc.) without depending on the input data format. 
For example, an input image could have one of several formats such as Jpeg or Dicom but the FW4SPl object will be the same.

Moreover, these object classes contain only data features and their corresponding getter/setter methods.

For instance, the ``Image`` object:

- contains a buffer pointer, a buffer size, the image's dimension and origin,
- has public setter/getter methods to access these members,
- does not have methods such as reading or writing a buffer

The ``fwData`` library contains the standard simple and advanced data. 
It is the FW4SPL's main data library. There is also the ``fwMedData`` library which 
contains several structures to store medical data. 
A data list with a brief description is available in the appendixes.

Creating data
~~~~~~~~~~~~~

New data must be created as described below.

In the header file (MyData.hpp):

.. code:: cpp

    class MyData : public ::fwData::Object
    {

    public :
        fwCoreClassDefinitionsWithFactoryMacro( (MyData)(::fwData::Object),
            (()), ::fwData::factory::New< MyData >) ;


        // Private constructor, required for data factory
        MyData(::fwData::Object::Key key);

        /// Destructor, required for all data
        virtual ~MyData();

        /// Defines shallow copy, required for all data
        void shallowCopy( const Object::csptr& _source );

        /// Defines deep copy, required for all data
        void cachedDeepCopy(const Object::csptr& _source,
                                DeepCopyCacheType &cache);

    };

In the source file (MyData.cpp), this line must also be added to declare
``MyClass`` as data of the framework architecture :

.. code:: cpp

    fwDataRegisterMacro( MyData );

Service
-------

A service represents a functionality which uses or modifies data. A service
is always associated with a data. For example, image data can have a reader
service, a writer service, a visualization service or a processing operator.

Service type
~~~~~~~~~~~~

Some service categories exist in FW4SPL. These categories are called *service
types* and are represented by an abstract class. The basic service types are:

- ``io::IReader``: base interface for reader services.
- ``io::IWriter``: base interface for writer services.
- ``fwGui::IActionSrv``: base interface to manage action from a button or a
  menu in the GUI.
- ``gui::editor::IEditor``:  base interface to create new widget in the GUI.
- ``fwRender::IRender``: base interface to create new visualization widgets in
  the GUI.
- ``fwServices::IController``: Does nothing in particular but can be considered as
  a default service type to be implemented by unclassified services.

All services require a type association and must inherit from an abstract
type service.

Service methods
~~~~~~~~~~~~~~~

Several methods exist to manipulate a service. The main methods are:
``configure``, ``start``, ``stop``, and ``update``.

- ``configure``: parses the service parameters and analyzes its
  configuration. For example, this method is used to configure an image file
  path on the file system for an image reader service.
- ``start``: initializes and launches the service (be careful,
  starting and instantiating a service is not the same thing. For
  example, for a visualization service, the ``start`` method instantiates all GUI
  widgets necessary to visualize the data but the service itself is
  instantiated before.).
- ``stop``: stops the service. For example, for a visualization
  service, this method detaches and destroys all GUI widgets previously
  instantiated earlier in the ``start`` method.
- ``update`` method is called to perform an action on the data associated with the
  service. For example, for an image reader service, the service reads the
  image, converts it and loads it into the associated data.

These methods are mandatory, but can be empty. This is because some services do
not need a start/stop process, an update process or to listen to object
modifications.

Service states
~~~~~~~~~~~~~~

These methods must follow a calling sequence. For example, it is not possible to
stop a service before starting it. To secure the process, a state machine
has been implemented to control the calling sequence.

The calling sequence to manage a service is:

.. code:: cpp

    MyData::sptr myData = MyData::New();
    MyService::sptr mySrv = MyService::New();
    mySrv->setObject(myData);

    mySrv->setConfiguration( ... ); // set parameters
    mySrv->configure(); // check parameters
    mySrv->start(); // start the service
    mySrv->update(); // update the service
    mySrv->stop(); // stop the service


Create a service
~~~~~~~~~~~~~~~~

A new service must be created as described below.

In the header file (MyService.hpp):

.. code:: cpp

    class MyService : public AbstractServiceType
    {
    public:

        // Macro to define few important parameters/functions
        // used by the architecture
        fwCoreServiceClassDefinitionsMacro((MyService)(AbstractServiceType));

        // Service constructor
        MyService() throw() ;

        // Service destructor.
        virtual ~MyService() throw() ;

    protected:

        // To configure the service
        void configuring() throw(fwTools::Failed);

        // To start the service
        void starting() throw(::fwTools::Failed);

        // To stop the service
        void stopping() throw(::fwTools::Failed);

        // To update the service
        void updating() throw(::fwTools::Failed);
    };

In the source file (MyService.cpp), this line must be also added to declare
``MyService`` as a service of the framework architecture:

.. code:: cpp

    fwServicesRegisterMacro( AbstractServiceType, MyService, MyData );

.. note::
    When a new service is created, the following functions must be overloaded
    from IService class : ``configuring``, ``starting``, ``stopping`` and 
    ``updating``.  The top level functions from IService class check the 
    service state before any call to the redefined method.

Object and service factories
----------------------------

To instantiate an object or a service, the architecture requires the use of a
factory system. In class-based programming, the factory method pattern is a
creational pattern which uses factory methods to deal with the problem of
creating classes without specifying the exact class that will be created. This
is done by creating classes via a factory method, which is either specified in
an interface (abstract class) and implemented in child classes (concrete
classes) or implemented in a base class (optionally as a template method),
which can be overridden when inherited in derivative classes; rather than by a
constructor.[#]_

.. [#] http://en.wikipedia.org/wiki/Factory_method_pattern

Object factory
~~~~~~~~~~~~~~

The ``fwData`` library has a factory to register and create all objects.
The registration is managed by two macros:

.. code:: cpp

    // in .hpp file
    fwCoreClassDefinitionsWithFactoryMacro( (MyData)(::fwData::Object),
        (()), ::fwData::factory::New< MyData >);

    // in .cpp file
    fwDataRegisterMacro( MyData );

Then, there are only two ways to build data in the framework:

.. code:: cpp

    // Direct creation
    MyData::sptr obj = MyData::New();

    // Factory creation (here obj is an object of type
    // MyData, it is possible to cast it)
    ::fwData::Object::sptr obj = ::fwData::factory::New("MyData");

Service factory
~~~~~~~~~~~~~~~

The ``fwService`` library has a factory to register and create all
services. The registration is managed by two macros:

.. code:: cpp

    // in .hpp file
    fwCoreServiceClassDefinitionsMacro ((MyService)(AbstractServiceType));

    // in .cpp file
    fwServicesRegisterMacro( AbstractServiceType, MyService, MyData );

Then, there is only one way to build a service in the framework:

.. code:: cpp

    ::fwServices::registry::ServiceFactory::sptr srvFactory
            = ::fwServices::registry::ServiceFactory::getDefault();

    // Factory creation (here srv is a service of type MyService,
    // it is possible to cast it)
    ::fwServices::IService::sptr srv = srvFactory->create("MyService");

Object-Service registry
-----------------------

The FW4SPL architecture is standardized thanks to:

- Abstract classes ``fwData::Object`` and ``fwService::IService``.
- The two factory systems.

In an application, one of the problems is managing the life cycle of a large number of object instances and their services. This problem is solved by the class ``fwServices::registry::ObjectService`` which maintains the relationship
between objects and services. This class concept is very simple :

.. code-block:: cpp

    // OSR is a singleton
    class ObjectService
    {
      // relation map beetwen an object and his associated services
      map < Object *, vec < IService > > osr;

      // Associates a service to an object
      // manages in the function the association: srv->setObject(obj);
      void registerService ( Object * obj , IService * srv );

      // Dissociates a service to his object
      void unregisterService ( IService * srv );

      // ...
    }

    // Some helpers exist : below, add method is used to combine
    // factory system with service registration
    ::fwServices::IService::sptr add(::fwData::Object::sptr obj,
            std::string serviceType, std::string _implementationId)

This registry manages the object-service relationships and guarantees the non-destruction of an object while some services are still working on it.

.. _Object-Service_example:

Object-Service concept example
------------------------------

To conclude, the generic object-service concept is illustrated with this
example:

.. code-block:: cpp

    // Create an object
    ::fwData::Object::sptr obj = ::fwData::factory::New("::fwData::Image");

    // Create a reader and a view for this object
    ::fwServices::IService::sptr reader
        = ::fwServices::add(obj, "::io::IReader", "MyCustomImageReader");
    ::fwServices::IService::sptr view
        = ::fwServices::add(obj, "::fwRender::IRender", "MyCustomImageView");

    // Configure and start services
    reader->setConfiguration ( /* ... */ );
    reader->configure();
    reader->start();

    view->setConfiguration ( /* ... */ );
    view->configure();
    view->start();

    // Execute services
    reader->update(); // Read image on filesystem
    view->update(); // Refresh visualization with the new image buffer

    // Stop services
    reader->stop();
    view->stop();

    // Destroy services
    ::fwServices::registry::ObjectService::unregisterService(reader);
    ::fwServices::registry::ObjectService::unregisterService(view);

This example shows the code to create a small application to read an image
and visualize it. You can easily transform this code to build an application
which reads and displays a 3D mesh by changing object and services
implementation strings only.

