import re

class CSSParser:
    def parse(self, css_content):
        styles = {}
        
        # Remove comments
        css_content = re.sub(r"/\*.*?\*/", "", css_content, flags=re.DOTALL)

        # Split the content into rules by "}"
        rules = css_content.split("}")
        
        for rule in rules:
            if "{" in rule:
                selector, properties = rule.split("{", 1)  # Split only at the first '{'
                selector = selector.strip()

                # Parse the properties
                properties = properties.strip()
                if properties:
                    styles[selector] = {}
                    for prop in properties.split(";"):
                        # Split properties into key and value, handling potential spaces
                        if ":" in prop:
                            key, value = prop.split(":", 1)
                            styles[selector][key.strip()] = value.strip()

        return styles
