Installation for Windows
======================

Prerequisites for Windows users
--------------------------------

If not already installed:

1. Install `Mercurial <http://mercurial.selenic.com/wiki/>`_

2. Optionally you can install `TortoiseHg <http://tortoisehg.bitbucket.org/>`_

3. Install `Visual Studio 2013 Community <https://www.visualstudio.com/en-us/products/visual-studio-community-vs.aspx>`_

4. Install `Python 2.7 <https://www.python.org/downloads/>`_

5. Install `CMake <http://www.cmake.org/download/>`_

6. Install `jom <http://wiki.qt.io/Jom>`_

7. Install `ninja <https://github.com/martine/ninja/releases>`_

Qt is an external library used in FW4SPL. For the successful compilation of Qt for FW4SPL, please see the following requirements:

- http://wiki.qt.io/Building_Qt_5_from_Git



FW4SPL installation
-------------------------

Good practice in FW4SPL recommend to separate source files, build and install folders. 
So to prepare the development environment:

* Create a development folder (Dev)

* Create a build folder (Dev\\Build)

    * Add a sub folder for Debug and Release.

* Create a source folder (Dev\\Src)

* Create a install folder (Dev\\Install)

    * Add a sub folder for Debug and Release.

To prepare the third party environment:

* Create a third party folder (BinPkgs)

* Create a build folder (BinPkgs\\Build)

    * Add a sub folder for Debug and Release.

* Create a source folder (BinPkgs\\Src)

* Create an install folder (BinPkgs\\Install)

    * Add a sub folder for Debug and Release.

.. .. image:: media/Directories.png

* Set environment for a x64 version.
  For compile BinPkgs and sources, you must use the 'VS2013 x64 Native Tools Command Prompt' 

Dependencies
~~~~~~~~~~~~~~~~~

.. warning:: Be sure to be in the 'VS2013 x64 Native Tools Command Prompt'

* `Clone <http://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository#Cloning-an-Existing-Repository>`_ the three following repositories in the (BinPkgs) source folder:

    * `fw4spl-deps <https://github.com/fw4spl-org/fw4spl-deps.git>`_

    * `fw4spl-ar-deps <https://github.com/fw4spl-org/fw4spl-ar-deps.git>`_

    * `fw4spl-ext-deps <https://github.com/fw4spl-org/fw4spl-ext-deps.git>`_

* Update the cloned repositories to the used version. 

.. note:: Make sure that CMake is set as environment variable. 

* Call the cmake-gui

* During Configure, choose the generator 'NMake Makefiles JOM'. 

.. note:: make sure the generator JOM are set in your PATH.

* Set the following arguments:

    * *ADDITIONAL_PROJECTS*: set the source location of fw4spl-ar-deps and fw4spl-ext-deps

    * *CMAKE_INSTALL_PREFIX*: set the install location.
    * *CMAKE_BUILD_TYPE*: set to Debug or Release

* Generate the code. 

* Compile the FW4SPL dependencies with jom in the console (e.g. jom all, jom qt, etc).

Source
~~~~~~

.. warning:: Be sure to be in the 'VS2013 x64 Native Tools Command Prompt'
    
* `Clone <http://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository#Cloning-an-Existing-Repository>`_ the three following repositories in the (Dev) source folder:

    * `fw4spl <https://github.com/fw4spl-org/fw4spl.git>`_

    * `fw4spl-ar <https://github.com/fw4spl-org/fw4spl-ar.git>`_

    * `fw4spl-ext <https://github.com/fw4spl-org/fw4spl-ext.git>`_

* Update the cloned repositories to the used version. 

.. note:: Make sure that CMake is in your PATH. 

* Call the cmake-gui.

* During Configure, choose the generator ('NMake Makefiles JOM' for compile BinPkgs or 'Ninja' for compile FW4SPL sources) 

.. note:: make sure the generator Ninja and JOM are set in your PATH.

* Set the following arguments:

    * *ADDITIONAL_PROJECTS*: set the source location of fw4spl-ar and fw4spl-ext

    * *CMAKE_INSTALL_PREFIX*: set the install location.

    * *EXTERNAL_LIBRARIES*: set the install path of the third part libraries.

    * *CMAKE_BUILD_TYPE*: set to Debug or Release

    * *PROJECT_TO_BUILD* set the name of the application to build (See Dev\Src\Apps)

    .. note:: If PROJECT_TO_BUILD is empty, all application will be compile

    * *PROJECT_TO_INSTALL* set the name of the application to install 

    .. note:: If PROJECT_TO_BUILD is empty, all application will be compile
    
.. warning:: Make sure the arguments concerning the compiler (advanced arguments) point to Visual Studio.

* Generate the code. 

* Compile the FW4SPL source code with ninja in the console. 

.. note:: it is possible to generate eclipse project with CMake. You just have to check ECLIPSE_PROJECT.

Launch an application
-------------------------

After an successful compilation the application can be launched with the launcher.exe from FW4SPL. 
Therefore the profile.xml of the application in the build folder has to be passed as argument. 

.. note:: Make sure that the external libraries directory is set to the path (set PATH=<FW4SPL Binpkgs path>\\Debug\\bin;<FW4SPL Binpkgs path>\\Debug\\x64\\vc12\\bin;%PATH%).

.. image:: ../media/launchApp.png

Recommended software
-------------------------

The following programs may be helpful for your developments:

* `Eclipse CDT <https://eclipse.org/cdt/>`_: Eclipse is a multi-OS Integrated Development Environment (IDE) for computer programming. 
* `Notepad++ <http://notepad-plus-plus.org/>`_: Notepad++ is a free source code editor, which is designed with syntax highlighting functionality. 
* `ConsoleZ <https://github.com/cbucher/console/wiki/Downloads>`_: ConsoleZ is an alternative command prompt for Windows, adding more capabilities to the default Windows command prompt. To compile FW4SPL with the console the windows command prompt has to be set in the tab settings. 

   
