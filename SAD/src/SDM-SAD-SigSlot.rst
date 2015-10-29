.. _SigSlot:

Signal-slot communication
=========================

Overview
--------

"Signals and slots" is a language construct introduced in Qt [#]_
for communication between objects.

.. [#] http://wiki.qt.io/Qt_signal-slot_quick_start

The concept is that objects and services(explained in 2.3) can send signals containing event information which can be
received by other services using special functions known as slots.


FW4SPL implementation
---------------------

In the FW4SPL architecture, the library ``fwCom`` provides a set of tools
dedicated to communication. These communications are based on the signal and
slot concept.

``fwCom`` provides the following features :

-  function and method wrapping
-  direct slot calling
-  asynchronous slot calling
-  ability to work with multiple threads
-  auto-disconnection of slot and signals
-  arguments loss between slots and signals

Slots
-----

Slots are wrappers for functions and class methods that can be attached
to a ``fwThread::Worker``. The purpose of this class is to provide
synchronous and asynchronous mechanisms for method and function calling.

Slots have a common base class : SlotBase. This allows the storage of them in
the same container. Slots are designed such that they can be called, even where only the argument type is known.

Examples :

A slot wrapping the function sum, which is a function with
the signature int (int, int) :

.. code-block:: c++

    ::fwCom::Slot< int (int, int) >::sptr slotSum = ::fwCom::newSlot( &sum );

A slot wrapping the function start with signature void() of
the object ``a`` which class type is ``A`` :

.. code-block:: c++

    ::fwCom::Slot< void() >::sptr slotStart = ::fwCom::newSlot(&A::start, &a);

Execution of the slots using the run method :

.. code-block:: c++

    slotSum->run(40,2);
    slotStart->run();

Execution of the slots using the method call, which returns the result
of the execution :

.. code-block:: c++

    int result = slotSum->call(40,2);
    slotStart->call();

A slot declaration and execution, through a SlotBase :

.. code-block:: c++

    ::fwCom::Slot< size_t (std::string) > slotLen
            = ::fwCom::Slot< size_t (std::string) >::New( &len );
    ::fwCom::SlotBase::sptr slotBaseLen = slotLen;
    ::fwCom::SlotBase::sptr slotBaseSum = slotSum;
    slotBaseSum->run(40,2);
    slotBaseSum->run<int, int>(40,2);

    // This one needs the  explicit argument type
    slotBaseLen->run<std::string>("R2D2");
    result = slotBaseSum->call<int>(40,2);
    result = slotBaseSum->call<int, int, int>(40,2);
    result = slotBaseLen->call<size_t, std::string>("R2D2");

Signals
-------

Signals allow to perform grouped calls on slots. For this purpose, a signal
class provides a mechanism to connect slots.

Examples:

The following instruction declares a signal with a void signature.

.. code-block:: c++

    ::fwCom::Signal< void() >::sptr sig = ::fwCom::Signal< void() >::New();

The connection between a signal and a slot of the same information type:

.. code-block:: c++

    sig->connect(slotStart);

The following instruction will trigger the execution of all
slots connected to this signal:

.. code-block:: c++

    sig->emit();

It is possible to connect multiple slots with the same information type to
the same signal and trigger their simultaneous execution.

Signals can take several arguments as a signature which will trigger their connected slots
by passing the right arguments.

In the following example a signal is declared of type void(int, int). The signal is connected
to two different types of slot, void (int) and int (int, int).

.. code-block:: c++

    using namespace fwCom;
    Signal< void(int, int) >::sptr sig2 = Signal< void(int, int) >::New();
    Slot< int(int, int) >::sptr    slot1 = Slot< int(int, int) >::New(...);
    Slot< void(int) >::sptr        slot2 = Slot< void(int) >::New(...);

    sig2->connect(slot1);
    sig2->connect(slot2);

    sig2->emit(21, 42);

Here 2 points need to be highlighted :

-  A signal cannot return a value. Consequently their return type is void. 
   Thus, the return value of a slot, triggered by a signal, equally cannot be retrieved.
   
-  To successfully trigger a slot using a signal, the minimum requirement as to the number of arguments or 
   fitting argument types has to be given by the signal. In the last example the slot slot2 only 
   requires one argument of type int, but the signal is emitting two arguments of type int. 
   Because the signal signature fulfills the slot's argument number and argument type, the signal 
   can successfully trigger the slot slot2. The slot slot2 takes the first emitted argument which 
   fits its parameter (here 21, the second argument is ignored).


Disconnection
~~~~~~~~~~~~~

The disconnect method is called between one signal and one slot, to stop their existing connection. 
A disconnection assumes a signal slot connection. Once a signal slot connection is disconnected, it 
cannot be triggered by this signal. Both connection and disconnection of a signal slot connection can be 
done at any time.

.. code-block:: c++

    sig2->disconnect(slot1);
    sig2->emit(21, 42); // do not trigger slot1 anymore

The instructions above will cause the execution of slot2. Due to the disconnection between sig2 and slot1, 
the slot slot1 is not triggered by sig2.

Connection handling
~~~~~~~~~~~~~~~~~~~

The connection between a slot and a signal returns a connection handler:

.. code-block:: c++

    ::fwCom::Connection connection = signal->connect(slot);

Each connection handler provides a mechanism which allows a
signal slot connection to be disabled temporarily. The slot stays connected to the signal, but it will
not be triggered while the connection is blocked :

.. code-block:: c++

    ::fwCom::Connection::Blocker lock(connection);
    signal->emit();
    // 'slot' will not be executed while 'lock' is alive or until lock is
    // reset

Connection handlers can also be used to disconnect a slot and a signal
:

.. code-block:: c++

    connection.disconnect();
    // slot is not connected anymore

Auto-disconnection
~~~~~~~~~~~~~~~~~~

Slots and signals can handle an automatic disconnection :

-  on slot destruction : every signal slot connection to this slot will be destroyed
   
-  on signal destruction : every slot connection to the signal will be destroyed

All related connection handlers will be invalidated when an automatic
disconnection occurs.

Manage slots or signals in a class
----------------------------------

The library ``fwCom`` provides two helper classes to manage signals or slots in
a structure.

HasSlots
~~~~~~~~

The class ``HasSlots`` offers mapping between a key (string defining the slot name)
and a slot. ``HasSlots`` allows the management of many slots using a map. To use
this helper in a class, the class must inherit from ``HasSlots`` and must register the slots
in the constructor:

.. code-block:: c++

    struct ThisClassHasSlots : public HasSlots
    {
      typedef Slot< int()> GetValueSlotType;

      ThisClassHasSlots()
      {
          newSlot("sum", &SlotsTestHasSlots::getValue, this);
      }

      int sum(int a, int b)
      {
          return a+b;
      }

      int getValue()
      {
          return 4;
      }
    };

Then, slots can be used as below :

.. code-block:: c++

    ThisClassHasSlots obj;
    obj.slot("sum")->call<int>(5,9);
    obj.slot< ThisClassHasSlots::GetValueSlotType >("getValue")->call();

HasSignals
~~~~~~~~~~

The class ``HasSignals`` provides mapping between a key (string defining the signal name) and a signal.
``HasSignals`` allows the management of many signals using a map, similar to ``HasSlots``. To use this helper in a class, the class must inherit from
``HasSignals`` as seen below and must register signals in the constructor:

.. code-block:: c++

    struct ThisClassHasSignals : public HasSignals
    {
      typedef ::fwCom::Signal< void()> SignalType;

      ThisClassHasSignals()
      {
          newSignal< SignalType >("sig");
      }
    };

Then, signals can be used as below:

.. code-block:: c++

    ThisClassHasSignals obj;
    Slot< void()>::sptr slot = ::fwCom::newSlot(&anyFunction)
    obj.signal("sig")->connect( slot );
    obj.signal< SignalsTestHasSignals::SignalType >("sig")->emit();
    obj.signal("sig")->disconnect( slot );

Signals and slots used in objects and services
-------------------------------------------------------

Slots are used in both objects and services, whereas signals are only used in services. The abstract
class ``fwData::Object`` inherits from the ``HasSignals`` class as a basis to use signals :

.. code-block:: c++

    class Object : public ::fwCom::HasSignals
    {
      /// Key in m_signals map of signal m_sigObjectModified
      static const ::fwCom::Signals::SignalKeyType s_MODIFIED_SIG;
      //...

      /// Type of signal m_sigObjectModified
      typedef ::fwCom::Signal< void ( CSPTR( ::fwServices::ObjectMsg ) ) >
                    ObjectModifiedSignalType;

      /// Signal that emits an ObjectMsg when an object is modified
      ObjectModifiedSignalType::sptr m_sigObjectModified;

      Object()
      {
          m_sigObjectModified = newSignal< ObjectModifiedSignalType >(s_MODIFIED_SIG);
          //...
      }
    }

Moreover the abstract class ``fwService::IService`` inherits from the ``HasSlots`` class and the ``HasSignals`` class, as a basis to communicate through signals and slots. Actually, the methods ``start()``, ``stop()``, ``swap()`` and ``update()`` are all slots. Here is an extract with ``update()``: 

.. code-block:: c++

    class IService : public ::fwCom::HasSlots, public ::fwCom::HasSignals 
    {
      typedef ::boost::shared_future< void > SharedFutureType;
      
      /// Key in m_slots map of slot m_slotUpdate
      static const ::fwCom::Slots::SlotKeyType s_UPDATE_SLOT;

      /// Type of signal m_slotUpdate
      typedef ::fwCom::Slot<SharedFutureType()> UpdateSlotType;

      /// Slot to call update method
      UpdateSlotType::sptr m_slotUpdate;

      IService()
      {
          //...
          m_slotUpdate = newSlot( s_UPDATE_SLOT, &IService::update, this ) ;
          //...
      }
      
      //...
    }

      
To automatically connect object signals and service slots, it is possible to override the method
``IService::getObjSrvConnections()``. Please note that to be effective the attribute "autoconnect" 
of the service must be set to "yes" in the xml configuration (see :ref:`App-config`).
The default implementation of this method connect the ``s_MODIFIED_SIG`` object signal to the 
``s_UPDATE_SLOT`` slot.

.. code-block:: c++

    IService::KeyConnectionsType IService::getObjSrvConnections() const
    {
        KeyConnectionsType connections;
        connections.push_back( std::make_pair( ::fwData::Object::s_MODIFIED_SIG, s_UPDATE_SLOT ) );
        return connections;
    }

Object signals
------------------------

Objects have signals that can be used to inform of modifications.
The base class ``::fwData::Object`` has the following signals available.

=============================== =====================================================================================================
  Objects                       Available messages
=============================== =====================================================================================================
Object                          {``modified``, ``addedFields``, ``changedFields``, ``removedFields``}
=============================== =====================================================================================================

Thus all objects in FW4SPL can use the previous signals. Some object classes define extra signals.

=============================== =====================================================================================================
  Objects                       Available messages
=============================== =====================================================================================================
Composite                       {``addedObjects``, ``changedObjects``, ``removedObjects``}
Graph                           {``updated``}
Image                           {``bufferModified``, ``landmarkAdded``, ``landmarkRemoved``, ``landmarkDisplayed``, ``distanceAdded``, ``distanceRemoved``, ``distanceDisplayed``, ``sliceIndexModified``, ``sliceTypeModified``, ``visibilityModified``, ``transparencyModified``}
Mesh                            {``vertexModified``, ``pointColorsModified``, ``cellColorsModified``, ``pointNormalsModified``, ``cellNormalsModified``, ``pointTexCoordsModified``, ``cellTexCoordsModified``}
ModelSeries                     {``reconstructionsAdded``, ``reconstructionsRemoved``}
PlaneList                       {``planeAdded``, ``planeRemoved``, ``visibilityModified``}
Plane                           {``selected``}
PointList                       {``pointAdded``, ``pointRemoved``}
Reconstruction                  {``meshModified``, ``visibilityModified``}
ResectionDB                     {``resectionAdded``, ``safePartAdded``}
Resection                       {``reconstructionAdded``, ``pointTexCoordsModified``}
Vector                          {``addedObjects``, ``removedObjects``}
...                             ...
=============================== =====================================================================================================

Proxy
-----

The class ``::fwServices::registry::Proxy`` is a communication element and singleton in the architecture. 
It defines a proxy for
signal/slot connections. The proxy concept is used to declare
communication channels: all signals registered in a proxy's channel are
connected to all slots registered in the same channel. This concept is
useful to create multiple connections or when the slots/signals have not yet been created (possible in dynamic programs).

The following shows an example where one signal is connected to several slots:

.. code-block:: c++

    const std::string CHANNEL = "myChannel";

    ::fwServices::registry::Proxy::sptr proxy
        = ::fwServices::registry::Proxy::getDefault();

    ::fwCom::Signal< void() >::sptr sig = ::fwCom::Signal< void() >::New();

    ::fwCom::Slot< void() >::sptr slot1 = ::fwCom::newSlot( &myFunc1 );
    ::fwCom::Slot< void() >::sptr slot2 = ::fwCom::newSlot( &myFunc2 );
    ::fwCom::Slot< void() >::sptr slot3 = ::fwCom::newSlot( &myFunc3 );

    proxy->connect(CHANNEL, sig);

    proxy->connect(CHANNEL, slot1);
    proxy->connect(CHANNEL, slot2);
    proxy->connect(CHANNEL, slot3);

    sig->emit(); // All slots are called

