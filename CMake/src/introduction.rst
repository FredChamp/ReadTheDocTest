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

The CMakeLists.txt file
^^^^^^^^^^^^^^^^^^^^^^^

The CMakeLists.txt should contain at least the function *fwLoadProperties()* to load the Properties.cmake.
But it can also contain others functions usefull to link with external libraries.

Here is an example of CMakeLists.txt from guiQt Bundle :

.. code:: cmake

    fwLoadProperties()
    fwUseForwardInclude(
        fwActivities
        fwGuiQt
        fwRuntime
        fwServices
        fwTools

        gui
    )

    find_package(Qt5 COMPONENTS Core Gui Widgets REQUIRED)


    fwForwardInclude(
        ${Qt5Core_INCLUDE_DIRS}
        ${Qt5Gui_INCLUDE_DIRS}
        ${Qt5Widgets_INCLUDE_DIRS}
    )

    fwLink(
           ${Qt5Core_LIBRARIES}
           ${Qt5Gui_LIBRARIES}
           ${Qt5Widgets_LIBRARIES}
    )

    set_target_properties(${FWPROJECT_NAME} PROPERTIES AUTOMOC TRUE)

The first line *fwLoadProperties()* will load the properties.cmake (see explanation in the next section).
The *fwUseForwardInclude(...)* function will add the include directories of each argument to the target.

The next lines are for the link with an external libraries (fw4spl-deps), in this example it is Qt.

The first thing to do is to call *find_package(The_lib COMPONENTS The_component)*.

The use *fwForwardInclude* to add includes directories to the target,
and *fwLink* to link the libraries with your target.

You can also add custom properties to your target with *set_target_properties*.


The Properties.cmake file
^^^^^^^^^^^^^^^^^^^^^^^^^
 
Properties.cmake should contain informations like name, version, dependencies and requirements of the current target.

Here is an example of Properties.cmake from fwData library:

.. code:: cmake

 set( NAME fwData )
 set( VERSION 0.1 )
 set( TYPE LIBRARY )
 set( DEPENDENCIES fwCamp fwCom fwCore fwMath fwMemory fwTools )
 set( REQUIREMENTS  )

- NAME: Name of the target
- VERSION: Version of the target
- TYPE: Type of the target (can be library, bundle or executable)
- DEPENDENCIES: Link the target with the given libraries (see `target_link_libraries <http://www.cmake.org/cmake/help/v3.0/command/target_link_libraries.html?highlight=target_link_libraries>`_ )
- REQUIREMENTS: Ensure that the depends are build before target (see `add_dependencies <http://www.cmake.org/cmake/help/v3.0/command/add_dependencies.html?highlight=add_dependencies>`_ )
