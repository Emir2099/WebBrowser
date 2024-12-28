import os
from utils.networking import fetch_content
from parser.html_parser import HTMLParser
from parser.css_parser import CSSParser
from layout.dom_to_layout import DOMToLayout

class Renderer:
    def __init__(self, layout_tree, base_url):
        self.layout_tree = layout_tree
        self.base_url = base_url
        self.form_data = {}

    def draw_element(self, box, depth=0):
        """
        Draw a single element as an ASCII representation.
        Print styles like color and font-size (simulated in the terminal).
        """
        content = box.node.text if box.node.text else "Box"
        indent = "  " * depth

        # Get applied styles
        styles = box.node.styles
        color = styles.get("color", "black")
        font_size = styles.get("font-size", "14px")
        background_color = styles.get("background-color", "transparent")
        text_decoration = styles.get("text-decoration", "none")
        font_weight = styles.get("font-weight", "normal")

        # Simulating rendering in the terminal
        print(f"{indent}{content} (Color: {color}, Font-size: {font_size}, Background-color: {background_color}, Text-decoration: {text_decoration}, Font-weight: {font_weight}, Width: {box.width}px, Height: {box.height}px, Padding: {box.padding}, Border: {box.border}, Margin: {box.margin}, Position: {box.position}, Left: {box.left}px, Top: {box.top}px)")

        if box.node.tag == 'a' and 'href' in box.node.attributes:
            href = box.node.attributes['href']
            print(f"{indent}Link: {href}")

        if box.node.tag == 'form':
            print(f"{indent}Form: {box.node.attributes.get('action', '')}")

        if box.node.tag == 'input':
            input_type = box.node.attributes.get('type', 'text')
            input_name = box.node.attributes.get('name', '')
            input_value = box.node.attributes.get('value', '')
            print(f"{indent}Input: type={input_type}, name={input_name}, value={input_value}")

        for child in box.children:
            self.draw_element(child, depth + 1)

    def render(self):
        print("Rendering Layout Tree:")
        self.draw_element(self.layout_tree)
        print("Rendering Complete.")

    def handle_link(self, href):
        if not href.startswith('http'):
            href = os.path.join(self.base_url, href)
        html_content = fetch_content(href)
        html_parser = HTMLParser(html_content)
        dom_tree = html_parser.parse()

        css_content = """
            body { background: lightblue; width: 1000px; height: 800px; }
            .container { width: 500px; height: 300px; padding: 20px; border: 10px solid black; margin: 30px; position: relative; }
            .absolute-box { width: 200px; height: 100px; background-color: yellow; position: absolute; left: 50px; top: 50px; }
            .relative-box { width: 150px; height: 75px; background-color: green; position: relative; left: 20px; top: 20px; }
            .fixed-box { width: 100px; height: 50px; background-color: pink; position: fixed; left: 10px; top: 10px; }
            .sticky-box { width: 120px; height: 60px; background-color: orange; position: sticky; top: 0; }
            p { color: green; font-size: 14px; }
            .float-left { float: left; width: 100px; height: 50px; background-color: lightgrey; }
            .float-right { float: right; width: 100px; height: 50px; background-color: lightcoral; }
            @media (min-width: 600px) {
                body { background: lightgreen; }
                .container { width: 600px; }
            }
        """  # Temporary inline CSS for testing
        css_parser = CSSParser()
        styles, media_queries = css_parser.parse(css_content)

        viewport_width = 800  # Example viewport width
        layout_tree = DOMToLayout(dom_tree, styles, media_queries, viewport_width).build_layout_tree()
        layout_tree.calculate_layout()

        self.layout_tree = layout_tree
        self.render()

    def handle_form_submission(self, form_data):
        print("Form Submitted with Data:")
        for key, value in form_data.items():
            print(f"{key}: {value}")