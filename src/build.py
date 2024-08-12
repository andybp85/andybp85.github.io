import re
import subprocess
from functools import reduce
from glob import glob
from os import path, scandir
from pathlib import Path
from typing import TextIO

from bs4 import BeautifulSoup
import markdown

'''
Utility Functions

Misc stuff that's better to have a small function handle
'''


def _glob(glob_pattern: str, pages_path: str, recursive: bool = True) -> [str]:
    return glob(str(Path(pages_path).joinpath(glob_pattern)), recursive=recursive)


def _markdown(md_text: str) -> (str, str):
    md = markdown.Markdown(extensions=['attr_list', 'meta'])
    return md.convert(md_text), md.Meta


def _markdown_file_paths(changed_files: [str], pages_path: str, page_sass_paths: [str],
                         subnav_template_path: str, template_path: str) -> {str}:
    if any(file_path == template_path for file_path in changed_files):
        return _glob('**/*.md', pages_path)
    else:
        paths_with_subnavs = []
        if any(file_path == subnav_template_path for file_path in changed_files):
            paths_with_subnavs = [str(p[0]) for p in Path('test/pages').walk() if len(p[1]) > 0][1:]
        return set([p for p in filter(lambda f: f.endswith('.md'), changed_files)]
                   + [Path(p).with_suffix('.md') for p in page_sass_paths]
                   + [s for p in paths_with_subnavs for s in _glob('**/*.md', p)])


def _page_path(file_path: str, pages_path: str) -> str:
    return '/'.join(Path(file_path).parts[len(Path(pages_path).parts):-1])


def _handle_sass_partials(changed_files: [str], pages_path: str) -> [str]:
    for sass_path in filter(lambda f: f.endswith('.sass'), changed_files):
        sass_file_name = Path(sass_path).stem
        if sass_file_name[0] == '_':
            import_test = re.compile(f'^@use.*{sass_file_name[1:]}\'$', re.M)
            for check_sass_path in _glob('**/*.sass', pages_path):
                if import_test.search(Path(check_sass_path).read_text()) is not None:
                    yield check_sass_path
        else:
            yield sass_path


def _sass_paths(changed_files: [str], pages_path: str) -> (str, str):
    return reduce(
        lambda a, c: (a[0] + [c], a[1]) if Path(c).stem[:2].isdigit() else (a[0], a[1] + [c]),
        [p for p in _handle_sass_partials(changed_files, pages_path)],
        ([], []))


def _soup(html: str | TextIO) -> BeautifulSoup:
    return BeautifulSoup(html, features='html.parser')


def _write(contents: str, outfile_path: Path) -> None:
    with open(outfile_path, 'w') as outfile:
        outfile.write(contents.replace('\n', ''))


'''
Maker Functions

These make pieces of page content
'''


def _make_css(sass_file_path: str, sass_partials: str) -> str:
    css_output = subprocess.run(
        ['sass', sass_file_path, '-I', sass_partials, '-s', 'compressed'],
        stdout=subprocess.PIPE,
        text=True)
    return css_output.stdout


def _make_nav_link(href: str, text: str, class_attr: str = None,
                   data: dict[str, [str]] = None) -> BeautifulSoup:
    soup = _soup(f'<a href="{href}">{text}</a>')
    if class_attr is not None:
        soup.a.attrs['class'] = class_attr
    if data is not None:
        for k, v in data.items():
            soup.a.attrs[f'--data-{k}'] = v[0]
    return soup


# TODO: fix for subnav_template.html
# File "/Users/andrewstanish/Projects/andybp85.github.io/src/build.py", line 101, in _make_nav
#         sub_page_paths = [Path(f, f.name + '.md') for f in scandir(Path(pages_path, sub_dir))
#                                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#     FileNotFoundError: [Errno 2] No such file or directory: 'pages/pages'
def _make_nav(page_name: str, pages_path: [str], sub_dir: str = '') -> [BeautifulSoup]:
    page_path = Path(pages_path, sub_dir, page_name)
    sub_page_paths = [Path(f, f.name + '.md') for f in scandir(Path(pages_path, sub_dir))
                      if (f.is_dir())]
    for p in sub_page_paths:
        class_attr = 'current' if page_path == p.parent else None
        _, meta = _markdown(p.read_text())
        yield _make_nav_link('/' + _page_path(str(p), pages_path), p.stem.replace('-', ' ').title(),
                             class_attr, meta)


