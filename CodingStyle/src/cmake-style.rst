CMakeLists coding
=================

.. rule :: Function name

    Standard CMake functions and macros should be written in lower case. Each word is generally separated by an underscore (this is a rule of CMake anyway).

    .. code-block :: cmake

        add_subdirectory("library/")
        include_directories(SYSTEM "/usr/local")

.. rule :: Macro name

    Custom macros should be written in camel case.

    .. code-block :: cmake

        fwLoadProperties()
        fwLink("boost")

.. rule :: Variable name

    Variables should be written in upper case letters separated if needed by underscores.

    .. code-block :: cmake

        set(VARIABLE_NAME "")

.. recommendation :: Expression in block ending

    In the past, CMake enforced to specify the label or expression in block ending, for instance :

    .. code-block :: cmake

        function(name arg1 arg2)
            ...
            if(expr1)
                ...
            else(expr1)
                ...
            endif(expr1)
            ...
        endfunction(name)

    This is no longer needed in latest CMake versions, and we recommend to use this possibility for the sake of simplicity.

    .. code-block :: cmake

        function(name arg1 arg2)
            ...
            if(expr1)
                ...
            else()
                ...
            endif()
            ...
        endfunction()

