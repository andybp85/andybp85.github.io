from functools import reduce
from glob import glob
from os import scandir
from os.path import exists
from pathlib import Path
from string import Template
from typing import TextIO

from bs4 import BeautifulSoup
from markdown import markdown
from sass import compile as compile_sass

'''
Utility Functions

Misc stuff that's better to have a small function handle
'''


def _compile_sass(sass: str) -> str:
    return compile_sass(string=sass, indented=True, output_style='compressed')


def _markdown(md: str) -> str:
    return markdown(md, extensions=['attr_list', 'meta'])


def _nav_vals(p: str, page_name: str) -> dict[str, str]:
    return {
        'page_name': p,
        'text': p.capitalize(),
        'current': ' class="current"' if str(page_name).lower() == str(p).lower() else ''
    }


def _page_path(file_path: str, pages_path: str) -> str:
    return '/'.join(Path(file_path).parts[len(Path(pages_path).parts):-1])


def _soup(html: str | TextIO) -> BeautifulSoup:
    return BeautifulSoup(html, features='html.parser')


def _glob(glob_pattern: str, pages_path: str, recursive: bool = True) -> [str]:
    return glob(str(Path(pages_path).joinpath(glob_pattern)), recursive=recursive)


def _write(contents: str, outfile_path: Path) -> None:
    with open(outfile_path, 'w') as outfile:
        outfile.write(contents)


'''
Maker Functions

These make pieces of page content
'''


def _make_css(sass_file_path: str) -> str:
    with open(sass_file_path, 'r') as sass_file:
        sass = sass_file.read()
        return sass if sass == '' else _compile_sass(sass)


def _make_nav(page_name: str, pages_path: str) -> [str]:
    dirs = [f for f in scandir(pages_path) if f.is_dir()]
    pages = [_page_path(str(d), pages_path) + Path(d).stem for d in dirs]
    template = Template('<a$current href="/$page_name">$text</a>')
    return [template.substitute(**_nav_vals(p, page_name)) for p in pages]


def _make_page(md_file_path: str, pages_path: str, template_path: str, style_path: str = '') -> str:
    with open(md_file_path, 'r') as mdFile, open(template_path, 'r') as template:
        template = _soup(template)
        template.find('main').append(_soup(_markdown(mdFile.read())))
        nav_elm = template.find('nav')
        for link in _make_nav(_page_path(md_file_path, pages_path), pages_path):
            nav_elm.append(_soup(link))
        if style_path != '':
            head_elm = template.find('head')
            head_elm.append(_soup('<link rel="stylesheet" href="/' + style_path + '">'))
        return str(template)


'''
Builder Functions

These write to files and are tested as part of `build()`.
'''


def _build_pages(out_path: str, md_file_paths: [str], pages_path: str, template_path: str) -> None:
    for path in md_file_paths:
        css_path = (Path(_page_path(path, pages_path), Path(path).stem + '.css')
                    if exists(Path(path).with_suffix('.sass')) else '')
        contents = _make_page(path, pages_path, template_path, str(css_path))
        page_path = Path(out_path, _page_path(path, pages_path), 'index.html')
        page_path.parent.mkdir(exist_ok=True, parents=True)
        _write(contents, page_path)


def _build_page_styles(out_path: str, pages_path: str, sass_file_paths: [str]) -> None:
    for path in sass_file_paths:
        css = _make_css(path)
        page_path = _page_path(path, pages_path)
        page_name = Path(path).stem
        _write(css, Path(out_path, page_path, page_name + '.css'))


def _build_styles(out_path: str, pages_path: str) -> None:
    paths = sorted(_glob('[0-9][0-9]*.sass', pages_path), key=lambda p: Path(p).name)
    contents = ''.join([_make_css(style) for style in paths])
    _write(contents, Path(out_path, 'styles.css'))


'''
Main Functions

These are the actual interface to the module, structured around the needs of `livereload`
'''


def build(changed_files: [str] = None, out_path: str = '..', pages_path: str = 'pages',
          template_path: str = 'template.html') -> None:
    """changed_files` works with livereload's watch method's `func` param"""
    print(changed_files)
    global_sass_paths, page_sass_paths = reduce(
        lambda a, c: (a[0] + [c], a[1]) if Path(c).stem[:2].isdigit() else (a[0], a[1] + [c]),
        filter(lambda f: f.endswith('.sass'), changed_files),
        ([], []))
    if len(global_sass_paths) > 0:
        _build_styles(out_path, pages_path)
    if len(page_sass_paths) > 0:
        _build_page_styles(out_path, pages_path, page_sass_paths)

    if any(path == template_path for path in changed_files):
        _build_pages(out_path, _glob('**/*.md', pages_path), pages_path, template_path)
        return

    md_paths = ([p for p in filter(lambda f: f.endswith('.md'), changed_files)]
                + [Path(p).with_suffix('.md') for p in page_sass_paths])
    if len(md_paths) > 0:
        _build_pages(out_path, md_paths, pages_path, template_path)


def build_all(out_path: str = '..', pages_path: str = 'pages',
              template_path: str = 'template.html') -> None:
    build(_glob('**/*.*', pages_path), **locals())


def ignore(file_path: str) -> bool:
    """files that should be ignored when livereload detects changes"""
    return file_path.startswith('env/') \
        or file_path.startswith('fixtures/') \
        or file_path.startswith('test/') \
        or file_path.endswith('.py') \
        or file_path.endswith('.txt') \
        or file_path.endswith('README.md')
