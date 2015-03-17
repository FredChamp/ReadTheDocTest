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

.. code:: c++

    ::fwCom::Slot< int (int, int) >::sptr slotSum = ::fwCom::newSlot( &sum );

A slot wrapping the function start with signature void() of
the object ``a`` which class type is ``A`` :

.. code:: c++

    ::fwCom::Slot< void() >::sptr slotStart = ::fwCom::newSlot(&A::start, &a);

Execution of the slots using the run method :

.. code:: c++

    slotSum->run(40,2);
    slotStart->run();

Execution of the slots using the method call, which returns the result
of the execution :

.. code:: c++

    int result = slotSum->call(40,2);
    slotStart->call();

A slot declaration and execution, through a SlotBase :

.. code:: c++

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

.. code:: c++

    ::fwCom::Signal< void() >::sptr sig = ::fwCom::Signal< void() >::New();

The connection between a signal and a slot of the same information type:

.. code:: c++

    sig->connect(slotStart);

The following instruction will trigger the execution of all
slots connected to this signal:

.. code:: c++

    sig->emit();

It is possible to connect multiple slots with the same information type to
the same signal and trigger their simultaneous execution.

Signals can take several arguments as a signature which will trigger their connected slots
by passing the right arguments.

In the following example a signal is declared of type void(int, int). The signal is connected
to two different types of slot, void (int) and int (int, int).

.. code:: c++

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

.. code:: c++

    sig2->disconnect(slot1);
    sig2->emit(21, 42); // do not trigger slot1 anymore

The instructions above will cause the execution of slot2. Due to the disconnection between sig2 and slot1, 
the slot slot1 is not triggered by sig2.

Connection handling
~~~~~~~~~~~~~~~~~~~

The connection between a slot and a signal returns a connection handler:

.. code:: c++

    ::fwCom::Connection connection = signal->connect(slot);

Each connection handler provides a mechanism which allows a
signal slot connection to be disabled temporarily. The slot stays connected to the signal, but it will
not be triggered while the connection is blocked :

.. code:: c++

    ::fwCom::Connection::Blocker lock(connection);
    signal->emit();
    // 'slot' will not be executed while 'lock' is alive or until lock is
    // reset

Connection handlers can also be used to disconnect a slot and a signal
:

.. code:: c++

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

