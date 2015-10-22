.. _Component:

Component-based software
==============================

The FW4SPL is also a component-based architecture.
 
Component-based software engineering (CBSE) (also known as component-based development (CBD)) is a
branch of software engineering that emphasizes the separation of concerns in
respect of the wide-ranging functionality available throughout a given software
system. It is a reuse-based approach to defining, implementing and composing
loosely coupled independent components into systems. This practice aims to
bring about an equally wide-ranging degree of benefits in both the short-term
and the long-term for the software itself and for organizations that sponsor
such software. Excerpt from "Component-based software engineering" [#]_ on Wikipedia 

.. [#] Component-based software engineering http://en.wikipedia.org/wiki/Component-based_software_engineering  

Definitions and characteristics
-------------------------------

An individual software component is a software package that encapsulates a set
of related code: resources, objects, services, XML configuration, etc.

All the architecture is placed into separate components so that all of the data
and functions inside each component are semantically related. Because of this
principle, it is often said that components are modular and cohesive.

Components communicate with each other via interfaces. When a component offers
services to the rest of the system, it adopts a provided interface which
specifies services that other components can use. The generic architecture
provided by classes Object/IService and the factory system make this
interfacing easier.

Re-usability is an important characteristic of a high-quality software
component. Programmers should design and implement software components in such
a way that many different programs can reuse them.

Component-based implementation
------------------------------

Implementation requires a dynamic structure which represents the component
and a software launcher which loads and manages these components. 
A component, called a bundle, is just a simple folder that contains :

- the component description file (plugin.xml) to describe the content of the
  dynamic library
- the dynamic library, the type of which (.so, .dll, .dylib) differs between
  operating systems
- other shared resources (icons, XSD file, media files, ...)

The software launcher uses the library ``fwRuntime`` to parse the software
description file (profile.xml) and load required dynamic libraries::

    ./launcher.exe mySoftware/profile.xml


The component description file (plugin.xml) is used to describe the content of
the dynamic library. This file reveals which concepts and concept implementations are proposed by the component.
These terms are identified in the file by keywords:

- Extension point: the concept
- Extension: a concept implementation (there can be many implementations one of a single concept)

In some cases, the Extension point is represented by an abstract class in a
component, and the Extension by the class that it inherits from the abstract class of another component.

One example is the service concept. The component description file
of servicesReg introduces the concept of service and incorporates the class IService into the dynamic library:

.. code-block:: xml

 <plugin id="serviceReg">

   <library name="servicesReg" />

   <extension-point id="::fwServices::registry::ServiceFactory" />

 </plugin>

And in another component, a new service is proposed in the dynamic library and
the information is shared in the description file.

.. code-block:: xml

 <plugin id="myBundle">

    <library name ="myBundle" />

    <! -- myBundle requires the bundle servicesReg to run -->
    <requirement id="servicesReg" />

    <! -- Need code related to ::io::IReader -->
    <requirement id="io" />

    <extension implements =" ::fwServices::registry::ServiceFactory ">
        <! -- service type -->
        <type>::io::IReader</type>
        <! -- the service name available in this component library -->
        <service>::myBundle::myReader</service>
        <! -- the object type associated to the service -->
        <object>::fwData::myData</object>
        <desc>Description of my reader</desc>
    </extension>

 </plugin>

Even if it is often the case, concepts are not limited to class level.
A lot a concepts can be defined : service configurations, operator
parameters, etc.

