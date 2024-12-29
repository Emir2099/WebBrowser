import threading
import time

class PythonScripting:
    def __init__(self, dom_tree):
        self.dom_tree = dom_tree
        self.event_queue = []

    def console_log(self, message):
        print(message)

    def set_timeout(self, callback, delay):
        def timeout_handler():
            time.sleep(delay / 1000)
            self.event_queue.append(callback)
        threading.Thread(target=timeout_handler).start()

    def get_element_by_id(self, element_id):
        return self._find_element(self.dom_tree, element_id)

    def _find_element(self, node, element_id):
        if node.attributes.get('id') == element_id:
            return node
        for child in node.children:
            result = self._find_element(child, element_id)
            if result:
                return result
        return None

    def update_element_style(self, element_id, style):
        element = self.get_element_by_id(element_id)
        if element:
            element.styles.update(style)

    def run_event_loop(self):
        while self.event_queue:
            event = self.event_queue.pop(0)
            if isinstance(event, str):
                exec(event, {"python_scripting": self})
            else:
                exec(event.__code__, {"python_scripting": self})