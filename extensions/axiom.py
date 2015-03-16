# ###### BEGIN LICENSE BLOCK ######
# FW4SPL - Copyright (C) IRCAD, 2009-2015.
# Distributed under the terms of the GNU Lesser General Public License (LGPL) as
# published by the Free Software Foundation.
# ###### END LICENSE BLOCK ######
#
#documentation extract from http://sphinx-doc.org/extdev/tutorial.html#the-setup-function

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives


#A directive class is a class deriving usually from docutils.parsers.rst.Directive. The directive interface is also covered in detail in the docutils documentation; the important thing is that the class has attributes that configure the allowed markup and a method run that returns a list of nodes.

#Flavien's directive:
class AxiomDirective(Directive):
        has_content = True
        tag_name = ""

        def run(self):

            if self.content:
                text = '\n'.join(self.content)
                definition = nodes.definition(text)

                self.state.nested_parse(self.content, self.content_offset, definition)

                def_list = nodes.definition_list()
                def_item = nodes.definition_list_item()

                term = nodes.term()
                def_text = nodes.Text( self.tag_name + str(" %d") % self.__class__.count)
                self.__class__.count = self.__class__.count + 1
                term.append(def_text)

                iFirst = definition.first_child_matching_class(nodes.paragraph)

                iText = definition[iFirst].first_child_matching_class(nodes.Text)
                text_child=definition[iFirst].children[iText]

                definition.remove(definition[iFirst])

                classifier = nodes.classifier()
                classifier.append(text_child)
            
                def_item.append(term)
                def_item.append(classifier)
                def_item.append(definition)
                def_list.append(def_item)

                return [def_list]
            else:
                return []

class Rule(AxiomDirective):

    tag_name = "Rule"
    count = 1

class Recommendation(AxiomDirective):

    tag_name = "Recommendation"
    count = 1
    
    
def  register_directive(app, docname, source):
    directives.register_directive("rule", Rule)
    directives.register_directive("recommendation", Recommendation)

def setup(app):
    
    # lets Sphinx know that it should recognize the new config value axiom_include_axioms, whose default value should be False (this also tells Sphinx that it is a boolean value).
    # If the third argument was True, all documents would be re-read if the config value changed its value. This is needed for config values that influence reading (build phase 1).
    app.add_config_value('axiom_include', False, False)

    # adds a new directive, given by name and class.
    app.add_directive('axiom', AxiomDirective)
    
    # adds an event handler to the event whose name is given by the first       argument. 
    # The event handler function is called with several arguments which are     documented with the event.
    app.connect('source-read', register_directive)

    return {'version': '0.1'}   # identifies the version of our extension