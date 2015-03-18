C++ coding
============

Source and files
-----------------

.. rule :: Files tree

    Source files must be placed in a folder ``src/``. Public header files must be placed in a folder ``include/``. Private headers may be placed in a different location.

.. rule :: Files hierarchy
    
    The file hierarchy should follow the namespace hierarchy. For instance, the implementation of a class ``::ns1::ns2::SService`` should be put in ``src/ns1/ns2/SService.cpp``.

.. rule :: Files extensions
    
    Header files use the extension ``.hpp``.

    Implementation files use the extension ``.cpp``.

    Files containing implementation of “template” classes use the extension ``.hxx``.

.. recommendation :: Only one class per file

    It is recommended to declare (or to implement) only one class per file. However tiny classes may be declared inside the same file.

.. rule :: Includes
    
    Use the right include directive depending on the context. ``#include "..."`` must be used to import headers from the same module, whereas ``#include <...>`` must be used to import headers from other modules.

.. rule :: Include path

    The include path is not an absolute path depending on a local file system. A correct include path does respect the letter case of the filenames and folders (since some platforms require it) and uses the character '/' as a separator.

.. rule :: Protection against multiple inclusions

    You must protect your files against multiple inclusions. To this end, use the standard directives of the precompiler ``#ifndef`` and ``#define`` (since ``#pragma`` once is only supported by Microsoft compilers).
    
    Use the name of the file and the namespace hierarchy inside the define name in order to prevent any conflict with a file which has the same name but located in a different namespace. Namespaces and file name must be separated by a single underscore ``_``. The define name must be prefixed and suffixed by two underscores ``__``. Last, a comment must be placed after ``#endif`` to quote the define.

    .. code-block :: cpp

        #ifndef __NAMESPACEA_NAMESPACEB_SAMPLE_HPP__ // Preamble protecting against
        #define __NAMESPACEA_NAMESPACEB_SAMPLE_HPP__ // multiple inclusions.

        #endif // __NAMESPACEA_NAMESPACEB_SAMPLE_HPP__

.. recommendation :: Independent headers

    A header should compile alone. All necessary includes should be contained inside the header itself. In the following sample :

    .. code-block :: cpp

        // Header.hpp

        class Foo
        {
        public:    
            std::string m_string;
        }

    you will be forced to include the file in this way to get a successful build :

    .. code-block :: cpp

        // Source.hpp

        #include <string>
        #include "Header.hpp"

    This is a bad practice, the header should rather be written :

    .. code-block :: cpp

        // Header.hpp

        #include <string>

        // Header.hpp
        class Foo
        {
        public:    
            std::string m_string;
        }

    So that people can simply include the header :

    .. code-block :: cpp

        // Source.hpp

        #include "Header.hpp"

.. recommendation :: Minimize inclusions

    Try to minimize as much as possible inclusions inside a header file. `Include only what you use <https://code.google.com/p/include-what-you-use/>`_. Use `forward declarations` when you can (i.e. a type or class structure is not referenced inside the header). This will limit dependency between files and reduce compile time. Hiding the implementation can also help to minimize inclusions (see `Hide implementation`_)

.. rule :: Sort headers inclusions

    You must sort headers in the following order : same module, framework libraries, bundles, external libraries, standard library. This way, this helps to make each header independent. The rule can be broken if a different include order is necessary to get a successful build.

    .. code-block :: cpp

        #include "currentModule.hpp"

        #include <libSampleB/second.hpp>
        #include <libSampleA/first.hpp>
        #include <libSampleB/subModule/first.hpp>

        #include <Qt/QtGui>
        #include <vector>
        #include <map>

.. recommendation :: Sort inclusions alphanumerically

    In addition to the previous sort, you may sort includes in alphanumerical order, according to the whole path. Thus they will be grouped by module. For a better readability, an empty line can be added between each module.

    .. code-block :: cpp

        #include "currentModule.hpp"

        #include <libSampleA/first.hpp>
        #include <libSampleB/second.hpp>

        #include <libSampleB/subModule/first.hpp>
        #include <libSampleB/subModule/second.hpp>

        #include <Qt/QtGui>

        #include <map>
        #include <vector>

