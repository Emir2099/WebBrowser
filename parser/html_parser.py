from lxml import html

class Node:
    def __init__(self, tag, text=None, attributes=None):
        self.tag = tag
        self.text = text.strip() if text else None
        self.attributes = attributes or {}
        self.children = []

    def add_child(self, child):
        self.children.append(child)

class HTMLParser:
    def __init__(self, html_content):
        self.tree = html.fromstring(html_content)

    def parse(self):
        def build_tree(element):
            node = Node(element.tag, element.text, element.attrib)
            for child in element:
                node.add_child(build_tree(child))
            return node

        return build_tree(self.tree)
