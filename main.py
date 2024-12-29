from parser.html_parser import HTMLParser
from parser.css_parser import CSSParser
from layout.dom_to_layout import DOMToLayout
from renderer.renderer import Renderer
from utils.networking import fetch_content
from python_scripting import PythonScripting
import os

event_handlers = {}

def handle_navigation(url):
    html_content = fetch_content(url)
    return html_content

def handle_form_submission(form_data):
    # Mock form submission
    print("Form submitted with data:", form_data)

def handle_button_click(event_id):
    if event_id in event_handlers:
        event_handlers[event_id]()

def main():
    # Fetch HTML content
    url = "http://127.0.0.1:5500/resources/example.html"  # Replace with any URL or file path
    html_content = fetch_content(url)

    # Parse HTML and CSS
    html_parser = HTMLParser(html_content)
    dom_tree = html_parser.parse()
    python_scripts = html_parser.extract_python_scripts()
    css_content = """
        body { background: lightblue; width: 1000px; height: 800px; }
        .animated-box { width: 100px; height: 100px; background-color: red; position: absolute; animation: move-right 2s; }
        @keyframes move-right {
            from { left: 0px; }
            to { left: 100px; }
        }
    """  # Temporary inline CSS for testing
    css_parser = CSSParser()
    styles, media_queries = css_parser.parse(css_content)

    # Convert DOM to layout
    viewport_width = 800  # Example viewport width
    layout_tree = DOMToLayout(dom_tree, styles, media_queries, viewport_width, event_handlers).build_layout_tree()
    layout_tree.calculate_layout()

    # Render the layout
    renderer = Renderer(layout_tree)
    renderer.render()  # Render in the terminal

    # Create Python scripting environment and execute scripts
    python_scripting = PythonScripting(dom_tree)
    for script in python_scripts:
        exec(script, {"python_scripting": python_scripting})

    # Simulate animation
    for child in layout_tree.children:
        child.simulate_animation()

    # Handle navigation and form submission
    while True:
        user_input = input("Enter 'link <url>' to navigate, 'submit <form_data>' to submit a form, or 'click <event_id>' to simulate a button click: ")
        if user_input.startswith("link "):
            url = user_input.split(" ", 1)[1]
            html_content = handle_navigation(url)
            html_parser = HTMLParser(html_content)
            dom_tree = html_parser.parse()
            python_scripts = html_parser.extract_python_scripts()
            layout_tree = DOMToLayout(dom_tree, styles, media_queries, viewport_width, event_handlers).build_layout_tree()
            layout_tree.calculate_layout()
            renderer = Renderer(layout_tree)
            renderer.render()
            python_scripting = PythonScripting(dom_tree)
            for script in python_scripts:
                exec(script, {"python_scripting": python_scripting})
        elif user_input.startswith("submit "):
            form_data = user_input.split(" ", 1)[1]
            handle_form_submission(form_data)
        elif user_input.startswith("click "):
            event_id = user_input.split(" ", 1)[1]
            handle_button_click(event_id)
        # Process event queue
        python_scripting.run_event_loop()

if __name__ == "__main__":
    main()
     # Fetch HTML content
    # url = "http://127.0.0.1:5500/resources/example.html"  # Replace with any URL or file path
    # html_content = fetch_content(url)