Naming conventions
------------------

.. rule :: Class

    Class names must be written in upper camel case. It should not repeat a namespace name. For instance ``::editor::SCustomEditor`` should be rather called ``::editor::SCustom``.

.. rule :: File

    The name of the file should be based on the class name defined in it. It must follow the same letter case.

.. rule :: Namespace

    Namespaces must be written in camel case. A comment quoting the namespace must be placed next to the ending '}'.

    .. code-block :: cpp

        namespace namespaceA
        {
        namespace namespaceB
        {
            class Sample
            {
            ...
            };
        } // namespace namespaceB
        } // namespace namespaceA

    When referring a namespace, you must put ``::`` if this is a root namespace, with an exception for ``std`` namespace. Ex: ``::boost::filesystem``.

.. rule :: Function and method names

    Functions and methods names must be written in camel case. 

.. recommendation :: Correct naming of functions

    Try as much as possible to help the users of your code by using comprehensive names. You may for instance help them to indicate the cost of a function. A function that executes a search to retrieve an object must not be called like a getter. In this case, it is better to call it ``findObjet()`` instead of ``getObject()``.

.. rule :: Variable

    Variable names must be written in camel case. Members of a class are prefixed with a ``m_``.

    .. code-block :: cpp

        class SampleClass
        {
        private:
           int m_identifier;
           float m_value;
        };

    Static variables are prefixed with a ``s_``.

    .. code-block :: cpp

        static int s_staticVar;

.. rule :: Constant
    
    Constant variables must be written in snake_case but in capitals, and follow the previous rule.

    .. code-block :: cpp

        class SampleClass
        {
            static const int s_AAA_BBB_CCC_VALUE = 1;           
        };

        void fooFunction()
        {
            const int AAA_BBB_VAR = 1;
            ...
        }
        
.. rule :: Type

    Type names, like classes, must be written in upper camel case.

    .. code-block :: cpp

        typedef int CustomType;
        typedef vector<int> CustomContainer;

.. rule :: Template parameter

    Template parameters must be written in capitals. In addition, they must be short and explicit.

    .. code-block :: cpp

        template< class KEY, class VALUE > class SampleClass
        {
            ...
        };

.. rule :: Macro
    
    Macros without parameters must be written in capitals. On the contrary, there is no specific rule on macros with parameters.

    .. code-block :: cpp

        #define CUSTOM_FLAG_A 1
        #define CUSTOM_FLAG_B 1

        #define CUSTOM_MACRO_A( x ) x
        #define Custom_Macro_B( x ) x
        #define custom_Macro_C( x ) x
        #define custom_macro_d( x ) x

.. rule :: Enumerated type

    An enumerated type name must be written in upper camel case. Labels must be written in capitals. If a ``typedef`` is defined, it follows the upper camel case standard.

    .. code-block :: cpp

        typedef enum SampleEnum
        {
            LABEL_1,
            LABEL_2
            ...
        } SampleEnumType;

.. rule :: Service

    A service implementation is identified by a ``S`` at the beginning of the class name. Example : ``SCustomEditor``. A service interface is identified by a ``I`` at the beginning of the class name. Example : ``IEditor``.

.. rule :: Signal

    A signal name must be prefixed with ``sig``. It should be suffixed by a past action (ex: Updated, Triggered, Cancelled, CakeCookedAndBaked). It follows other common variable naming rules (member of a class, etc...).

    .. code-block :: cpp

        class Sample
        {
            SigType::sptr m_sigImageDisplayed;
        };

.. rule :: Slot

    A slot name must be prefixed with ``slot``. It should be suffixed by an imperative order (Ex: Update, Run, Detach, Deliver, OpenWebBrowser, GoToFail). It follows other common variable naming rules (member of a class, etc...).

    .. code-block :: cpp

        class Sample
        {
            SlotType::sptr m_slotDisplayImage;
        }

