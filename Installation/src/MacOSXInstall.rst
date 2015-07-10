Installation for MacOSX
======================

Prerequisites for MacOSX users
--------------------------------

If not already installed:

1. Install `Mercurial <http://mercurial.selenic.com/wiki/>`_ 

2. Optionally you can install `TortoiseHg <http://tortoisehg.bitbucket.org/>`_ 

4. Install `Python 2.7 <https://www.python.org/downloads/>`_ 

5. Install `CMake <http://www.cmake.org/download/>`_ 


.. tip::
    1. You can also install `Ninja <https://github.com/martine/ninja/releases>`_ instead of using **make**.

    2. For an easy install, you can use the `Hombrew project <http://brew.sh/>`_  to install missing packages.


FW4SPL installation
-------------------------

FW4SPL works with data separation for source, build and install data. 
To prepare the development environment:

- Create a development folder (Dev)

- Create a build folder (Dev\\Build)

- Create a source folder (Dev\\Src)

- Create a install folder (Dev\\Install)

To prepare the third party environment:

- Create a third party folder (BinPkgs)

- Create a build folder (BinPkgs\\Build)

- Create a source folder (BinPkgs\\Src)

- Create a install folder (BinPkgs\\Install)

.. _build_tools:

Build tools
~~~~~~~~~~~~

FW4SPL is a CMake project. That means, for each build target there is a CMakeLists that provides build parameters.
To configure you project you can use the ``cmake`` command from the build folder with the sources as arguments:
    
.. code:: bash

    ccmake /PATH/TO/fw4spl-deps

if you want to use **Ninja** as build to tools, use the option ``-G Ninja``, as following:

.. code:: bash

    ccmake -G Ninja /PATH/TO/fw4spl-deps

It is the same process for BinPkgs and FW4SPL sources.

Dependencies
~~~~~~~~~~~~~~~~~

For the third party libraries the three following repositories have to be `cloned <http://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository#Cloning-an-Existing-Repository>`_ in the (BinPkgs) source folder:

- `fw4spl-deps <https://github.com/fw4spl-org/fw4spl-deps.git>`_

- `fw4spl-ar-deps <https://github.com/fw4spl-org/fw4spl-ar-deps.git>`_

- `fw4spl-ext-deps <https://github.com/fw4spl-org/fw4spl-ext-deps.git>`_

To build dependencies see :ref:`build_tools` instructions.
Some CMake variables have to be change:

- *ADDITIONAL_PROJECTS*: set the source location of fw4spl-ar-deps and fw4spl-ext-deps

- *CMAKE_INSTALL_PREFIX*: set the install location.

.. image:: ../media/osx_cmake_binpkgs.png

Press configure (*[c]*) and generate (*[g]*) makefiles. Then, compile the FW4SPL dependencies with make or ninja in a terminal.

Source
~~~~~~~~~~~~~~~~~

For the FW4SPL source code the three following repositories have to be `cloned <http://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository#Cloning-an-Existing-Repository>`_ in the (Dev) source folder:

- `fw4spl <https://github.com/fw4spl-org/fw4spl.git>`_

- `fw4spl-ar <https://github.com/fw4spl-org/fw4spl-ar.git>`_

- `fw4spl-ext <https://github.com/fw4spl-org/fw4spl-ext.git>`_

To build soruces see :ref:`build_tools` instructions.
Some CMake variables have to be change:

- *ADDITIONAL_PROJECTS*: set the source location of fw4spl-ar and fw4spl-ext

- *CMAKE_INSTALL_PREFIX*: set the install location.

- *EXTERNAL_LIBRARIES*: set the install path of the third part libraries.

.. image:: ../media/osx_cmake_fw4spl.png

Press configure (**[c]**) and generate (**[g]**) makefiles. Then, build dependencies with make or ninja in a terminal.

example:
    ``make Qt`` or ``ninja Qt``


Launch an application
-------------------------

To build a specific or several applications the CMake argument ``PROJECTS_TO_BUILD`` can be set.

.. tip::
    Use ``;`` so separate each application name.
    
After an successful compilation the application can be launched with the launcher program from a terminal. 
Therefore the profile.xml of the application in the build folder has to be passed as argument to the launcher:

.. code:: bash

    bin/launcher Bundles/MyApplicationAndVersion/profile.xml)

.. note:: 

    To generate the projects in release, the following instruction has to be change:
    - Change CMake argument ``CMAKE_BUILD_TYPE`` to release
    - Set the ``EXTERNAL_LIBRARIES`` to the release install folder of dependencies

Recommended softwares
-------------------------

The following programs may be helpful for your developments:

- IDE:
    - `Qt creator <http://www.qt.io/download-open-source/#section-6>`_
    - `Eclipse CDT <https://eclipse.org/cdt/>`_.

- Versioning tools:
    - `TortoiseHg <http://tortoisehg.bitbucket.org/>`_
    - `SourceTree <http://www.sourcetreeapp.com/>`_


