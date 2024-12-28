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
        background_color = styles.get("background-color", "transparent")
        text_decoration = styles.get("text-decoration", "none")
        font_weight = styles.get("font-weight", "normal")

        # Simulating rendering in the terminal
        print(f"{indent}{content} (Color: {color}, Font-size: {font_size}, Background-color: {background_color}, Text-decoration: {text_decoration}, Font-weight: {font_weight}, Width: {box.width}px, Height: {box.height}px, Padding: {box.padding}, Border: {box.border}, Margin: {box.margin}, Position: {box.position}, Left: {box.left}px, Top: {box.top}px)")

        for child in box.children:
            self.draw_element(child, depth + 1)

    def render(self):
        print("Rendering Layout Tree:")
        self.draw_element(self.layout_tree)
        print("Rendering Complete.")