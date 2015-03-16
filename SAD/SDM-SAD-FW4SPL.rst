******************************************
Software Architecture Description (SAD)
******************************************

General
========

Introduction
------------

The framework FW4SPL (FrameWork for Software Production) is an open-source 
framework, developed by IRCAD (research institute against cancer and disease). 
The principle of FW4SPL is the fast and easy creation of applications, mainly 
in the medical field. Therefore it provides features like digital image
processing in 2D and 3D, visualization or simulation of medical interactions. 
To build an application with FW4SPL there are no programming skills required. 
By writing a simple XML the users can design their own application.
 
FW4SPL is built on component-based architecture composed of C++ libraries. 
The three main concepts of the architecture, explained in the following sections, are:

-  object-service concept
-  component approach
-  signal-slot communication

The framework is multi-platform and runs under Windows, Linux and MacOS. 
The programming language of the framework is C++.
This document will introduce the general architecture of FW4SPL.

Annexes
-------

-  *Srclib list:* this document lists all libraries with a brief description.
-  *Object list:* this document lists all data with a brief description.
-  *Service list:* this document lists all services and bundles with a brief description.
-  *Third party:* this document contains a description of libraries used to
   support this architecture and its functions.
-  *OSR diagram:* this document introduces how to represent an application
   configuration as a diagram.


Object-Service concept
======================

.. include:: SDM-SAD-ObjService.rst


Signal-slot communication
=========================

.. include:: SDM-SAD-SigSlot.rst

App-config
=======================

.. include:: SDM-SAD-App-config.rst

.. [TODO]Activities
.. =======================
.. .. include:: SDM-SAD-Activities.rst

Multithreading
=======================

.. include:: SDM-SAD-Thread.rst

Serialization
=======================

.. include:: SDM-SAD-Serialization.rst

.. [TODO]Environment management
.. ============================
.. .. include:: SDM-SAD-Env.rst

.. [TODO]Binary packages
.. =======================
.. .. include:: SDM-SAD-bp.rst

.. [TODO]Memory management
.. =======================
.. .. include:: SDM-SAD-memory.rst

Medical patient folder
============================

.. include:: SDM-SAD-PatientFolder.rst

.. [TODO]Generic scene
.. =======================
.. .. include:: SDM-SAD-GenericScene.rst

Manager and updater services
==================================

.. include:: SDM-SAD-Manager.rst

.. [TODO]Progress bar
.. =======================
.. .. include:: SDM-SAD-ProgressBar.rst

.. [TODO]Software license
.. ======================
.. .. include:: SDM-SAD-License.rst

.. [TODO]Log
.. =========
.. .. include:: SDM-SAD-Log.rst

.. [TODO]Application and launcher
.. ===============================
.. .. include:: SDM-SAD-Application.rst

Component-based software
==============================

.. include:: SDM-SAD-Component.rst

Graphical User Interface
========================

.. include:: SDM-SAD-GUI.rst

