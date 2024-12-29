from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import requests
from parser.html_parser import HTMLParser
from parser.css_parser import CSSParser
from layout.dom_to_layout import DOMToLayout
from renderer.renderer import Renderer
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

class BrowserTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Navigation bar
        nav_bar = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.back_button = Button(text="<", size_hint_x=None, width=40, background_color=(0.1, 0.5, 0.8, 1), color=(1, 1, 1, 1))
        self.back_button.bind(on_press=self.go_back)
        self.forward_button = Button(text=">", size_hint_x=None, width=40, background_color=(0.1, 0.5, 0.8, 1), color=(1, 1, 1, 1))
        self.forward_button.bind(on_press=self.go_forward)
        self.refresh_button = Button(text="⟳", size_hint_x=None, width=40, background_color=(0.1, 0.5, 0.8, 1), color=(1, 1, 1, 1))
        self.refresh_button.bind(on_press=self.refresh_page)
        self.url_bar = TextInput(size_hint_y=None, height=40, hint_text="Enter URL", background_color=(0.2, 0.2, 0.2, 1), foreground_color=(1, 1, 1, 1))
        self.url_bar.bind(on_text_validate=self.navigate_to_url)
        self.load_button = Button(text="Load", size_hint_x=None, width=60, background_color=(0.1, 0.5, 0.8, 1), color=(1, 1, 1, 1))
        self.load_button.bind(on_press=self.navigate_to_url)

        nav_bar.add_widget(self.back_button)
        nav_bar.add_widget(self.forward_button)
        nav_bar.add_widget(self.refresh_button)
        nav_bar.add_widget(self.url_bar)
        nav_bar.add_widget(self.load_button)

        # Content area
        self.content_area = ScrollView()
        self.content_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.content_container.bind(minimum_height=self.content_container.setter('height'))
        self.content_area.add_widget(self.content_container)

        # Status bar
        self.status_bar = Label(size_hint_y=None, height=30, text="Ready", color=(1, 1, 1, 1))
        with self.status_bar.canvas.before:
            Color(0.1, 0.1, 0.1, 1)  # Background color
            self.status_bar.rect = Rectangle(size=self.status_bar.size, pos=self.status_bar.pos)
            self.status_bar.bind(size=self._update_rect, pos=self._update_rect)

        self.add_widget(nav_bar)
        self.add_widget(self.content_area)
        self.add_widget(self.status_bar)

        # History for back and forward navigation
        self.history = []
        self.history_index = -1

    def _update_rect(self, instance, value):
        self.status_bar.rect.pos = instance.pos
        self.status_bar.rect.size = instance.size

    def navigate_to_url(self, instance):
        url = self.url_bar.text
        logging.debug(f"Loading URL: {url}")
        self.status_bar.text = "Loading..."
        html_content = self.fetch_content(url)
        self.render_content(html_content)
        self.status_bar.text = "Completed"
        self.history.append(url)
        self.history_index += 1

    def fetch_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            logging.debug(f"Fetched content from {url}")
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to fetch content from {url}: {e}")
            self.status_bar.text = "Failed to load"
            return ""

    def render_content(self, html_content):
        if not html_content:
            logging.error("No HTML content to render")
            return

        logging.debug("Parsing HTML content")
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

        logging.debug("Converting DOM to layout")
        viewport_width = 800  # Example viewport width
        layout_tree = DOMToLayout(dom_tree, styles, media_queries, viewport_width, {}).build_layout_tree()
        layout_tree.calculate_layout()

        logging.debug("Rendering layout")
        renderer = Renderer(layout_tree)
        rendered_content = renderer.render()
        if rendered_content is None:
            logging.error("Rendered content is None")
            return
        self.display_rendered_content(rendered_content)
        logging.debug("Rendering complete")

    def display_rendered_content(self, rendered_content):
        self.content_container.clear_widgets()
        for box in rendered_content:
            self.display_box(box)

    def display_box(self, box):
        with self.content_container.canvas:
            Color(1, 1, 1, 1)  # White color
            Rectangle(pos=(box['left'], box['top']), size=(box['width'], box['height']))
            if box['text']:
                label = Label(text=box['text'], pos=(box['left'], box['top']), size_hint_y=None, height=box['height'], color=(0, 0, 0, 1))
                self.content_container.add_widget(label)
            for child in box['children']:
                self.display_box(child)

    def go_back(self, instance):
        if self.history_index > 0:
            self.history_index -= 1
            url = self.history[self.history_index]
            self.url_bar.text = url
            self.navigate_to_url(instance)

    def go_forward(self, instance):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            url = self.history[self.history_index]
            self.url_bar.text = url
            self.navigate_to_url(instance)

    def refresh_page(self, instance):
        if self.history_index >= 0:
            url = self.history[self.history_index]
            self.url_bar.text = url
            self.navigate_to_url(instance)

class BrowserApp(App):
    def build(self):
        self.title = 'Custom Web Browser'
        main_layout = BoxLayout(orientation='vertical')

        # Add a button to create new tabs
        new_tab_button = Button(text='New Tab', size_hint_y=None, height=40, background_color=(0.1, 0.5, 0.8, 1), color=(1, 1, 1, 1))
        new_tab_button.bind(on_press=self.add_new_tab)

        tab_panel = TabbedPanel(do_default_tab=False)
        self.tab_panel = tab_panel

        # Create the first tab
        tab1 = TabbedPanelItem(text='Tab 1')
        tab1.add_widget(BrowserTab())
        tab_panel.add_widget(tab1)

        main_layout.add_widget(new_tab_button)
        main_layout.add_widget(tab_panel)

        return main_layout

    def add_new_tab(self, instance):
        tab_count = len(self.tab_panel.tab_list) + 1
        new_tab = TabbedPanelItem(text=f'Tab {tab_count}')
        new_tab.add_widget(BrowserTab())
        self.tab_panel.add_widget(new_tab)

if __name__ == '__main__':
    BrowserApp().run()