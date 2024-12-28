class LayoutBox:
    def __init__(self, node, styles):
        self.node = node
        self.styles = styles
        self.children = []
        self.width = 0  # Default width
        self.height = 0  # Default height
        self.padding = self.parse_box_model("padding")
        self.border = self.parse_box_model("border")
        self.margin = self.parse_box_model("margin")
        self.position = styles.get("position", "static")
        self.left = int(styles.get("left", "0").replace("px", ""))
        self.top = int(styles.get("top", "0").replace("px", ""))

    def parse_box_model(self, property_name):
        """Parse box model properties (padding, border, margin)."""
        box_model = {
            "top": int(self.styles.get(f"{property_name}-top", "0").replace("px", "")),
            "right": int(self.styles.get(f"{property_name}-right", "0").replace("px", "")),
            "bottom": int(self.styles.get(f"{property_name}-bottom", "0").replace("px", "")),
            "left": int(self.styles.get(f"{property_name}-left", "0").replace("px", ""))
        }
        return box_model

    def add_child(self, child):
        self.children.append(child)

    def calculate_layout(self):
        # Calculate width and height
        self.width = int(self.styles.get("width", "0").replace("px", ""))
        self.height = int(self.styles.get("height", "0").replace("px", ""))

        # Calculate the total width and height including padding, border, and margin
        self.total_width = self.width + self.padding["left"] + self.padding["right"] + self.border["left"] + self.border["right"] + self.margin["left"] + self.margin["right"]
        self.total_height = self.height + self.padding["top"] + self.padding["bottom"] + self.border["top"] + self.border["bottom"] + self.margin["top"] + self.margin["bottom"]

        # Calculate the position based on the parent position and margin
        if self.position == "absolute":
            self.left = self.left
            self.top = self.top
        elif self.position == "relative":
            self.left += self.margin["left"]
            self.top += self.margin["top"]
        else:  # static positioning
            self.left = self.margin["left"]
            self.top = self.margin["top"]

        # Calculate layout for children
        for child in self.children:
            child.calculate_layout()