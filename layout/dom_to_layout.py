from layout.layout_box import LayoutBox

class DOMToLayout:
    def __init__(self, dom_tree, styles):
        self.dom_tree = dom_tree
        self.styles = styles

    def apply_styles(self, node, parent_styles=None):
        """
        Apply styles to a DOM node from the CSS styles and inline styles.
        """
        node.styles = self.get_styles_for_node(node)  # Get CSS styles for the node

        # Inherit styles from parent
        if parent_styles:
            inherited_styles = parent_styles.copy()
            inherited_styles.update(node.styles)
            node.styles = inherited_styles

        # Parse inline styles and merge with CSS styles
        inline_styles = self.parse_inline_styles(node.attributes.get('style', ''))
        node.styles.update(inline_styles)

    def get_styles_for_node(self, node):
        """Get styles for a node considering specificity (tag, class, id)."""
        styles = {}
        tag = node.tag
        classes = node.attributes.get("class", "").split()
        node_id = node.attributes.get("id", "")

        for selector, properties in self.styles.items():
            # Match based on tag
            if selector == tag:
                styles.update(properties)
            # Match based on classes
            for cls in classes:
                if selector == f".{cls}":
                    styles.update(properties)
            # Match based on ID
            if selector == f"#{node_id}":
                styles.update(properties)

        return styles

    def parse_inline_styles(self, style_string):
        """Parse inline styles from a string into a dictionary."""
        styles = {}
        if style_string:
            for style in style_string.split(';'):
                if ':' in style:
                    key, value = style.split(':', 1)
                    styles[key.strip()] = value.strip()
        return styles

    def build_layout_tree(self):
        """
        Recursively builds the layout tree from the DOM.
        """
        def process_node(node, parent_styles=None):
            # Apply styles to each node in the DOM
            self.apply_styles(node, parent_styles)
            layout_box = LayoutBox(node, node.styles)
            
            # Recursively process child nodes (if any)
            for child in node.children:
                layout_box.add_child(process_node(child, node.styles))

            return layout_box

        # Build the root layout box from the root of the DOM tree
        return process_node(self.dom_tree)