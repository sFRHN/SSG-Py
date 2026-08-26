from ssg.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Splitting text with MATCHING delimiter produces a list where:
        # even index -> regular text
        # odd  index -> formatted text
        #
        # Splitting text with UNMATCHED closing delimiter always produces a list with even num of values

        node_sections = node.text.split(delimiter)

        if len(node_sections) % 2 == 0:
            raise ValueError(f"Matching closing delimiter ({delimiter}) not found - {node}")

        for index, val in enumerate(node_sections):
            
            # Skip empty values - can happen when delimiter is at the start/end of a line
            if val == "":
                continue

            if index % 2 != 0:
                new_node = TextNode(text=val, text_type=text_type)
                new_nodes.append(new_node)

            else:
                new_node = TextNode(text=val, text_type=TextType.TEXT)
                new_nodes.append(new_node)


    return new_nodes

