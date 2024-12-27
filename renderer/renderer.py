class Renderer:
    def __init__(self, layout_tree):
        self.layout_tree = layout_tree

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

        # Simulating rendering in the terminal
        print(f"{indent}{content} (Color: {color}, Font-size: {font_size})")

        for child in box.children:
            self.draw_element(child, depth + 1)

    def render(self):
        print("Rendering Layout Tree:")
        self.draw_element(self.layout_tree)
        print("Rendering Complete.")
