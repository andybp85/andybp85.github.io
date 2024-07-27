from bs4 import BeautifulSoup
from glob import glob
from markdown import markdown
from os import scandir
from pathlib import Path
from sass import compile as compile_sass
from string import Template
from typing import TextIO


def ignore(file_path: str) -> bool:
    return file_path.startswith("env/") \
        or file_path.startswith("fixtures/") \
        or file_path.startswith("test/") \
        or file_path.endswith(".py") \
        or file_path.endswith(".txt") \
        or file_path.endswith("README.md")


def make_css(sass_paths: [str]) -> str:
    for sass_file_path in sass_paths:
        with open(sass_file_path, "r") as sass_file:
            sass = sass_file.read()
            yield sass if sass == "" else compile_sass(string=sass, indented=True,
                                                       output_style="compressed")


def _nav_vals(p: str, page_name: str) -> dict[str, str]:
    return {
        "page_name": p,
        "text": p.capitalize(),
        "current": ' class="current"' if str(page_name).lower() == str(p).lower() else ""
    }


def make_page_path(md_file_path: str, pages_path: str) -> str:
    return "/".join(Path(md_file_path).parts[len(Path(pages_path).parts):-1])


def _make_soup(html: str | TextIO) -> BeautifulSoup:
    return BeautifulSoup(html, features="html.parser")


def make_nav(page_name: str, pages_path: str) -> str:
    dirs = [f for f in scandir(pages_path) if f.is_dir()]
    pages = [make_page_path(str(d), pages_path) + Path(d).stem for d in dirs]
    template = Template('<a$current href="/$page_name">$text</a>')
    for p in pages:
        yield _make_soup(template.substitute(**_nav_vals(p, page_name)))


def _make_markdown(md: str) -> str:
    return markdown(md, extensions=["attr_list", "meta"])


def make_page(md_file_path: str, pages_path: str, template_path: str) -> str:
    with open(md_file_path, "r") as mdFile, open(template_path, "r") as template:
        template = _make_soup(template)
        template.find("main").append(_make_soup(_make_markdown(mdFile.read())))
        nav_elm = template.find("nav")
        for link in [link for link in
                     make_nav(make_page_path(md_file_path, pages_path), pages_path)]:
            nav_elm.append(link)
        return str(template)


def _paths(glob_pattern: str, pages_path: str, recursive: bool = True) -> [str]:
    return glob(str(Path(pages_path).joinpath(glob_pattern)), recursive=recursive)


def _write(contents: str, outfile_path: Path) -> None:
    with open(outfile_path, 'w') as outfile:
        outfile.write(contents)


def _build_pages(out_path: str, pages_path: str, pages_to_build: [str], template_path: str) -> None:
    for md_file_path in pages_to_build:
        contents = make_page(md_file_path, pages_path, template_path)
        page_path = Path(out_path, make_page_path(md_file_path, pages_path), "index.html")
        page_path.parent.mkdir(exist_ok=True, parents=True)
        _write(contents, page_path)


def _build_styles(out_path: str, pages_path: str) -> None:
    paths = sorted(_paths("[0-9][0-9]*.sass", pages_path), key=lambda p: Path(p).name)
    contents = "\n".join([style for style in make_css(paths)])
    _write(contents, Path(out_path, "styles.css"))


def build(changed_files: [str] = None, pages_path: str = "pages", out_path: str = "..",
          template_path: str = "template.html") -> None:
    if changed_files is None:
        print("No Input: " + str([p for p in _paths('**/*.html', out_path) if "src/" not in p]))
        return

    if any(file == template_path for file in changed_files):
        _build_pages(out_path, pages_path, _paths("**/*.md", pages_path), template_path)
        _build_styles(out_path, pages_path)
        return

    md_files = [f for f in filter(lambda f: f.endswith(".md"), changed_files)]
    if len(md_files) > 0:
        _build_pages(out_path, pages_path, md_files, template_path)

    sass_files = [f for f in filter(lambda f: f.endswith(".sass"), changed_files)]
    if any(Path(file).stem[:2].isdigit() for file in sass_files):
        _build_styles(out_path, pages_path)


def build_all(pages_path: str = "pages", template_path: str = "template.html",
              out_path: str = "..") -> None:
    """convenience method, untested"""
    build(glob(pages_path + "**/*"), pages_path, out_path, template_path)
