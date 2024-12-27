class LayoutBox:
    def __init__(self, node, styles):
        self.node = node
        self.styles = styles
        self.children = []
        self.width = 0  # Default width
        self.height = 0  # Default height

    def add_child(self, child):
        self.children.append(child)

    def calculate_layout(self):
        # Placeholder layout calculation
        self.width = int(self.styles.get("width", "800"))
        self.height = int(self.styles.get("height", "600"))
