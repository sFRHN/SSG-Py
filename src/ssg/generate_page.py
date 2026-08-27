import os
from os.path import isdir, isfile

from ssg.markdown_blocks import extract_title
from ssg.markdown_html import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")


    with open(from_path, "r") as file:
        md_content = file.read()

    with open (template_path, "r") as file:
        template_content = file.read()


    md_to_html_str: str = markdown_to_html_node(md_content).to_html()
    md_title: str = extract_title(md_content)

    # Writing the markdown to HTML
    new_title_template = template_content.replace("{{ Title }}", md_title)
    final_template = new_title_template.replace("{{ Content }}", md_to_html_str)


    # Writing the file
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as file:
        file.write(final_template)
        

def generate_pages_recursive(content_dir_path, template_path, dest_dir_path):
    file_list = os.listdir(content_dir_path)

    for file in file_list:

        content_file_path = os.path.join(content_dir_path, file)
        dest_file_path = os.path.join(dest_dir_path, file)

        if os.path.isfile(content_file_path):
            new_path = dest_file_path.removesuffix(".md") + ".html"
            generate_page(content_file_path, template_path, new_path)
        
        elif os.path.isdir(content_file_path):
            generate_pages_recursive(content_file_path, template_path, dest_file_path)
