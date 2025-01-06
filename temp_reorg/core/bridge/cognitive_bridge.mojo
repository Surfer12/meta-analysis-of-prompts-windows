# Cognitive bridge implementation
from python import Python
from ..base.tag_element import TagElement  # Updated import path
from ..base.visitor import Visitor, ProcessingContext  # Updated import path


struct CognitiveBridge:
    """Main bridge implementation for cognitive processing."""

    var context: ProcessingContext
    var visitors: PythonObject  # Python list for visitors

    fn __init__(inout self):
        """Initialize the cognitive bridge."""
        self.context = ProcessingContext()
        self.visitors = Python.list()

    fn add_visitor(inout self, visitor: Visitor):
        """Add a visitor to the processing pipeline."""
        self.visitors.append(visitor)

    fn process_input(inout self, input: String) raises:
        """Process user input through the visitor pipeline."""
        var element = TagElement("user_input", input)

        # Process through all visitors
        try:
            for visitor in self.visitors:
                visitor.visit(element)
        except:
            self.context.add_error("Error processing input: " + input)

    fn get_feedback(self) -> String:
        """Get accumulated feedback."""
        if len(self.context.get_errors()) > 0:
            return "Errors:\n" + self.context.get_errors()
        return "Feedback:\n" + self.context.feedback

    fn cleanup(inout self):
        """Cleanup resources."""
        self.visitors.clear()