.. code:: c++

    struct ThisClassHasSlots : public HasSlots
    {
      typedef Slot< int()> GetValueSlotType;

      ThisClassHasSlots()
      {
          GetValueSlotType::sptr slotGetValue
                = ::fwCom::newSlot( &SlotsTestHasSlots::getValue, this );
          HasSlots::m_slots("sum", &SlotsTestHasSlots::sum, this)
                           ("getValue", slotGetValue );
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

.. code:: c++

    ThisClassHasSlots obj;
    obj.slot("sum")->call<int>(5,9);
    obj.slot< ThisClassHasSlots::GetValueSlotType >("getValue")->call();

HasSignals
~~~~~~~~~~

The class ``HasSignals`` provides mapping between a key (string defining the signal name) and a signal.
``HasSignals`` allows the management of many signals using a map, similar to ``HasSlots``. To use this helper in a class, the class must inherit from
``HasSignals`` as seen below and must register signals in the constructor:

.. code:: c++

    struct ThisClassHasSignals : public HasSignals
    {
      typedef ::fwCom::Signal< void()> SignalType;

      ThisClassHasSignals()
      {
          SignalType::sptr signal = SignalType::New();
          HasSignals::m_signals("sig", signal);
      }
    };

Then, signals can be used as below:

.. code:: c++

    ThisClassHasSignals obj;
    Slot< void()>::sptr slot = ::fwCom::newSlot(&anyFunction)
    obj.signal("sig")->connect( slot );
    obj.signal< SignalsTestHasSignals::SignalType >("sig")->emit();
    obj.signal("sig")->disconnect( slot );

Signals and slots used in objects and services
-------------------------------------------------------

Slots are used in both objects and services, whereas signals are only used in services. The abstract
class ``fwData::Object`` inherits from the ``HasSignals`` class as a basis to use signals :

.. code:: c++

    class Object : public ::fwCom::HasSignals
    {
      /// Key in m_signals map of signal m_sigObjectModified
      static const ::fwCom::Signals::SignalKeyType s_OBJECT_MODIFIED_SIG;

      /// Type of signal m_sigObjectModified
      typedef ::fwCom::Signal< void ( CSPTR( ::fwServices::ObjectMsg ) ) >
                    ObjectModifiedSignalType;

      /// Signal that emits an ObjectMsg when an object is modified
      ObjectModifiedSignalType::sptr m_sigObjectModified;

      Object()
      {
          m_sigObjectModified = ObjectModifiedSignalType::New();
          m_signals( s_OBJECT_MODIFIED_SIG,  m_sigObjectModified);
      }
    }

Moreover the abstract class ``fwService::IService`` inherits from the ``HasSlots`` class and the ``HasSignals`` class, as a basis to communicate through signals and slots:

.. code:: c++

    class IService : public ::fwCom::HasSlots, public ::fwCom::HasSignals 
    {
      /// Key in m_slots map of slot m_slotReceive
      static const ::fwCom::Slots::SlotKeyType s_RECEIVE_SLOT;

      /// Type of signal m_slotReceive
      typedef ::fwCom::Slot<void(ObjectMsg::csptr)> ReceiveSlotType;

      /// Slot to call receive method
      ReceiveSlotType::sptr m_slotReceive;

      IService()
      {
          m_slotReceive  = ::fwCom::newSlot( &IService::receive   , this ) ;
          ::fwCom::HasSlots::m_slots( s_RECEIVE_SLOT , m_slotReceive )
      }
    }

According to the design, the ``s_OBJECT_MODIFIED_SIG``
object signal is connected to all ``s_RECEIVE_SLOT`` slots of its associated services (object service relation).
When a service modifies its associated object, the service emits an ``s_OBJECT_MODIFIED_SIG``
signal from the object in order to notify any service working on the modified
object through the receive method.

An other way to communicate between objects and services is
to split each modification type into different signals and to
create different slots in the services. In this case, the method
``IService::getObjSrvConnections()`` and the helper
``::fwServices::helper::SigSlotConnection`` provide few tools to
connect/disconnect signals/slots between objects/services.


Proxy
-----

The class ``::fwServices::registry::Proxy`` is a communication element and singleton in the architecture. 
It defines a proxy for
signal/slot connections. The proxy concept is used to declare
communication channels: all signals registered in a proxy's channel are
connected to all slots registered in the same channel. This concept is
useful to create multiple connections or when the slots/signals have not yet been created (possible in dynamic programs).

The following shows an example where one signal is connected to several slots:

.. code:: c++

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

Object messages
------------------------

The communication system called *communication channel system* used in the former versions of FW4SPL, was replaced by the signal slot communication system. As a result of this replacement, object messages were introduced. With each object modification, a message is sent informing
services that an object modification has occurred.
The signals and slots use a message parameter to store information about the object modification or to
specialize the message from others. The library ``fwComEd`` contains all message
structures which can be used to communicate object modifications. As shown in the table below,
several messages are available for each object.

=============================== =====================================================================================================
  Objects                       Available messages
=============================== =====================================================================================================
Acquisition                     {``ADD_RECONSTRUCTION``, ``VISIBILITY``, ``NEW_RECONSTRUCTION_SELECTED``}
Boolean                         {``VALUE_IS_MODIFIED``}
Camera                          {``NEW_CAMERA``, ``CAMERA_MOVING``}
Color                           {``VALUE_IS_MODIFIED``}
Composite                       {``MODIFIED_FIELDS``, ``ADDED_FIELDS``, ``REMOVED_FIELDS``, ``SWAPPED_FIELDS``}
Float                           {``VALUE_IS_MODIFIED``}
Graph                           {``NEW_GRAPH``, ``ADD_NODE``, ``REMOVE_NODE``, ``ADD_EDGE``, ``REMOVE_EDGE``, ``SELECTED_NODE``,
                                ``UNSELECTED_NODE``, ...}
Image                           {``NEW_IMAGE``, ``BUFFER``, ``MODIFIED``, ``DIMENSION``, ``SPACING``, ``REGION``, ``PIXELTYPE``,
                                ``TRANSFERTFUNCTION``, ...}
Integer                         {``VALUE_IS_MODIFIED``}
Interaction                     {``MOUSE_LEFT_UP``, ``MOUSE_RIGHT_UP``, ``MOUSE_MIDDLE_UP``, ``MOUSE_WHEELFORWARD_UP``,
                                ``MOUSE_WHEELBACKWARD_UP``, ...}
Location                        {``LOCATION_IS_MODIFIED``}
Material                        {``MATERIAL_IS_MODIFIED``}
Model                           {``NEW_MODEL``}
PatientDB                       {``NEW_PATIENT``, ``ADD_PATIENT``, ``CLEAR_PATIENT``, ``NEW_IMAGE_SELECTED``, ``NEW_LOADED_PATIENT``,
                                ``NEW_RESECTION_SELECTED``}
Patient                         {``NEW_PATIENT``, ``NEW_MATERIAL_FOR_RECONSTRUCTION``}
PlaneList                       {``ADD_PLANE``, ``REMOVE_PLANE``, ``PLANELIST_VISIBILITY``,
                                ``PLANELIST_MODIFIED``, ``DESELECT_ALL_PLANES``}
Plane                           {``PLANE_MODIFIED``, ``START_PLANE_INTERACTION``, ``DESELECT_PLANE``,
                                ``WAS_SELECTED``, ``WAS_DESELECTED``}
PointList                       {``ELEMENT_MODIFIED``, ``ELEMENT_ADDED``, ``ELEMENT_REMOVED``}
Point                           {``POINT_IS_MODIFIED``, ``START_POINT_INTERACTION``}
Reconstruction                  {``MESH``, ``VISIBILITY``}
ResectionDB                     {``NEW_RESECTIONDB_SELECTED``, ``RESECTIONDB_SELECTED``, ``NEW_RESECTION_SELECTED``,
                                ``NEW_SAFE_PART_SELECTED``, ...}
Resection                       {``ADD_RECONSTRUCTION``, ``VISIBILITY``, ``NEW_RECONSTRUCTION_SELECTED``, ``MODIFIED``}
Spline                          {``NEW_SPLINE``}
String                          {``VALUE_IS_MODIFIED``}
Tag                             {``TAG_IS_MODIFIED``}
...                             ...
=============================== =====================================================================================================
