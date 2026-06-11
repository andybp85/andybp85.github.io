from pathlib import Path
from string import Template

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from pygments.formatters.html import HtmlFormatter

SRC_PATH = Path(__file__).parent.parent


def _markdown(md_text: str) -> tuple[str, dict[str, list[str]]]:
    md = markdown.Markdown(extensions=['attr_list', 'fenced_code', 'meta',
                                       CodeHiliteExtension(pygments_formatter=HtmlFormatter,
                                                           wrapcode=True)])
    return md.convert(md_text), md.Meta


def _posts(posts_path: Path) -> list[dict[str, str]]:
    posts = []
    for md_path in sorted(Path(posts_path).glob('*.md')):
        content, meta = _markdown(md_path.read_text())
        if 'date' not in meta:
            raise ValueError(f"post '{md_path.stem}' is missing required 'date' meta")
        posts.append({'categories': meta.get('categories', [''])[0], 'content': content,
                      'date': meta['date'][0], 'slug': md_path.stem,
                      'title': _title(md_path.stem)})
    return sorted(posts, key=lambda p: p['date'], reverse=True)


def _pygments_css() -> str:
    return HtmlFormatter(style='monokai').get_style_defs('.codehilite')


def _subnav(posts: list[dict[str, str]]) -> str:
    return ''.join(
        f'<a href="/blog/{p["slug"]}" data-date="{p["date"]}"'
        + (f' data-categories="{p["categories"]}"' if p['categories'] else '')
        + f'>{p["title"]}</a>'
        for p in posts)


def _title(slug: str) -> str:
    return slug.replace('-', ' ').title()


def build_all(blog_index_template_path: Path = SRC_PATH / 'blog_index_template.html',
              out_path: Path = SRC_PATH.parent,
              post_template_path: Path = SRC_PATH / 'post_template.html',
              posts_path: Path = SRC_PATH / 'posts') -> None:
    """
    :param Path blog_index_template_path: template for /blog/index.html
    :param Path out_path: site root to write into
    :param Path post_template_path: template for /blog/<slug>/index.html
    :param Path posts_path: directory of post markdown sources
    :return: None
    """
    posts = _posts(posts_path)
    subnav = _subnav(posts)
    blog_path = Path(out_path, 'blog')
    blog_path.mkdir(parents=True, exist_ok=True)

    post_template = Template(Path(post_template_path).read_text())
    for post in posts:
        post_path = blog_path / post['slug'] / 'index.html'
        post_path.parent.mkdir(exist_ok=True)
        post_path.write_text(post_template.substitute(
            content=post['content'], subnav=subnav, title=post['title']))

    (blog_path / 'index.html').write_text(
        Template(Path(blog_index_template_path).read_text()).substitute(subnav=subnav))
    Path(out_path, 'pygments.css').write_text(_pygments_css())


def main() -> None:
    build_all()
    print('blog built')
