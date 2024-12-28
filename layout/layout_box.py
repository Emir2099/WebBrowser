import time

class LayoutBox:
    def __init__(self, node, styles, event_handlers):
        self.node = node
        self.styles = styles
        self.children = []
        self.width = 0  # Default width
        self.height = 0  # Default height
        self.padding = self.parse_box_model("padding")
        self.border = self.parse_box_model("border")
        self.margin = self.parse_box_model("margin")
        self.position = styles.get("position", "static")
        self.display = styles.get("display", "block")
        self.left = int(styles.get("left", "0").replace("px", ""))
        self.top = int(styles.get("top", "0").replace("px", ""))
        self.z_index = int(styles.get("z-index", "0"))
        self.overflow = styles.get("overflow", "visible")
        self.animation = styles.get("animation", "")
        self.transition = styles.get("transition", "")
        self.event_id = None

        # Handle onclick event
        if "onclick" in node.attributes:
            self.event_id = node.attributes["id"]
            event_handlers[self.event_id] = self.handle_click

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
        elif self.position == "fixed":
            self.left = self.left
            self.top = self.top
        elif self.position == "sticky":
            self.left = self.left
            self.top = self.top
        else:  # static positioning
            self.left = self.margin["left"]
            self.top = self.margin["top"]

        # Calculate layout for children
        if self.display == "flex":
            self.calculate_flex_layout()
        elif self.display == "grid":
            self.calculate_grid_layout()
        else:
            for child in self.children:
                child.calculate_layout()

    def calculate_flex_layout(self):
        # Implement basic flexbox layout calculation
        flex_direction = self.styles.get("flex-direction", "row")
        justify_content = self.styles.get("justify-content", "flex-start")
        align_items = self.styles.get("align-items", "stretch")
        flex_wrap = self.styles.get("flex-wrap", "nowrap")

        # Calculate positions of children based on flex properties
        main_axis_size = self.width if flex_direction == "row" else self.height
        cross_axis_size = self.height if flex_direction == "row" else self.width

        main_axis_pos = 0
        for child in self.children:
            child_width = int(child.styles.get("width", "0").replace("px", ""))
            child_height = int(child.styles.get("height", "0").replace("px", ""))
            flex_grow = float(child.styles.get("flex-grow", "0"))
            flex_shrink = float(child.styles.get("flex-shrink", "1"))
            flex_basis = int(child.styles.get("flex-basis", "0").replace("px", ""))

            if flex_direction == "row":
                child.left = main_axis_pos
                child.top = 0
                main_axis_pos += child_width + flex_basis
            else:
                child.left = 0
                child.top = main_axis_pos
                main_axis_pos += child_height + flex_basis

            # Apply flex-grow and flex-shrink
            if flex_grow > 0:
                child.width += (main_axis_size - main_axis_pos) * (flex_grow / sum([float(c.styles.get("flex-grow", "0")) for c in self.children]))
            if flex_shrink > 0:
                child.width -= (main_axis_size - main_axis_pos) * (flex_shrink / sum([float(c.styles.get("flex-shrink", "1")) for c in self.children]))

    def calculate_grid_layout(self):
        # Implement basic grid layout calculation
        grid_template_columns = self.styles.get("grid-template-columns", "").split()
        grid_template_rows = self.styles.get("grid-template-rows", "").split()
        grid_gap = self.styles.get("grid-gap", "0px").replace("px", "")

        # Handle fractional units (fr)
        column_widths = self.calculate_fractional_units(grid_template_columns, self.width)
        row_heights = self.calculate_fractional_units(grid_template_rows, self.height)

        # Calculate positions of children based on grid properties
        for child in self.children:
            grid_column = int(child.styles.get("grid-column", "1")) - 1
            grid_row = int(child.styles.get("grid-row", "1")) - 1
            child.left = sum(column_widths[:grid_column]) + grid_column * int(grid_gap)
            child.top = sum(row_heights[:grid_row]) + grid_row * int(grid_gap)
            child.width = column_widths[grid_column]
            child.height = row_heights[grid_row]

    def calculate_fractional_units(self, template, total_size):
        """Calculate sizes for fractional units (fr) in grid layout."""
        sizes = []
        total_fr = sum([float(size.replace("fr", "")) for size in template if "fr" in size])
        remaining_size = total_size - sum([int(size.replace("px", "")) for size in template if "px" in size])
        for size in template:
            if "fr" in size:
                fr = float(size.replace("fr", ""))
                sizes.append((fr / total_fr) * remaining_size)
            elif "px" in size:
                sizes.append(int(size.replace("px", "")))
            elif size == "auto":
                sizes.append(remaining_size / len([s for s in template if s == "auto"]))
            else:
                sizes.append(0)  # Default to 0 for unsupported units
        return sizes

    def simulate_animation(self):
        if self.animation:
            animation_name, animation_duration = self.animation.split()
            animation_duration = float(animation_duration.replace("s", ""))
            steps = 10
            step_duration = animation_duration / steps

            for step in range(steps + 1):
                progress = step / steps
                self.apply_animation_step(animation_name, progress)
                self.render()
                time.sleep(step_duration)

    def apply_animation_step(self, animation_name, progress):
        # Example animation: move from left to right
        if animation_name == "move-right":
            self.left = int(progress * 100)  # Move 100px to the right

    def render(self):
        # Render the layout tree (simplified for demonstration)
        print(f"Rendering Layout Tree at left: {self.left}, top: {self.top}")
        for child in self.children:
            child.render()

    def handle_click(self):
        print(f"Button with ID {self.event_id} clicked!")