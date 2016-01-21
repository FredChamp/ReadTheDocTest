Installation for Linux
======================

Prerequisites for Linux users
--------------------------------

If not already installed:

#. Install `git <https://git-scm.com/>`_

#. Install `gcc <https://gcc.gnu.org/>`_ The minimal version required is 4.8 or `clang <http://clang.llvm.org/>`_ The minimal version required is 3.5

#. Install `Python 2.7 <https://www.python.org/downloads/>`_

#. Install `CMake <http://www.cmake.org/download/>`_ The minimal version required is 3.0

#. Install `Ninja <https://martine.github.io/ninja/>`_

Depending on which linux distribution you use, for example on Debian you can do:

.. code:: bash

    $ apt-get install build-essential ninja-build python2.7 git

Qt is an external library used in FW4SPL. For the successful compilation of Qt with FW4SPL, please see the following requirements:

- http://wiki.qt.io/Building_Qt_5_from_Git


FW4SPL installation
-------------------------

FW4SPL works with data separation for source, build and install data.
To prepare the development environment:

- Create your "Dev" directory

.. code:: bash

    $ mkdir Dev

- Create into "Dev" the source, build and install directories

.. code:: bash

    $ mkdir Dev/Src Dev/Build Dev/Install

- Create sub-folders to separate Debug and Release compilations

.. code:: bash

    $ mkdir Dev/Build/Debug Dev/Build/Release Dev/Install/Debug Dev/Install/Release

To prepare the third party environment:

- Create a third party folder (Deps)

.. code:: bash

    $ mkdir Deps

- Create into "Deps" the source, build and install directories

.. code:: bash

    $ mkdir Deps/Src Deps/Build Deps/Install

- Create sub-folders to separate Debug and Release compilations

.. code:: bash

    $ mkdir Deps/Build/Debug Deps/Build/Release Deps/Install/Debug Deps/Install/Release


.. _build_tools:

Build tools
~~~~~~~~~~~~

FW4SPL is a CMake project. That means, for each build target there is a CMakeLists that provides build parameters.
To configure you project you can use the ``cmake`` command from the build folder with the sources as arguments:

.. code:: bash

    $ cd Dev/Build/Debug
    $ ccmake ../../Src/fw4spl

if you want to use **Ninja** as build to tools, use the option ``-G Ninja``, as following:

.. code:: bash

    $ ccmake -G Ninja ../../Src/fw4spl

It is the same process for Deps and FW4SPL sources. It is recommended to use make to compile the deps.

Dependencies
~~~~~~~~~~~~~~

- Clone the repository into your source directory of Deps

.. code:: bash

    $ cd Deps/Src
    $ git clone https://github.com/fw4spl-org/fw4spl-deps.git fw4spl-deps

- Get into fw4spl-deps folder and update to the latest stable version

.. code:: bash
    $ cd fw4spl-deps
    $ git checkout fw4spl_0.10.2.2

- Get into your Build directory (Debug or Release) : here an example if you want to compile in DEBUG

.. code:: bash

    $ cd Deps/Build/Debug

- Call ccmake and point to the sources

.. code:: bash

    $ ccmake ../../Src/fw4spl-deps


To build the dependencies, you must configure the project with cmake into the Build folder

.. code:: bash

    $ cd ~/Dev/Deps/Build
    $ cmake ../Src/fw4spl-deps -DCMAKE_INSTALL_PREFIX=../Install -DCMAKE_BUILD_TYPE=Debug

Or open cmake gui editor, see :ref:`build_tools` instructions.

.. code:: bash

    $ ccmake ../Src/fw4spl-deps

Some CMake variables have to be change:

- *CMAKE_INSTALL_PREFIX*: set the install location.

- *CMAKE_BUILD_TYPE*: set the build type 'Debug' or 'Release'

.. image:: ../media/osx_cmake_binpkgs.png

Press configure (*[c]*) and generate (*[g]*) makefiles.

- Compile the FW4SPL dependencies with make in the console, it will automaticaly download, build and install each dependencies.

.. code:: bash

    $ make all

.. warning::
    Do NOT use ninja to compile the dependencies, it cause conflict with qt compilation.


Source
~~~~~~~~~~~~~~~~~

- Clone fw4spl repository into your source directory

.. code:: bash

    $ cd Dev/Src
    $ git clone https://github.com/fw4spl-org/fw4spl.git fw4spl

- Get into fw4spl folder and update to the latest stable version

.. code:: bash

    $ cd fw4spl
    $ git checkout fw4spl_0.10.2.2

- Get into your Build directory (Debug or Release) : here an example if you want to compile in DEBUG

