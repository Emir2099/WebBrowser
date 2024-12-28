import re
from lxml import html

class Node:
    def __init__(self, tag, text=None, attributes=None):
        self.tag = tag
        self.text = text.strip() if text else None
        self.attributes = attributes or {}
        self.styles = self.extract_inline_styles()
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def extract_inline_styles(self):
        """Extract inline styles from the attributes."""
        style_string = self.attributes.get('style', '')
        styles = {}
        if style_string:
            for style in style_string.split(';'):
                if ':' in style:
                    key, value = style.split(':', 1)
                    styles[key.strip()] = value.strip()
        return styles

    def __repr__(self):
        return f"Node(tag={self.tag}, text={self.text}, attributes={self.attributes}, styles={self.styles}, children={len(self.children)})"

class HTMLParser:
    def __init__(self, html_content):
        self.html_content = html_content

    def parse(self):
       
    # Remove comments and scripts
        html_content = self.remove_comments(self.html_content)
        html_content = self.remove_script_tags(html_content)

    # Wrap the content in a root node if needed
        root = html.fromstring(html_content)
        return self.build_tree(root)


    def remove_comments(self, html_content):
        """Remove HTML comments."""
        return re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)

    def remove_script_tags(self, html_content):
        """Remove content within <script> tags."""
        return re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL)

    def build_tree(self, element):
        """Recursively build the DOM tree."""
        if element.tag in ['head', 'style', 'script']:
            return None

        node = Node(element.tag, element.text, element.attrib)
        for child in element:
            child_node = self.build_tree(child)
            if child_node:
                node.add_child(child_node)
        return node