Coding rules
-----------------

Blocks
~~~~~~~~~~~~~~~~~~~~~~~~~

.. rule :: Indentation

    Code block indentation and bracket positioning follow the `Allman <http://en.wikipedia.org/wiki/Indent_style#Allman_style>`_ style.

    .. code-block :: cpp

        void function(void)
        {
            if(x == y)
            {
                something1();
                something2();
            }
            else
            {
                somethingElse1();
                somethingElse2();
            }
            finalThing();
        }

.. rule :: Indentation of namespaces

    Namespaces are an exception of the previous rule. They should not be indented.

    .. code-block :: cpp

        namespace namespaceA
        {
        namespace namespaceB
        {
            ...
        } // namespace namespaceB
        } // namespace namespaceA

.. rule :: Blocks are mandatory

    After a control statement (if, else, for, while/do...while, try/catch, switch, foreach, etc...), it is mandatory to open a block, whatever is the number of instructions inside the block.

.. rule :: Scope

    The keywords ``public``, ``protected`` and ``private`` are not indented, they should be aligned with the keyword ``class``.

    .. code-block :: cpp
        
        class Sample
        {
        public:
            ...
        private:
            ...
        };

Class declaration
~~~~~~~~~~~~~~~~~~~~~~~~~

.. recommendation :: Only three scope sections

    When possible, use only one section of each scope type ``public``, ``protected`` and ``private``. They must be declared in this order.

.. recommendation :: Group class members by type

    You may group class members in each scope according to their type: type definitions, constructors, destructor, operators, variables, functions.

.. _`Hide implementation`:
.. rule :: Hide implementation

    Avoid non-const public member variables except in very small classes (i.e. a 3D point). The `Pimpl idiom <http://c2.com/cgi/wiki?PimplIdiom>`_ may also be helpful to separate the implementation from the declaration.

.. recommendation :: Hide implementation

    Try to put variables as much as possible in the ``private`` section.

.. rule :: Accessors

    Since you protect your member variables from the outside, you will have to write accessors, named ``getXXX()`` and ``setXXX()``. Getters are always ``const``.

.. rule :: Template class function definition

    The function definition of a template class must be defined after the declaration of the class.

    .. code-block :: cpp

        template < typename TYPE >
        class Sample
        {
        public:
            void function(int i);
        };

        template < typename TYPE >
        inline Sample<TYPE>::function(int i)
        {
            ...
        }
        
.. recommendation :: Separate template class function definition

    In addition of the previous rule, you may put the definition of the function in a ``.hxx`` file. This file will be included in the implementation file right after the header file (the compile time will be reduced comparing with an inclusion of the ``.hxx`` in the header file itself).

    .. code-block :: cpp

        #include <namespaceA/file.hpp>
        #include <namespaceA/file.hxx>

Initializer list
~~~~~~~~~~~~~~~~~~~~~~~~~

.. rule :: One initializer per line

    In a class constructor, use the initialization list as much as possible. Place one initializer per line. Constructors of base classes should be placed first, followed by member variables. Do not specify an initializer if it is the default one (empty std::string for instance).

    .. code-block :: cpp

        SampleClass::SampleClass( const std::string& name, const int value ) :
            BaseClassOne( name ),
            BaseClassTwo( name ),
            m_value( value ),
            m_misc( 10 )
        {}

.. recommendation :: Align everything that improves readability

    To improve readability, you may align members on one hand and argument lists on the other hand.

    .. code-block :: cpp

        SampleClass::SampleClass( const std::string& name, const int value ) :
            BaseClassOne  ( name ),
            BaseClassTwo  ( name ),
            m_value       ( value ),
            m_misc        ( 10 )
        {}

