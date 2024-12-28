from parser.html_parser import HTMLParser
from parser.css_parser import CSSParser
from layout.dom_to_layout import DOMToLayout
from renderer.renderer import Renderer
from utils.networking import fetch_content
import os

def main():
    # Fetch HTML content
    url = "http://127.0.0.1:5500/resources/example.html"  # Replace with any URL or file pathu
    html_content = fetch_content(url)

    # Parse HTML and CSS
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

    # Convert DOM to layout
    viewport_width = 800  # Example viewport width
    layout_tree = DOMToLayout(dom_tree, styles, media_queries, viewport_width).build_layout_tree()
    layout_tree.calculate_layout()

    # Render the layout
    renderer = Renderer(layout_tree)
    renderer.render()  # Render in the terminal

if __name__ == "__main__":
    main()
   
    #    url = "http://127.0.0.1:5500/resources/example.html"  # Replace with any URL or file path