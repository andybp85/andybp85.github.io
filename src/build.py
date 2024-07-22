from bs4 import BeautifulSoup
from glob import glob
from markdown import markdown
from os import scandir
from pathlib import Path
from sass import compile as compile_sass
from string import Template


def ignore(file_path: str) -> bool:
    return file_path.startswith("env/") \
           or file_path.startswith("fixtures/") \
           or file_path.startswith("test/") \
           or file_path.endswith(".py") \
           or file_path.endswith(".txt") \
           or file_path.endswith("README.md")


def styles(sass_paths: [str]) -> str:
    for sass_file_path in sass_paths:
        with open(sass_file_path, "r") as sass_file:
            sass = sass_file.read()
            yield sass if sass == "" else compile_sass(string=sass, indented=True, output_style="compressed")


def _nav_vals(p: str, page_name: str) -> dict:
    return {
        "page_name": p,
        "text": p.capitalize(),
        "current": ' class="current"' if str(page_name).lower() == str(p).lower() else ""
    }


def make_page_path(pages_path: str, md_file_path: str) -> str:
    return "/".join(Path(md_file_path).parts[len(Path(pages_path).parts):-1])


def nav(pages_path: str, page_name: str) -> str:
    pages = [make_page_path(pages_path, f) + Path(f).stem for f in scandir(pages_path) if f.is_dir()]
    template = Template('<a$current href="$page_name">$text</a>')
    for p in pages:
        yield BeautifulSoup(template.substitute(**_nav_vals(p, page_name)), features="html.parser")


def page(pages_path: str, template_path: str, md_file_path: str) -> str:
    with open(md_file_path, "r") as mdFile, open(template_path, "r") as template:
        template = BeautifulSoup(template, features="html.parser")
        template.find("main").append(BeautifulSoup(markdown(mdFile.read()), features="html.parser"))
        nav_elm = template.find("nav")
        for link in [link for link in nav(pages_path, make_page_path(pages_path, md_file_path))]:
            nav_elm.append(link)
        return template.prettify()


def _paths(pages_path: str, extension: str) -> [str]:
    return glob(str(Path(pages_path).joinpath("**/*." + extension)), recursive=True)


def build(changed_files: [str], pages_path="pages", template_path="template.html", out_path="..") -> None:
    if any(file.endswith(".sass") for file in changed_files):
        with open(Path(out_path, "styles.css"), "w+") as stylesFile:
            for style in styles(sorted(_paths(pages_path, "sass"), key=lambda p: Path(p).name)):
                stylesFile.write(style)

    pages_to_build = []

    if any(file == template_path for file in changed_files):
        pages_to_build = _paths(pages_path, "md")
    elif any(file.endswith(".md") for file in changed_files):
        pages_to_build = [f for f in filter(lambda f: f.endswith(".md"), changed_files)]

    if len(pages_to_build) > 0:
        for md_file_path in pages_to_build:
            contents = page(pages_path, template_path, md_file_path)
            page_path = Path(out_path, make_page_path(pages_path, md_file_path), "index.html")
            page_path.parent.mkdir(exist_ok=True, parents=True)
            page_path.write_text(contents)
