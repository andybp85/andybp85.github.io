from pathlib import Path

import pytest

from builder import build


def _write_post(posts_path: Path, slug: str, date: str) -> None:
    (posts_path / f'{slug}.md').write_text(f'date: {date}\n\n## {slug}\n')


def test__markdown_converts_text_and_meta():
    html, meta = build._markdown('date: 2016-10-22\n\n## Hi\n')
    assert '<h2>Hi</h2>' in html
    assert meta['date'] == ['2016-10-22']


def test__posts_raises_on_missing_date(tmp_path):
    (tmp_path / 'no-date.md').write_text('## hi\n')
    with pytest.raises(ValueError, match='no-date'):
        build._posts(tmp_path)


def test__posts_reads_meta_and_content(tmp_path):
    (tmp_path / 'a-post.md').write_text('date: 2016-10-22\ncategories: life|sleep\n\n## Hi\n')
    posts = build._posts(tmp_path)
    assert posts == [{'categories': 'life|sleep', 'content': posts[0]['content'],
                      'date': '2016-10-22', 'slug': 'a-post', 'title': 'A Post'}]
    assert '<h2>Hi</h2>' in posts[0]['content']


def test__posts_sorts_newest_first(tmp_path):
    _write_post(tmp_path, 'older-post', '2016-10-22')
    _write_post(tmp_path, 'newer-post', '2020-01-01')
    assert [p['slug'] for p in build._posts(tmp_path)] == ['newer-post', 'older-post']


def test__pygments_css_targets_codehilite():
    assert '.codehilite' in build._pygments_css()


def test__subnav_makes_links_with_data_attrs():
    posts = [{'categories': 'life|sleep', 'content': '', 'date': '2016-10-22',
              'slug': 'a-post', 'title': 'A Post'}]
    assert build._subnav(posts) == ('<a href="/blog/a-post" data-date="2016-10-22"'
                                    ' data-categories="life|sleep">A Post</a>')


def test__subnav_omits_empty_categories():
    posts = [{'categories': '', 'content': '', 'date': '2016-10-22',
              'slug': 'a-post', 'title': 'A Post'}]
    assert build._subnav(posts) == '<a href="/blog/a-post" data-date="2016-10-22">A Post</a>'


def test__title_turns_slug_into_title_case():
    assert build._title('tips-for-waking-up') == 'Tips For Waking Up'
