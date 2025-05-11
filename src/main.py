import shutil as sh
from pathlib import Path

from site_builder import copy_dir, generate_page


def main():
    static_dir = Path("static")
    public_dir = Path("public")

    index_source_path = Path("content/index.md")
    template_path = Path("template.html")
    index_destination_path = public_dir / "index.html"

    if public_dir.is_dir():
        sh.rmtree(public_dir)

    copy_dir(static_dir, public_dir)
    generate_page(index_source_path, template_path, index_destination_path)


if __name__ == "__main__":
    main()