.. code:: bash

    $ cd Dev/Build/Debug

- Call *ccmake* and point to the sources

To use make :

.. code:: bash

    $ ccmake ../../Src/fw4spl

To use ninja :

.. code:: bash

    $ ccmake -G Ninja ../../Src/fw4spl

- Change the following cmake arguments

    - *CMAKE_INSTALL_PREFIX*: set the install location (Dev/Install/Debug or Release)

    - *CMAKE_BUILD_TYPE*: set to DEBUG or RELEASE.

    - *EXTERNAL_LIBRARIES*: set the install path of the third part libraries.(ex : Deps/Install/Debug)

    - *PROJECT_TO_BUILD*: set the list of the projects you want to build (ex: VRRender, Tuto01Basic ...), each project should be separated by ";".

.. note::
    - If PROJECT_TO_BUILD is empty, all application will be compiled
    - If PROJECT_TO_INSTALL is empty, no application will be installed

.. image:: ../media/osx_cmake_fw4spl.png

Press configure (**[c]**) and generate (**[g]**) makefiles.

Then, build dependencies with ninja.

.. code:: bash

    $ ninja all

Launch an application
-------------------------

To build a specific or several applications the CMake argument ``PROJECTS_TO_BUILD`` can be set.
Use ``;`` so separate each application name.

After an successful compilation the application can be launched with the launcher program from FW4SPL.
Therefore the profile.xml of the application in the build folder has to be passed as argument to the launcher call in the console.

.. code:: bash

    $ bin/launcher Bundles/MyApplication_Version/profile.xml

Example:

.. code:: bash

    $ cd /Dev/Build
    $ bin/launcher Bundles/VRRender_0-9/profile.xml

Extensions
----------

**fw4spl** has two extension repositories:

-  `fw4spl-ext <https://github.com/fw4spl-org/fw4spl-ext/>`_: contains additional functionalities and proofs of concept
- `fw4spl-ar <https://github.com/fw4spl-org/fw4spl-ar/>`_: contains functionalities for augmented reality (video tracking, calibration)

Dependencies
~~~~~~~~~~~~

If you want to use this extension, you need to clone the deps repositories:

- `fw4spl-ext-deps <https://github.com/fw4spl-org/fw4spl-ext-deps.git>`_: contains the scripts to compile the external libraries used by fw4spl-ext

.. code:: bash

    $ cd ~/Dev/Deps/Src
    $ git clone https://github.com/fw4spl-org/fw4spl-ext-deps.git fw4spl-ext-deps
    $ cd fw4spl-ext-deps
    $ git checkout fw4spl_0.10.2.2

- `fw4spl-ar-deps <https://github.com/fw4spl-org/fw4spl-ar-deps.git>`_: contains the scripts to compile the external libraries used by fw4spl-ar

.. code:: bash

    $ cd ~/Dev/Deps/Src
    $ git clone https://github.com/fw4spl-org/fw4spl-ar-deps.git fw4spl-ar-deps
    $ cd fw4spl-ar-deps
    $ git checkout fw4spl_0.10.2.2

You must re-edit cmake configuration to add this repository:

.. code:: bash

    $ cd ~/Dev/Deps/Build
    $ ccmake .

Modify *ADDITIONAL_DEPS*: set the source location of fw4spl-ar-deps and fw4spl-ext-deps separated by ';'

.. code:: bash

    ~/Dev/Deps/Src/fw4spl-ext-deps/;~/Dev/Deps/Src/fw4spl-ar-deps/

Source
~~~~~~

If you want to use fw4spl extension, you need this repositories:

- `fw4spl-ext <https://github.com/fw4spl-org/fw4spl-ext.git>`_: extension of fw4spl repository, contains additional functionalities and proofs of concept

.. code:: bash

    $ cd Dev/Src
    $ git clone https://github.com/fw4spl-org/fw4spl-ext.git fw4spl-ext
    $ cd fw4spl-ext
    $ git checkout fw4spl_0.10.2.2

- `fw4spl-ar <https://github.com/fw4spl-org/fw4spl-ar.git>`_: another extension of fw4spl, contains functionalities for augmented reality (video tracking)

.. code:: bash

    $ cd ../../Build
    $ ccmake .

Modify *ADDITIONAL_PROJECTS*: set the source location of fw4spl-ar and fw4spl-ext separated by ';'

.. code:: bash

    ~/Dev/Src/fw4spl-ext/;~/Dev/Src/fw4spl-ar/

Recommended software
-------------------------

The following programs may be helpful for your developments:

- `Eclipse CDT <https://eclipse.org/cdt/>`_

- `QtCreator <https://www.qt.io/download-open-source/#section-2>`_
