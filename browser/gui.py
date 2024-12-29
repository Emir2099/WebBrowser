from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt
import sys
import requests
from parser.html_parser import HTMLParser
from parser.css_parser import CSSParser
from layout.dom_to_layout import DOMToLayout
from renderer.renderer import Renderer

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Web Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.url_bar = QLineEdit(self)
        self.url_bar.setPlaceholderText("Enter URL")
        self.url_bar.returnPressed.connect(self.load_url)

        self.load_button = QPushButton("Load", self)
        self.load_button.clicked.connect(self.load_url)

        self.content_area = QTextEdit(self)
        self.content_area.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.url_bar)
        layout.addWidget(self.load_button)
        layout.addWidget(self.content_area)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_url(self):
        url = self.url_bar.text()
        html_content = self.fetch_content(url)
        self.render_content(html_content)

    def fetch_content(self, url):
        response = requests.get(url)
        return response.text

    def render_content(self, html_content):
        # Use your custom HTML and CSS parsers here
        html_parser = HTMLParser(html_content)
        dom_tree = html_parser.parse()
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
        layout_tree = DOMToLayout(dom_tree, styles, media_queries, viewport_width, {}).build_layout_tree()
        layout_tree.calculate_layout()

        # Render the layout
        renderer = Renderer(layout_tree)
        rendered_content = renderer.render()
        self.content_area.setHtml(rendered_content)

class Renderer:
    def __init__(self, layout_tree):
        self.layout_tree = layout_tree

    def render(self):
        rendered_content = ""
        for box in self.layout_tree.children:
            rendered_content += self.render_box(box)
        return rendered_content

    def render_box(self, box):
        content = f"<div style='position:absolute; left:{box.left}px; top:{box.top}px; width:{box.width}px; height:{box.height}px; background-color:{box.background_color};'>{box.text}</div>"
        for child in box.children:
            content += self.render_box(child)
        return content

def main():
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()