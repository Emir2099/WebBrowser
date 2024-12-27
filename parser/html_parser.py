import re
from lxml import html

class Node:
    def __init__(self, tag, text=None, attributes=None):
        self.tag = tag
        self.text = text.strip() if text else None
        self.attributes = attributes or {}
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"Node(tag={self.tag}, text={self.text}, attributes={self.attributes}, children={len(self.children)})"

class HTMLParser:
    def __init__(self, html_content):
        self.html_content = html_content

    def parse(self):
        # Step 1: Remove comments
        html_content = self.remove_comments(self.html_content)
        
        # Step 2: Remove script tags
        html_content = self.remove_script_tags(html_content)

        # Step 3: Parse the HTML content into DOM-like structure
        self.tree = html.fromstring(html_content)
        return self.build_tree(self.tree)

    def remove_comments(self, html_content):
        """Remove HTML comments."""
        return re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)

    def remove_script_tags(self, html_content):
        """Remove content within <script> tags."""
        return re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL)

    def build_tree(self, element):
        """Recursively build the DOM tree."""
        node = Node(element.tag, element.text, element.attrib)
        for child in element:
            node.add_child(self.build_tree(child))
        return node