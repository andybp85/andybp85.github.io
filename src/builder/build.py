from datetime import date
from functools import partial
from pathlib import Path
from string import Template

import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from pygments.formatters.html import HtmlFormatter

SRC_PATH = Path(__file__).parent.parent


def _markdown(md_text: str) -> tuple[str, dict[str, list[str]]]:
    # linespans wraps each source line in its own <span> so a CSS counter can
    # number the lines and soft-wrap them with a hanging indent (see projects.css).
    md = markdown.Markdown(extensions=['attr_list', 'fenced_code', 'meta',
                                       CodeHiliteExtension(pygments_formatter=partial(HtmlFormatter,
                                                                                      linespans='line'),
                                                           wrapcode=True)])
    return md.convert(md_text), md.Meta


def _posts(posts_path: Path) -> list[dict[str, str]]:
    posts = []
    for md_path in sorted(Path(posts_path).glob('*.md')):
        content, meta = _markdown(md_path.read_text(encoding='utf-8'))
        if 'date' not in meta:
            raise ValueError(f"post '{md_path.stem}' is missing required 'date' meta")
        date_str = meta['date'][0]
        date.fromisoformat(date_str)
        posts.append({'categories': meta.get('categories', [''])[0], 'content': content,
                      'date': date_str, 'slug': md_path.stem,
                      'title': _title(md_path.stem)})
    return sorted(posts, key=lambda p: p['date'], reverse=True)


def _pygments_css() -> str:
    return HtmlFormatter(style='monokai').get_style_defs('.codehilite')


def _subnav(posts: list[dict[str, str]], current_slug: str | None = None) -> str:
    return ''.join(
        f'<a href="/blog/{p["slug"]}" data-date="{p["date"]}"'
        + (f' data-categories="{p["categories"]}"' if p['categories'] else '')
        + (' class="current"' if p['slug'] == current_slug else '')
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
    blog_path = Path(out_path, 'blog')
    blog_path.mkdir(parents=True, exist_ok=True)

    post_template = Template(Path(post_template_path).read_text(encoding='utf-8'))
    for post in posts:
        post_path = blog_path / post['slug'] / 'index.html'
        post_path.parent.mkdir(exist_ok=True)
        post_path.write_text(post_template.substitute(
            content=post['content'], subnav=_subnav(posts, post['slug']),
            title=post['title']), encoding='utf-8')

    (blog_path / 'index.html').write_text(
        Template(Path(blog_index_template_path).read_text(encoding='utf-8')).substitute(subnav=_subnav(posts)),
        encoding='utf-8')
    Path(out_path, 'pygments.css').write_text(_pygments_css(), encoding='utf-8')


def main() -> None:
    build_all()
    print('blog built')
