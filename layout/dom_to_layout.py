from layout.layout_box import LayoutBox

class DOMToLayout:
    def __init__(self, dom_tree, styles):
        self.dom_tree = dom_tree
        self.styles = styles

    def apply_styles(self, node):
        """
        Apply styles to a DOM node from the CSS styles.
        """
        tag = node.tag
        if tag in self.styles:
            node.styles = self.styles[tag]
        else:
            node.styles = {}

    def build_layout_tree(self):
        """
        Recursively builds the layout tree from the DOM.
        """
        def process_node(node):
            # Apply styles to each node in the DOM
            self.apply_styles(node)
            layout_box = LayoutBox(node, node.styles)
            
            # Recursively process child nodes (if any)
            for child in node.children:
                layout_box.add_child(process_node(child))

            return layout_box

        # Build the root layout box from the root of the DOM tree
        return process_node(self.dom_tree)