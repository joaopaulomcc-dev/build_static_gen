import os
import shutil as sh
from pathlib import Path

from parser import markdown_to_html_node


def copy_dir(source_dir: Path, destination_dir: Path):
    if source_dir.is_dir():
        # delete destination_dir, if it exists
        if destination_dir.is_dir():
            sh.rmtree(destination_dir)

        # create destination_dir
        os.mkdir(destination_dir)

        for path in source_dir.glob("*"):
            if path.is_file():
                print(f"Copying file {path} to {destination_dir / path.name}")
                sh.copy(path, destination_dir / path.name)
            else:
                print(f"Copying folder {path} to {destination_dir / path.name}")
                copy_dir(path, destination_dir / path.name)


def extract_title(markdown_file: Path):
    lines = markdown_file.read_text().splitlines()

    for line in lines:
        if line.startswith("# "):
            return line.replace("# ", "").strip()

    else:
        raise ValueError("Title was not found")


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    contents = from_path.read_text()
    template = template_path.read_text()

    contents_html = markdown_to_html_node(contents).to_html()

    title = extract_title(from_path)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", contents_html)

    if not dest_path.parent.is_dir():
        os.mkdir(dest_path.parent)

    dest_path.write_text(page)


def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path):
    for path in dir_path_content.glob("*"):
        if path.suffix == ".md":
            dest_path = (dest_dir_path / path.name).with_suffix(".html")
            generate_page(path, template_path, dest_path)

        elif path.is_dir():
            new_dest_dir_path = dest_dir_path / path.name

            if not new_dest_dir_path.is_dir():
                os.mkdir(new_dest_dir_path)

            generate_pages_recursive(path, template_path, new_dest_dir_path)
