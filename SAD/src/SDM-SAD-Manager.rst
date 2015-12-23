Manager and updater services
==================================

Concepts
--------

In the FW4SPL architecture, there is an object container which is often used:
``::fwData::Composite``. This container is also an Object and represents a map
which associates a string with an Object. The architecture provides two main
services to manage a Composite: a composite updater and a service manager.

Updater
~~~~~~~

The updater service extends service type ``::ctrlSelection::IUpdaterSrv`` and
the work on a selection composite. This kind of service listens specific events
from objects identified by their UID. When it receives an event, it performs an
operation on an object in the selection composite and notifies composite
listeners.

Available operations on composite are:

- Adding an object
- Swapping an object
- Removing an object
- Removing an object if present
- Adding or swapping an object
- Doing nothing

There are few generic updater services which listen all events sent by Objects,
and few other which work with particular Object events.

Manager
~~~~~~~

The manager services extend service type ``::ctrlSelection::IManagerSrv`` and
react to updater messages. This kind of service manages services on identified
data if they are present in a composite. There are few manager services,
but the most common is ``::ctrlSelection::manager::SwapperSrv``. This service
manages other services on objects stored in the composite. When this
manager gets notified, it can perform an action defined in the manager
configuration on the concerned object such as :

- starting the services of the concerned object
- stopping the services of the concerned object
- create communication connection between new objects and/or new services

Implementation
--------------

Updater
~~~~~~~

An updater implementation must inherit from the ``::ctrlSelection::IUpdaterSrv`` service.

In the example below, an updater is used to manage a ``::fwData::Reconstruction`` object identified with 
the ``reconstruction`` key in a selection composite. This ``::fwData::Reconstruction`` is stored in a
``::fwMedData::ModelSeries`` and we used a specific updater to listen signals and manage the structure.

The updater provites slots to react on object/service signals.


Example
********

For example, the updater ``::ctrlSelection::SObjFromSlots`` provides the following slots :

- ``add(object)``: add the given object in the composite with the configured key
- ``swapObj(object)``: swap the given object in the composite with the configured key
- ``addOrSwap(object)``: if the configured key exists in the composote, the object is swapped, else it is added
- ``remove()``: remove the object with the configured key from the composite
- ``removeIfPresent()``: remove the object if the configured key exists in the composite

Updater configuration example:

.. code-block:: xml

    <object id="model_uid" type="::fwMedData::ModelSeries">
        <service uid="${GENERIC_UID}_listOrganEditor" impl="::uiMedData::editor::SModelSeriesList" 
            type="::gui::editor::IEditor" autoConnect="yes" />
    </object>

    <object type="::fwData::Composite">
        <service uid="myUpdater" impl="::ctrlSelection::updater::SObjFromSlot" type="::ctrlSelection::IUpdaterSrv">
            <compositeKey>reconstruction</compositeKey><!-- key of the updated object -->
        </service>
    </object>

    <!-- connect updater to listen the reconstruction selection -->
    <connect>
        <signal>listOrganEditor/reconstructionSelected</signal>
        <slot>myUpdater/addOrSwap</slot>
    </connect>


Manager
~~~~~~~

Managers inherit from ``::ctrlSelection::IManagerSrv``. As explained earlier, they manage tasks or services on objects 
which appear or disappear from the composite on which they are working. 

Example
********

For instance, the XML configuration below manages a GUI to configure rendering options of a reconstruction from a 
reconstruction list thanks to the ``::ctrlSelection::manager::SwapperSrv`` service. In this configuration, the manager
updates the services attached to the ``rec`` object each time it is added, removed or swapped.

Manager configuration example

.. code-block:: xml

    <object type="::fwData::Composite">
      <service uid="manager_uid" impl="::ctrlSelection::manager::SwapperSrv"
            type="::ctrlSelection::IManagerSrv" autoConnect="yes" >
            <mode type="dummy" />
            <config>
                <object id="rec" type="::fwData::Reconstruction">
                    <service uid="organMaterialEditor" impl="::uiReconstruction::OrganMaterialEditor" 
                        type="::gui::editor::IEditor" />
                    <service uid="representationEditor" impl="::uiReconstruction::RepresentationEditor" 
                        type="::gui::editor::IEditor" />
                </object>
        </config>
      </service>
    </object>


mode 
    The mode must be "stop", "dummy" or "startAndUpdate". 
    The mode "stop", used by default, starts the services when their attached object is added in the compsite 
    and stop and unregister the services when the object is deleted.
    The mode "dummy" doesn't stop the services when its attached object is deleted but swap it on a dummy object. 
    The mode "startAndUpdate" start and update the services when its attached object is added in the composite.
    
object
    It defines the objects and their services to manage.
    
    * **id**: the key of the object in the composite
    * **type**: the type of the object
    
    The services are declared as same as in the AppConfig.
    

connect (optional): 
    It allows to connect a signal to one or more slot(s). The signal and slots must be compatible.
    The signal uid is optional, if it is not defines, the signal is from the current managed object.
    
.. code-block:: xml

    <object type="::fwData::Composite">
        <service uid="manager_uid" impl="::ctrlSelection::manager::SwapperSrv"
            type="::ctrlSelection::IManagerSrv" autoConnect="yes" >
            <mode type="dummy" />
            <config>
                <object id="rec" type="::fwData::Reconstruction">
                
                    <!--  ....  services ....    -->
                
                    <connect>
                        <signal>object_uid/signal_name</signal>
                        <slot>service_uid/slot_name</slot>
                    </connect>

                    <connect>
                        <signal>signal_name</signal><!-- signal from recontruction "rec" -->
                        <slot>service_uid/slot_name</slot>
                    </connect>
                </object>
            </config>
        </service>
    <object>


proxy (optional):
    It allows to connect one or more signal(s) to one or more slot(s). The signals and slots must be compatible. 
    The signal uid is optional, if it is not defines, the signal is from the current managed object.
    
    channel:
        Name of the channel use for the proxy. 

.. code-block:: xml
     
     <object type="::fwData::Composite">
         <service uid="manager_uid" impl="::ctrlSelection::manager::SwapperSrv"
             type="::ctrlSelection::IManagerSrv" autoConnect="yes" >
             <mode type="dummy" />
             <config>
                 <object id="rec" type="::fwData::Reconstruction">
                 
                     <!--  ....  services ....    -->
                 
                     <proxy channel="myChannel">
                         <signal>object_uid/signal_name</signal>
                         <slot>service_uid/slot_name</slot>
                     </proxy>

                     <proxy channel="myOtherChannel">
                         <signal>signal_name</signal><!-- signal from recontruction "rec" -->
                         <slot>service_uid/slot_name</slot>
                     </proxy>
                 </object>
             </config>
         </service>
     <object>
     


