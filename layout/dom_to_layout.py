from layout.layout_box import LayoutBox
import re

class DOMToLayout:
    def __init__(self, dom_tree, styles, media_queries, viewport_width, event_handlers):
        self.dom_tree = dom_tree
        self.styles = styles
        self.media_queries = media_queries
        self.viewport_width = viewport_width
        self.event_handlers = event_handlers

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
        """Get styles for a node considering specificity (tag, class, id) and media queries."""
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

        # Apply media queries
        for media_query, media_styles in self.media_queries.items():
            if self.evaluate_media_query(media_query):
                print(f"Applying media query: {media_query}")
                for selector, properties in media_styles.items():
                    if selector == tag or selector in classes or selector == f"#{node_id}":
                        styles.update(properties)

        return styles

    def evaluate_media_query(self, media_query):
        """Evaluate if a media query applies based on the viewport width."""
        match = re.search(r"min-width:\s*(\d+)px", media_query)
        if match:
            min_width = int(match.group(1))
            return self.viewport_width >= min_width
        return False

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
            layout_box = LayoutBox(node, node.styles, self.event_handlers)
            
            # Recursively process child nodes (if any)
            for child in node.children:
                layout_box.add_child(process_node(child, node.styles))

            return layout_box

        # Build the root layout box from the root of the DOM tree
        return process_node(self.dom_tree)