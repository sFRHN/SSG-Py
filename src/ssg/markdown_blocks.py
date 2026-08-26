def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    for block in markdown.split("\n\n"):
        stripped_block = block.strip()
        if stripped_block == "":
            continue
        blocks.append(stripped_block)

    return blocks
