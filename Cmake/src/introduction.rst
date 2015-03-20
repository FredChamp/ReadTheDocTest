CMake for fw4spl
================

Introduction
-------------

Fw4spl and it's dependencies are based on `CMake <http://www.cmake.org/>`_ .
Note that the minimal version of cmake to have is 2.8.12.

CMake files for dependencies
-----------------------------
fw4spl dependencies are based on the `ExternalProject <http://www.cmake.org/cmake/help/v3.0/module/ExternalProject.html>`_ concept from lastest versions of cmake.

The concept is to create custom targets to build projects in external trees.
Each project has custom steps for download, update/patch, configure, build and install.

Here is a simple example from camp :

.. code:: cmake

    cmake_minimum_required(VERSION 2.8)

    project(campBuilder)

    include(ExternalProject)

    set(CAMP_CMAKE_ARGS ${COMMON_CMAKE_ARGS}
                        -DBUILD_DOXYGEN:BOOL=OFF
                        -DBOOST_INCLUDEDIR:PATH=${CMAKE_INSTALL_PREFIX}/include/boost-1_57
    )

    getCachedUrl(https://github.com/greenjava/camp/archive/0.7.1.1.tar.gz CACHED_URL)

    ExternalProject_Add(
        camp
        URL ${CACHED_URL}
        DOWNLOAD_DIR ${ARCHIVE_DIR}
        DEPENDS boost
        INSTALL_DIR ${CMAKE_INSTALL_PREFIX}
        CMAKE_ARGS ${CAMP_CMAKE_ARGS}
        STEP_TARGETS CopyConfigFileToInstall
    )

    ExternalProject_Add_Step(camp CopyConfigFileToInstall
        COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_SOURCE_DIR}/cmake/findBinpkgs/FindCAMP.cmake ${CMAKE_INSTALL_PREFIX}/FindCAMP.cmake
        COMMENT "Install configuration file"


The important parts are in the *ExternalProject_Add* fonction:

- URL: is the download link of the sources
- DOWNLOAD_DIR: The folder where the sources will be stored (set globaly for all deps)
- DEPENDS: The dependencies of the current library (will be compiled before)
- INSTALL_DIR: The folder in which the library will be installed (set globaly for all deps)
- CMAKE_ARGS: CMake options for library which have a cmake build system
- STEP_TARGETS: Custom command (in this example it will copy a script in the install folder)

Note that in other script you can have much more options like:

- PATCH_COMMAND
- CONFIGURE_COMMAND
- BUILD_COMMAND
- INSTALL_COMMAND

Refer you to the documentation of `ExternalProject <http://www.cmake.org/cmake/help/v3.0/module/ExternalProject.html>`_ for more informations.



CMake files for fw4spl
-----------------------


Each project (apps, bundles, libs) have two "CMake" files:

- CMakeLists.txt
- Properties.cmake
 


The CMakeLists.txt must contain at least the fonction *fwLoadProperties()*

Properties.cmake should contain informations like name, version, dependencies and requirements.

Here is an example of Properties.cmake from fwData library:

.. code:: cmake

 set( NAME fwData )
 set( VERSION 0.1 )
 set( TYPE LIBRARY )
 set( DEPENDENCIES fwCamp fwCom fwCore fwMath fwMemory fwTools )
 set( REQUIREMENTS  )