def _make_page(md_file_path: str, pages_path: str, style_path: str,
               subnav_template_path: str, template_path: str) -> str:
    index_soup = _soup(Path(template_path).read_text())
    main_elm = index_soup.find('main')
    main_elm.append(_soup(_markdown(Path(md_file_path).read_text())[0]))
    page_path = _page_path(md_file_path, pages_path)
    top_level = page_path.split('/')[0]
    nav = index_soup.find('nav')
    for nav_link in _make_nav(top_level, pages_path):
        nav.append(nav_link)

    if str(Path(md_file_path).parent) != pages_path:
        sub_nav_links = [a for a in _make_nav(Path(page_path).parts[-1], pages_path, top_level)]
        if len(sub_nav_links) > 0:
            subnav_soup = _soup(Path(subnav_template_path).read_text())
            subnav = subnav_soup.find('nav')
            for link in sub_nav_links:
                subnav.append(link)
            main_elm.insert_before(subnav_soup)

    if style_path != '':
        index_soup.find('head').append(_soup('<link rel="stylesheet" href="/' + style_path + '">'))

    return str(index_soup).replace('\n', '')


def _make_styles(pages_path: str, sass_partials: str) -> str:
    paths = sorted(_glob('[0-9][0-9]*.sass', pages_path), key=lambda p: Path(p).name)
    return ''.join([_make_css(style, sass_partials) for style in paths])


'''
Main Functions

These are the actual interface to the module, structured around the needs of `livereload`
'''


def build(changed_files: [str] = None, out_path: str = '..', pages_path: str = 'pages',
          sass_partials: str = 'sass-partials', subnav_template_path: str = 'subnav_template.html',
          template_path: str = 'template.html') -> None:
    """
    :param [str] changed_files: see livereload's watch method's `func` param
    :param str out_path: destination path
    :param str pages_path: path to Markdown source directory
    :param str sass_partials: path to Sass partials directory
    :param subnav_template_path: path to subnav template
    :param str template_path: path to HTML template file
    :return: None
    """
    global_sass_paths, page_sass_paths = _sass_paths(changed_files, pages_path)

    if len(global_sass_paths) > 0:
        _write(_make_styles(pages_path, sass_partials), Path(out_path, 'styles.css'))

    for p in page_sass_paths:
        _write(_make_css(p, sass_partials),
               Path(out_path, _page_path(p, pages_path), Path(p).stem + '.css'))

    for md_path in _markdown_file_paths(changed_files, pages_path, page_sass_paths,
                                        subnav_template_path, template_path):
        css_path = Path(_page_path(md_path, pages_path), Path(md_path).stem + '.css')
        style_path = str(css_path) if path.exists(Path(md_path).with_suffix('.sass')) else ''
        page_path = Path(out_path, _page_path(md_path, pages_path), 'index.html')
        page_path.parent.mkdir(exist_ok=True, parents=True)
        _write(_make_page(md_path, pages_path, style_path, subnav_template_path, template_path),
               page_path)


def build_all(pages_path: str = 'pages', **kwargs) -> None:
    """
    :param pages_path: see build()
    :param kwargs: see build()
    :return: None

    convenience method to build everything, also runs on startup
    """
    build(_glob('**/*.*', pages_path), **kwargs)


def ignore(file_path: str) -> bool:
    """
    :param str file_path: see livereload's watch method's `ignore` param
    :return: None

    files that should be ignored when livereload detects changes
    """
    return file_path.startswith('env/') \
        or file_path.startswith('fixtures/') \
        or file_path.startswith('test/') \
        or file_path.endswith('.py') \
        or file_path.endswith('.txt') \
        or file_path.endswith('README.md')
