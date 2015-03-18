Activities
==========
An activity represents a set of services. This set can be used as a sub part of an application or as an application.

The SActivityLauncher service allows to launch an activity. Its role is to create the specific Activity associated with 
the selected data.

.. figure:: ../media/activity.svg

* *::activities::action::SActivityLauncher* uses the selected data to generate the activity.
* *::guiQt::editor::DynamicView*  displays the activity in the application.
* *Vector* contains the set of selected data .