from ssg.html_node import HTMLNode
from ssg.leaf_node import LeafNode
from ssg.markdown_blocks import BlockType, block_to_blocktype, markdown_to_blocks
from ssg.parent_node import ParentNode
from ssg.text_node import TextNode, text_node_to_html_node
from ssg.text_split import text_to_textnodes


def markdown_to_html_node(markdown: str) -> HTMLNode:

    blocks: list[str] = markdown_to_blocks(markdown)

    top_level_children: list[HTMLNode] = []

    for b in blocks:
        b_type: BlockType = block_to_blocktype(b)
        
        match b_type:

            # Simple case - Directly create a ParentNode of the text
            case BlockType.PARAGRAPH:
                text: str = " ".join(b.split())
                parent_node: ParentNode = ParentNode("p", text_to_children(text))
                top_level_children.append(parent_node)

            case BlockType.HEADING:
                # Need to make Nodes out of the text AFTER the #s
                # [0] - Hashtags, [1] - Remaining Text
                sections = b.split(" ", maxsplit=1)
                hashtags = sections[0]
                remaining_text = sections[1]

                tag: str = f"h{hashtags.count('#')}"
                parent_node: ParentNode = ParentNode(tag, text_to_children(remaining_text))
                top_level_children.append(parent_node)

            case BlockType.CODE:
                # Special Case - All text inside a code block should not be formatted
                # CODE block will be a ParentNode(tag: <pre>) with a single LeafNode(tag: <code>)
                # Need to extract the text without the "```" and create a LeafNode out of it

                remaining_text = b.split("```")[1].removeprefix("\n")
                if remaining_text == "":
                    continue

                # Manually creating the LeafNode for the text
                leaf_node: LeafNode = LeafNode("code", remaining_text)
                parent_node: ParentNode = ParentNode("pre", [leaf_node])            
                top_level_children.append(parent_node)

            case BlockType.QUOTE:
                # QUOTE itself will be a parent node
                # Even though each line of the block has a ">", the block will be a single ParentNode(tag: <blockquote>)
                # Need to create a new-line separated list of quotes without ">" 
                # and convert the text into LeafNodes(tag: <li> ) for the ParentNode

                quote_list = b.strip().split("\n")
                quote_list_without_symbol = [q.split(">", maxsplit=1)[1].strip() for q in quote_list]
                quote_block = "\n".join(quote_list_without_symbol)

                parent_node: ParentNode = ParentNode("blockquote", text_to_children(quote_block))
                top_level_children.append(parent_node)

            case BlockType.UNORDERED_LIST:
                # UNORDERED_LIST will be a ParentNode(tag: <ul>)
                # Each list-item will also be a ParentNode(tag: <li>)
                # containing LeafNodes of it's text (without the "-")

                ul_items = b.strip().split("\n")

                list_item_parents: list[HTMLNode] = []
                for item in ul_items:
                    item_without_dash = item.removeprefix("- ")
                    if item_without_dash == "":
                        continue

                    parent_item: ParentNode = ParentNode("li", text_to_children(item_without_dash))
                    list_item_parents.append(parent_item)

                ul_parent: ParentNode = ParentNode("ul", list_item_parents)
                top_level_children.append(ul_parent)

            case BlockType.ORDERED_LIST:
                # UNORDERED_LIST will be a ParentNode(tag: <ol>)
                # Each list-item will also be a ParentNode(tag: <li>) -
                # containing LeafNodes of it's text (without the "1.")
                
                ol_items = b.strip().split("\n")

                list_item_parents: list[HTMLNode] = []
                for item in ol_items:
                    item_without_numdot = item.split(". ")[1]
                    if item_without_numdot == "":
                        continue

                    parent_item: ParentNode = ParentNode("li", text_to_children(item_without_numdot))
                    list_item_parents.append(parent_item)

                ul_parent: ParentNode = ParentNode("ol", list_item_parents)
                top_level_children.append(ul_parent)

            case _:
                raise ValueError(f"Unhandled block type: {b_type}")

    div_parent: ParentNode = ParentNode("div", top_level_children)
    return div_parent

def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes: list[TextNode] = text_to_textnodes(text)
    html_nodes: list[HTMLNode] = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes
