class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html error")
    
    def props_to_html(self):
        html_str = ""
        if self.props:
            for key, val in self.props.items():
                html_str += f' {key}="{val}"'
        return html_str
    
    def __repr__(self):
        return f" \
            tag = {self.tag}, \
            value = {self.value}, \
            children = {self.children}, \
            props = {self.props} \
        "