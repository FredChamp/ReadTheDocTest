Documentation
=============

.. rule :: Document the code

    The code must be documented with **Doxygen**, an automated tool to generate documentation.

.. rule :: Location of the documentation

    Every documentation that can be useful to a user must be placed inside the header files. Thus a user of a module can find the declaration of a class and its documentation at the same place. Inside the implementation file, the documentation will give more details about algorithms.
    Moreover, every documentation must be placed next to the entity it is refering to, in order to help searching inside the code.

.. recommendation :: Lightweight documentation

    Inside a documentation block, only use necessary tags. This will avoid to overload the documentation and makes it readable. By the way, empty tags will be presented inside the generated documentation and will be useless.
    Just use an empty line to make a separation inside a documentation block.
    Don't indicate parameter types when using ``@param`` directive. This is useless since it will duplicate information of the function prototype.
    Also, prefer the use of ``///`` whenever possible.

Example 1 : Bad documentation block

    .. code-block :: cpp

        /**
        * @brief        A very short description.
        *
        * A longer description, giving more details about the documented piece
        * of code.
        *********************************************
        * @param
        *********************************************
        * @return
        *********************************************
        * @exception
        *********************************************
        * @todo
        *********************************************

Example 2 : Good documentation block

    .. code-block :: cpp

        /**
        * @brief        A very short description.
        *
        * A longer description, giving more details about the documented piece
        * of code.
        */

Example 3 : Function documentation

    .. code-block :: cpp

        class Sample
        {
        public:
            /**
            * Retrieve the thing.
            *
            * @return       The thing value.
            */
            const std::string& getThing( void ) const;
            /**
            * @brief        Set the thing.
            *
            * @param        thing   :  The new thing.
            */
            void setThing( const std::string& thing );

        private:
            /// stored thing
            std::string     m_thing;
        };

.. recommendation :: Structured documentation

    Doxygen provides a default structure when you generate the documentation. However, when dealing with a big documented entity, it is often recommended to use the group feature (``@name``). With this feature you will build a logical view of the class interfaces.

.. rule :: Document service configuration

    The method ``configuring`` of a service must be properly documented. It should indicate every parameter that can be passed, no matter if it is optional or not. Example :

    .. code-block :: cpp

        /**
         * @verbatim
        <adaptor id="points" class="::namespace::SService">
            <config option1="default" option2="false"/>
        </adaptor>
         @endverbatim
         * - \b option1 : first option.
         * - \b option2(optional) : second option.
        */
        NAMESPACE_API void configuring() throw(fwTools::Failed);
    
