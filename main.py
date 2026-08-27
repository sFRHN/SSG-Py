import sys

from ssg.copy_files import copy_files
from ssg.generate_page import generate_pages_recursive


def main():
    
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1] 

    copy_files("static", "docs")
    generate_pages_recursive(base_path, "content", "template.html", "docs")

if __name__ == "__main__":
    main()
