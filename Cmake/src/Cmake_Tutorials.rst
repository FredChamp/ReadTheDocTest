Tutorials
==========

How can I add a new dependency
------------------------------

You may want to add a new dependency into fw4spl-deps or you may want to add your own folder of dependencies.

.. tip::
    You need to know that the main CMakeLists.txt is in fw4spl-deps, and you can add as many additional folders as you want.
    Use the *ADDITONNAL_DEPS* option in cmake to set the path of your custom deps.


Add a new deps in fw4spl-deps
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adding a new deps is quite easy, the only things to do is to add a new folder *myNewDeps* and put a CMakeLists.txt file into it.
The CMakeLists.txt should contain at least:

- cmake_minimum_required()
- project()
- include(ExternalProject)
- ExternalProject_Add(...)

For example:

.. code:: cmake

    cmake_minimum_required(VERSION 2.8)

    project(myDepsBuilder)

    include(ExternalProject)

    getCachedUrl(http://myDeps.com/myDeps.zip CACHED_URL)

    ExternalProject_Add(
        myDeps
        URL ${CACHED_URL}
        DOWNLOAD_DIR Path/To/Your/Download/dir
        PATCH_COMMAND your_patch_command (optional)
        CONFIGURE_COMMAND your_configure_command (optional)
        BUILD_COMMAND  your_build_command (optional)
        INSTALL_COMMAND your_install_command (optional)
        INSTALL_DIR your_install_dir
        CMAKE_ARGS cmake_arguments
    )
 

Add a custom deps repository
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may want to add your own folder of dependencies (as fw4spl-ext-deps or fw4spl-ar-deps).
In this case your main need to create a CMakeLists.txt in the root of your folder (myDepsFolder/CMakeLists.txt) in order to list the subdirectories of your deps.

.. code:: cmake

    cmake_minimum_required(VERSION 2.8)

    project(CustomDeps)

    list(APPEND SUBDIRECTORIES myDeps1)
    list(APPEND SUBDIRECTORIES myDeps2)
    ...

Then when you do a *ccmake* or *cmake-gui* in the build of your deps, you need to add the path to your custom repository in the *ADDITONNAL_DEPS* option.
Then cmake will automaticaly parsed your folder.


How can I add a custom bundle in fw4spl
----------------------------------------

You may want to add a new bundle/lib/app in an existing repository or you may want to add your custom repository to fw4spl.

.. tip::
    You need to know that the main CMakeLists.txt is in fw4spl repository, and you can add as many additional repository as you want.
    Use the *ADDITIONAL_PROJECTS* option in cmake to add path of your custom folders.

Add a new bundle/lib/app in fw4spl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The only thing to do is to write a CMakeLists.txt and a Properties.cmake (see section Cmake for Fw4spl for more informations).

Add a custom repository to fw4spl
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As the main CMakeLists.txt is in fw4spl repository,you need to add the path of your folder in *ADDITIONAL_PROJECTS* option when you launch *ccmake* of *cmake-gui* on the build folder of fw4spl.
Then your folder will automaticaly be parsed by cmake.

.. note::
    All your bundle/lib/application need to respect the fw4spl-cmake conventions and  have a CMakeLists.txt and a Properties.cmake.

