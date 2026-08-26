from ssg.markdown_extract import extract_markdown_images, extract_markdown_links
from ssg.textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    first_node = TextNode(text=text, text_type=TextType.TEXT)

    all_nodes = [first_node]
    all_nodes = split_nodes_image(all_nodes)
    all_nodes = split_nodes_links(all_nodes)
    all_nodes = split_nodes_delimiter(all_nodes, "**", TextType.BOLD)
    all_nodes = split_nodes_delimiter(all_nodes, "_", TextType.ITALIC)
    all_nodes = split_nodes_delimiter(all_nodes, "`", TextType.CODE)

    return all_nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:

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
            raise ValueError(
                f"Matching closing delimiter ({delimiter}) not found - {node}"
            )

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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Need to keep splitting the text into sections for processing
        # Get all possible images from the given node.text to split the text by
        current_text: str = node.text
        all_images: list[tuple[str, str]] = extract_markdown_images(current_text)

        # If no images were in the list, move on
        if len(all_images) == 0:
            new_nodes.append(node)
            continue

        for alt_text, url in all_images:
            image_text_md = f"![{alt_text}]({url})"
            text_split_by_image = current_text.split(image_text_md, maxsplit=1)

            # If the split didn't output exactly 2 sections (before and after the image), means formatting error
            if len(text_split_by_image) != 2:
                raise ValueError(f"Node wasn't properly formatted - {node}")

            # If there is text before the image, add it as a TEXT node
            if text_split_by_image[0] != "":
                new_nodes.append(TextNode(text=text_split_by_image[0], text_type=TextType.TEXT))

            new_nodes.append(TextNode(text=alt_text, text_type=TextType.IMAGE, url=url))

            current_text = text_split_by_image[1]

        # If there is text remaining at the end after all images, add it as a TEXT Node
        if current_text != "":
            new_nodes.append(TextNode(text=current_text, text_type=TextType.TEXT))

    return new_nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Need to keep splitting the text into sections for processing
        # Get all possible links from the given node.text to split the text by
        current_text: str = node.text
        all_links: list[tuple[str, str]] = extract_markdown_links(current_text)

        # If no links were in the list, move on
        if len(all_links) == 0:
            new_nodes.append(node)
            continue

        for alt_text, url in all_links:
            link_text_md = f"[{alt_text}]({url})"
            text_split_by_link = current_text.split(link_text_md, maxsplit=1)

            # If the split didn't output exactly 2 sections (before and after the link), means formatting error
            if len(text_split_by_link) != 2:
                raise ValueError(f"Node wasn't properly formatted - {node}")

            # If there is text before the link, add it as a TEXT node
            if text_split_by_link[0] != "":
                new_nodes.append(TextNode(text=text_split_by_link[0], text_type=TextType.TEXT))

            new_nodes.append(TextNode(text=alt_text, text_type=TextType.LINK, url=url))

            current_text = text_split_by_link[1]

        # If there is text remaining at the end after all links, add it as a TEXT Node
        if current_text != "":
            new_nodes.append(TextNode(text=current_text, text_type=TextType.TEXT))

    return new_nodes
