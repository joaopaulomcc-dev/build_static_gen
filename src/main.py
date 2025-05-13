import shutil as sh
import sys
from pathlib import Path

from site_builder import copy_dir, generate_pages_recursive


def main():
    static_dir = Path("static")
    public_dir = Path("docs")

    basepath = sys.argv[1] if sys.argv[1] else "/"

    index_source_path = Path("content")
    template_path = Path("template.html")
    index_destination_path = public_dir

    if public_dir.is_dir():
        sh.rmtree(public_dir)

    copy_dir(static_dir, public_dir)
    generate_pages_recursive(
        index_source_path, template_path, index_destination_path, basepath=basepath
    )


if __name__ == "__main__":
    main()
