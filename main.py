from parser.html_parser import HTMLParser
from parser.css_parser import CSSParser
from layout.dom_to_layout import DOMToLayout
from renderer.renderer import Renderer
from utils.networking import fetch_content


def main():
    # Fetch HTML content
    url = "http://127.0.0.1:5500/resources/example.html"  # Replace with any URL or file path
    html_content = fetch_content(url)

    # Parse HTML and CSS
    html_parser = HTMLParser(html_content)
    dom_tree = html_parser.parse()

    css_content = """
        body { background: white; }
        p { color: black; font-size: 16px; }
    """  # Temporary inline CSS for testing
    css_parser = CSSParser()
    styles = css_parser.parse(css_content)

    # Convert DOM to layout
    layout_tree = DOMToLayout(dom_tree, styles).build_layout_tree()
    layout_tree.calculate_layout()

    # Render the layout
    renderer = Renderer(layout_tree)
    renderer.render()  # Render in the terminal


if __name__ == "__main__":
    main()
