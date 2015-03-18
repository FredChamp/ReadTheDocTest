********************************
Frequently Asked Questions (FAQ)
********************************

What is fw4spl?
===============

The framework FW4SPL (FrameWork for Software Production) is an open-source framework, developed by IRCAD (research institute against cancer and disease). The principle of FW4SPL is the fast and easy creation of applications, mainly in the medical field. Therefore it provides features like digital image processing in 2D and 3D, visualization or simulation of medical interactions. To build an application with FW4SPL there are no programming skills required. By writing a simple XML the users can design their own application.

What does fw4spl mean?
======================

FW4SPL means FrameWork for Software Production Line. It is also called F4S ("forces").

What are the features of fw4spl?
=======================================

The framework is built around the notion of component (bundle). To build an application with FW4SPL there are no programming skills required. By writing a simple XML the users can design their own application.

FW4SPL has a component-based architecture composed of C++ libraries.
There are three main concepts in the architecture:
- object-service concept
- component approach
- signal-slot communication


Which platforms does fw4spl run on?
===================================

This framework can run under Windows, Linux and MacOS and we are working on the Android part.

Where can I find applications developed with fw4spl ?
======================================================

Some tutorials are provided with the framework and you can also build VR-Render, a free visualization software.

Which prerequiste do I need to develop bundle?
===============================================

You must have a good knowledge in C++. Concerning the configuration files, they are written in XML.

What are the BinPkgs?
======================

The BinPkgs (binary packages) contain all the extern libraries needed by fw4spl. For each BinPkg, a CMakeLists provides the OS specific instructions to build it . They can be downloaded on https://github.com/fw4spl-org/fw4spl-deps

Is it difficult to compile an application with fw4spl?
======================================================

No, it isn't. You just have to compile all the bundles and libraries used by the application.

Why does fw4spl provide a launcher?
===================================

The launcher is used to create the entry point of the application. It parses the profile and configuration xml file to build it.

How can I debug my program ?
=============================

First, you can change the log level of a sub-project in the CMake configuration.

The allowed values are : ['trace', 'debug', 'info', 'error', 'fatal', 'warning', 'disable']. the value 'trace' gives me the maximun of log, 'disable' disables log.

   **note a** : Printing many log messages ( by activating trace on all sub-projects for ex. ) can be very time consuming for the application.

    **note b** : Under windows system, log messages are saved on filesystem in SLM.log file, in the working directory.

Secondly, you can debug your application using gdb (Linux/Mac) or Visual Studio (Windows) and compiling your application in Debug mode

    **note a** : you can use gdb like this "LD_LIBRARY_PATH=./lib gdb -arg bin/launcher Bundles/myApp/myProfile.xml", and press "r" for run the program

    **note b** : you can use under gdb the command "catch throw" hence gdb will stop near the error
    **note c** : Documentation to learn using gdb : http://www.cs.tau.ac.il/lin-club/lecture-notes/GDB_Linux_telux.pdf
    
Thirdly, you can manage the program complexity by reducing the number of activated components (in profile.xml) and the number of created services (in config.xml) to better localize errors.

Fourthly, verify that your profile.xml / plugin.xml and each bundle plugin.xml are well-formed, by using xmllint (command line tool provided by libxml2).

I have an assertion/fatal message when I launch my program, any idea to correct the problem ?
===================================================================================================

First, you can read the output message :) and try to solve the problem.
In many cases, there are two kind of problems. The program fails to :
    - create the service given in configuration In this case, four reasons are possibles :
    
        - the name of service implementation in config.xml contains mistakes
        - the bundle that contains this service is not activated in the profile
        - the bundle plugin.xml, that contains this service, not declares the     service or the declaration contains mistakes.
        - the service is not register in the Service Factory (forget of macro REGISTER_SERVICE(...) in file .cpp) 
        
    - manage the configuration of service. In this case, the implementation code in .cpp file ( generally configuring() method of service ) does not correspond to description code in config.xml ( Missing arguments, or not well-formed, or mistakes string parameters ).

If I use fw4spl, do I need wrap all my data ?
=============================================

The first question is to know if the data is on center of application:

    - Need you to shared data between few bundles ?
    - Need you to attach services on this data ?

        - If the answer is no, you don't need to wrap your data. 
        - Otherwise, you need to have an object that inherits of ::fwData::Object.

    In this last case, do you need shared this object between different services which use different libraries, ex for Object Image : itk::Image vs vtkImage ?

        - If the answer is yes, you need create a new object like fwData::Image and a wrapping with fwData::Image<=>itk::Image and fwData::Image<=>vtkImage.
        - Otherwise, you can just encapsulated an itk::Image in fwData::Image and create an accessor on it. ( however, this kind of choice implies that all applications that use fwData::Image need itk library for running. )
