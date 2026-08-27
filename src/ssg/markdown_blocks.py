from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        stripped_block = block.strip()
        if stripped_block == "":
            continue
        blocks.append(stripped_block)

    return blocks

def block_to_blocktype(block: str) -> BlockType:
    
    # Split into lines for checking QUOTE, UNORDERED_LIST and ORDERED_LIST
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(lines[i].startswith(f"{i+1}. ") for i, _ in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
