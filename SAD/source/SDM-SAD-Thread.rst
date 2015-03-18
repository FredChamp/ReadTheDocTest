Multithreading
=======================

Overview
--------

The multithreading paradigm has become more popular as efforts to further
exploit instruction level parallelism have stalled since the late 1990s. This
allowed the concept of throughput computing to re-emerge to prominence from the
more specialized field of transaction processing:

- Even though it is very difficult to further speed up a single thread or
  single program, most computer systems are actually multi-tasking among
  multiple threads or programs.
- Techniques that would allow speedup of the overall system throughput of all
  tasks would be a meaningful performance gain.

Some advantages include:

- If a thread gets a lot of cache misses, the other thread(s) can continue,
  taking advantage of the unused computing resources, which thus can lead to
  faster overall execution, as these resources would have been idle if only a
  single thread was executed.
- If a thread cannot use all the computing resources of the CPU (because
  instructions depend on each other's result), running another thread can avoid
  leaving these idle.
- If several threads work on the same set of data, they can actually share
  their cache, leading to better cache usage or synchronization of its values.

Some criticisms of multithreading include:

- Multiple threads can interfere with each other when sharing hardware
  resources such as caches or translation look aside buffers (TLBs).
- Execution times of a single thread are not improved but can be degraded, even
  when only one thread is executing. This is due to slower frequencies and/or
  additional pipeline stages that are necessary to accommodate thread-switching
  hardware.
- Hardware support for multithreading is more visible to software, thus
  requiring more changes to both application programs and operating systems
  than multiprocessing.
- Thread scheduling is also a major problem in multithreading.

Michael K. Gschwind, et al. [#]_ 

.. [#]  Michael K. Gschwind, Valentina Salapura. 2011. Using Register Last Use Infomation to Perform Decode-Time Computer Instruction Optimization US 20130086368 A1 [Patent]. http://www.google.com/patents/US20130086368



Worker and Timer
----------------

In the FW4SPL architecture, the library ``fwThread`` provides few tools to execute
asynchronous tasks on different threads.

In this library, the class ``Worker`` creates and manages a task loop. The default
implementation creates a loop in a new thread. Some tasks can be posted on the
worker and will be executed on the managed thread. When the worker is stopped,
it waits for the last task to be processed and stops the loop.

.. code:: cpp

    ::fwThread::Worker::sptr worker = ::fwThread::Worker::New();

    ::boost::packaged_task<void> task( ::boost::bind( &myFunction ) );
    ::boost::future< void > future = task.get_future();
    ::boost::function< void () > f = moveTaskIntoFunction(task);

    worker->post(f);

    future.wait();
    worker->stop();

The Timer class provides single-shot or repetitive timers. A Timer triggers a
function once after a delay, or periodically, inside the worker loop. The delay
or the period is defined by the duration attribute.

.. code:: cpp

    ::fwThread::Worker::sptr worker = ::fwThread::Worker::New();

    ::fwThread::Timer::sptr timer = worker->createTimer();

    timer->setFunction(  ::boost::bind( &myFunction)  );

    ::boost::chrono::milliseconds duration
            = ::boost::chrono::milliseconds(100) ;
    timer->setDuration(duration);

    timer->start();
    //...
    timer->stop();

    worker->stop();

Mutex
-----

The namespace ``fwCore::mt`` provides common foundations for multithreading in
FW4SPL, especially tools to manage mutual exclusions. In computer science,
mutual exclusion refers to the requirement of ensuring that two concurrent
threads are not in a critical section at the same time, it is a basic
requirement in concurrency control, to prevent race conditions. Here, a
critical section refers to a period when the process accesses a shared
resource, such as shared memory. A lock system is designed to enforce a mutual
exclusion concurrency control policy.

Currently, FW4SPL uses Boost Thread library which allows the use of multiple
execution threads with shared data, keeping the C++ code portable.
``fwCore::mt`` defines a few typedef over Boost:

.. code:: cpp

    namespace fwCore
    {
    namespace mt
    {

    typedef ::boost::mutex Mutex;
    typedef ::boost::unique_lock< Mutex > ScopedLock;

    typedef ::boost::recursive_mutex RecursiveMutex;
    typedef ::boost::unique_lock< RecursiveMutex > RecursiveScopedLock;

    /// Defines a single writer, multiple readers mutex.
    typedef ::boost::shared_mutex ReadWriteMutex;
    /**
    * @brief Defines a lock of read type for read/write mutex.
    * @note Multiple read lock can be done.
    */
    typedef ::boost::shared_lock< ReadWriteMutex > ReadLock;
    /**
    * @brief Defines a lock of write type for read/write mutex.
    * @note Only one write lock can be done at once.
    */
    typedef ::boost::unique_lock< ReadWriteMutex > WriteLock;
    /**
    * @brief Defines an upgradable lock type for read/write mutex.
    * @note Only one upgradable lock can be done at once but there
            may be multiple read lock.
    */
    typedef ::boost::upgrade_lock< ReadWriteMutex > ReadToWriteLock;
    /**
    * @brief Defines a write lock upgraded from ReadToWriteLock.
    * @note Only one upgradable lock can be done at once but there
            may be multiple read lock.
    */
    typedef ::boost::upgrade_to_unique_lock< ReadWriteMutex >
                UpgradeToWriteLock;

    } //namespace mt
    } //namespace fwCore


Multithreading and communication
---------------------------------

Asynchronous call
~~~~~~~~~~~~~~~~~

Slots are able to work with ``fwThread::Worker``. If a Slot has a Worker, each
asynchronous execution request will be run in its worker, otherwise
asynchronous requests can not be satisfied without specifying a worker.

Setting worker example:

.. code:: cpp

    ::fwCom::Slot< int (int, int) >::sptr slotSum
            = ::fwCom::newSlot( &sum );
    ::fwCom::Slot< void () >::sptr slotStart
            = ::fwCom::newSlot( &A::start, &a );

    ::fwThread::Worker::sptr w = ::fwThread::Worker::New();
    slotSum->setWorker(w);
    slotStart->setWorker(w);


``asyncRun`` method returns a boost::shared_future< void >, that makes it possible
to wait for end-of-execution.

.. code:: cpp

    ::boost::future< void > future = slotStart->asyncRun();
    // do something else ...
    future.wait(); //ensures slotStart is finished before continuing

``asyncCall`` method returns a ``boost::shared_future< R >`` where R is the return
type. This allows facilitates waiting for end-of-execution and retrieval of the computed value.

.. code:: cpp

    ::boost::future< int > future = slotSum->asyncCall();
    // do something else ...
    future.wait(); //ensures slotStart is finished before continuing
    int result = future.get();

In this case, the slots asynchronous execution has been *weakened*. For an async call/run
pending in a worker queue, it means that :

- if the slot is detroyed before the execution of this call, it will be
  canceled.
- if slot's worker is changed before the execution of this call, it will also
  be canceled.

Asynchronous emit
~~~~~~~~~~~~~~~~~

As slots can work asynchronously, triggering a Signal with asyncEmit results in
the execution of connected slots in their worker :

.. code:: cpp

    sig2->asyncEmit(21, 42);

The instruction above has the consequence of running each connected slot in its
own worker.

Note: Each connected slot must have a worker set to use asyncEmit.


Object-Service and Multithreading
----------------------------------

Object
~~~~~~

The architecture allows the writing of thread safe functions which manipulate objects
easily. Objects have their own mutex (inherited from ``fwData::Object``) to
control concurrent access from different threads. This mutex is available using the following method:

.. code:: cpp

    ::fwCore::mt::ReadWriteMutex & getMutex();

The namespace ``fwData::mt`` contains several helpers to lock objects for
multithreading:

- ``ObjectReadLock``: locks an object mutex on read mode.
- ``ObjectReadToWriteLock``:  locks an object mutex on upgradable mode.
- ``ObjectWriteLock``: locks an object mutex on exclusive mode.

The following example illustrates how to use these helpers:

.. code:: cpp

    ::fwData::String::sptr m_data = ::fwData::String::New();
    {
        // lock data to write
        ::fwData::mt::ObjectReadLock readLock(m_data);
    } // helper destruction, data is no longer locked


    {
        // lock data to write
        ::fwData::mt::ObjectWriteLock writeLock(m_data);

        // unlock data
        writeLock.unlock();

        // lock data to read
        ::fwData::mt::ObjectReadToWriteLock updrageLock(m_data);

        // unlock data
        updrageLock.unlock();

        // lock again data to read
        updrageLock.lock();

        // lock data to write
        updrageLock.upgrade();

        // lock data to read
        updrageLock.downgrade();

    } // helper destruction, data is no longer locked



Services
~~~~~~~~

The service architecture allows the writing of a thread-safe service by
avoiding the requirement of explicit synchronization. Each service has an associated
worker in which service methods are intended to be executed.

Specifically, all inherited ``IService`` methods (``start``, ``stop``,
``update``, ``receive``, ``swap``) are slots. Thus, the whole service life
cycle can be managed in a separate thread.

Since services are designed to be managed in an associated worker, the worker
can be set/updated by using the inherited method :

.. code:: cpp

    // Initializes m_associatedWorker and associates
    // this worker to all service slots
    void setWorker( ::fwThread::Worker::sptr worker );

    // Returns associate worker
    ::fwThread::Worker::sptr getWorker() const;

Since the signal-slot communication is thread-safe and
``IService::receive(msg)`` method is a slot, it is possible to attach a service
to a thread and send notifications to execute parallel tasks.

.. note::
    Some services use or require GUI backend elements. Thus, they can't be used
    in a separate thread. All GUI elements must be created and managed in the
    application main thread/worker.

