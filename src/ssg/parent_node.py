from ssg.html_node import HTMLNode


class ParentNode(HTMLNode):

    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode has no tag")

        if self.children is None:
            raise ValueError("ParentNode has no children")

        chilldren_str = ""
        for node in self.children:
            chilldren_str += node.to_html()
        final_str = f"<{self.tag}{self.props_to_html()}>{chilldren_str}</{self.tag}>"
        return final_str
