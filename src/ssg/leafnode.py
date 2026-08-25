from ssg.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str | None, props: dict | None = None):
        super().__init__(tag, value, None, props)


    def to_html(self) -> str:
        if self.value == "" or self.value == None:
            raise ValueError("LeafNode has no value")

        if self.tag == None:
            return self.value

        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self) -> str:
        return f"""
        Tag: {self.tag}
        Value: {self.value}
        Props: {self.props}
        """
