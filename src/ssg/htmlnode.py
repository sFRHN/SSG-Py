class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict | None = None,
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict | None = props

    def to_html(self):
        raise NotImplementedError("HTMLNode.to_html() not implmented yet")

    def props_to_html(self) -> str:
        if self.props == None:
            return ""

        props_str_repr = ""
        for key, val in self.props:
            props_str_repr += f' {key}:"{val}"'
        return props_str_repr

    def __eq__(self, other) -> bool:
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )

    def __repr__(self) -> str:
        return f"""
        Tag: {self.tag}
        Value: {self.value}
        Children: {self.children}
        Props: {self.props}
        """