Functions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. rule :: Constant reference

    Whenever possible, use constant references to pass arguments of non-primitive types. This avoids useless and expensive copies.

    .. code-block :: cpp
        
        void badFunction( std::vector<int> array )
        {
            ...
        }

        void goodFunction( const std::vector<int>& array )
        {
            ...
        }

.. recommendation :: Constant reference for shared pointers

    For performance sake, it is preferable to use ``const&`` to pass arguments of type ``::boost::shared_ptr``. It is only useful to pass the pointer by copy if the pointer can be invalidated by an another thread during the function call. If you have any doubt, it is safer to pass the argument by copy.        

.. rule :: Constant functions

    Whenever a member function should not modify an attribute of a class, it must be declared as ``const``.

    .. code-block :: cpp

        void readOnlyFunction( const std::vector<int>& array ) const
        {
            ...
        }

.. recommendation :: Limit use of expression in arguments

    When passing arguments, try to limit the use of expressions to the minimum.

    .. code-block :: cpp

        // This is bad
        function( fn1(val1 + val2 / 4 ), fn2( fn3( val3 ), val4) );
    
        // This is better
        const float res0 = val1 + val2 / 4;

        const float res1 = fn1(res0);
        const float res3 = fn3(val3);
        const float res2 = fn2(res3, val4);

        function( res1 , res2 );

Miscellaneous
~~~~~~~~~~~~~~~~~~~~~~~~~

.. rule :: Enumerator labels

    Each label must be placed on a single line, followed by a comma. If you assign values to labels, align values on the same column.

    .. code-block :: cpp

        enum OpenFlag
        {
            OPEN_SHARE_READ      = 1,
            OPEN_SHARE_WRITE     = 2,
            OPEN_EXISTING        = 4,
        };

.. rule :: Use of namespaces

    You have to organize your code inside namespaces. By default, you will have at least one namespace for your module (application or bundle). Inside this namespace, it is recommended to split your code into sub-namespaces. This helps notably to prevent naming conflicts.

    It is forbidden to use the expression``using namespace`` in header files but it is allowed in implementation files. It is however recommended to use aliases in this latter case.

    .. code-block :: cpp

        namespace bf = ::boost::filesystem;
        

.. rule :: Keyword const

    Use this keyword as much as possible for variables, parameters and functions.

.. recommendation :: Keyword auto

    Use this keyword as much as possible to improve maintainability and robustness of the code.

.. rule :: Prefer constants instead of #define

    Use a static constant object or an enumeration instead of a ``#define``. This will help the compiler to make type checking. You will also be able to check the content of the constants while debugging. You can also define a scope for them, inside the namespace, inside a class, private to a class, etc...

.. rule :: Prefer references over pointers

    When possible, use references instead of pointers, especially for function parameters. Pointer as parameter should only be used if it is considered to have a NULL pointer or when passing a C-like array. If you use a pointer, always check it if is null in the current scope before dereferencing it.

.. rule :: Type conversion

    For type conversion, use the C++ operators which are ``static_cast``, ``dynamic_cast``,  ``const_cast`` and ``reinterpret_cast``. Use them wisely in the appropriate case. You may read `this documentation <http://www.cplusplus.com/doc/tutorial/typecasting/>`_.

.. recommendation :: Strings to numbers/numbers to string conversion

    When converting strings to numbers or numbers to string, prefer the use of `boost::lexical_cast <http://www.boost.org/doc/libs/1_55_0/doc/html/boost_lexical_cast/examples.html#boost_lexical_cast.examples.strings_to_numbers_conversion>`_.

.. recommendation :: Exceptions

    Exceptions are the preferred mechanism to handle error notifications.

.. rule :: Explicit integer types

    When you do need a specific integer size, use type definitions declared in `<cstdint> <http://www.cplusplus.com/reference/cstdint/>`_, for example :
    
    ======  =========  ==========
     Bits    Signed     Unsigned
    ======  =========  ==========
     8       int8_t     uint8_t
     16      int16_t    uint16_t
     32      int32_t    uint32_t
     64      int64_t    uint64_t
    ======  =========  ==========