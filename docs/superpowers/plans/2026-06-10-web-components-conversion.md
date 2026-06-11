# Web Components + Modern CSS Conversion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Python-generates-everything + Sass build with hand-written HTML using vanilla web components, plain modern CSS, and a small uv-managed Python tool that only builds the blog from markdown and serves the site locally.

**Architecture:** The repo root is the served site (GitHub Pages). Shared chrome (`<site-header>`, `<site-footer>`) is rendered by one zero-dependency ES module; `<sub-nav>` is a styled-only custom element whose links are plain light-DOM children. A Python package in `src/` (uv project, deps: `markdown` + `Pygments`) converts `src/posts/*.md` into `/blog/<slug>/index.html` pages plus `/blog/index.html`, and runs a stdlib dev server with an mtime-polling rebuild watcher.

**Tech Stack:** Vanilla JS custom elements (light DOM), modern CSS (custom properties, native nesting, `:has()`, range media queries), Python 3.12 + uv + hatchling, `markdown`, `Pygments`, `pytest`.

**Spec:** `docs/superpowers/specs/2026-06-10-web-components-conversion-design.md`

**Working directory note:** All `uv` commands run from `src/` — written below as `(cd src && uv run …)`. All file paths are relative to the repo root.

**Code style (from README, still applies):** functions over OOP, alphabetical ordering wherever possible, `_`-prefixed module-private functions, type hints with return types (including `-> None`), 100-char lines, side effects (file writes) localized to one function per kind.

---

### Task 1: uv project scaffold + working pre-commit hook

The old `src/` virtualenv setup (`setup.sh`, `requirements.txt`, `penv`) is replaced by a uv project. The repo's `.git/hooks/pre-commit` currently runs the **old** broken test suite, so it must be replaced now or every commit in this plan fails.

**Files:**
- Create: `src/pyproject.toml`
- Create: `src/builder/__init__.py`
- Create: `src/test/__init__.py`
- Modify: `src/.gitignore`
- Modify: `src/pre-commit`
- Modify: `.git/hooks/pre-commit` (not tracked by git)
- Move: `src/pages/blog/tips-for-waking-up-far-far-too-early/tips-for-waking-up-far-far-too-early.md` → `src/posts/tips-for-waking-up-far-far-too-early.md`

- [ ] **Step 1: Write `src/pyproject.toml`**

```toml
[build-system]
build-backend = "hatchling.build"
requires = ["hatchling"]

[dependency-groups]
dev = [
    "pytest>=8",
    "pytest-cov>=5",
]

[project]
dependencies = [
    "markdown>=3.6",
    "pygments>=2.18",
]
description = "Builds the blog from markdown and serves the site locally."
name = "builder"
requires-python = ">=3.12"
version = "1.0.0"

[project.scripts]
build = "builder.build:main"
serve = "builder.serve:main"

[tool.hatch.build.targets.wheel]
packages = ["builder"]

[tool.pytest.ini_options]
testpaths = ["test"]
```

- [ ] **Step 2: Create the package and test dirs**

Create `src/builder/__init__.py` and `src/test/__init__.py`, both empty.

If an old `src/test/` directory exists with stale content, remove its contents first (check with `ls src/test/`).

- [ ] **Step 3: Move the post markdown into `src/posts/`**

```bash
mkdir src/posts
git mv src/pages/blog/tips-for-waking-up-far-far-too-early/tips-for-waking-up-far-far-too-early.md src/posts/
```

- [ ] **Step 4: Sync the environment**

Run: `(cd src && uv sync)`
Expected: creates `src/.venv`, installs markdown, pygments, pytest, pytest-cov; writes `src/uv.lock`.

- [ ] **Step 5: Replace `src/.gitignore`**

```
.venv
htmlcov
__pycache__
.pytest_cache
.coverage
```

- [ ] **Step 6: Replace `src/pre-commit` and install it**

New content of `src/pre-commit`:

```sh
#!/bin/sh
cd src && uv run pytest
```

Then install it:

```bash
cp src/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

- [ ] **Step 7: Commit (bypass hook once — empty test suite exits 5)**

```bash
git add -A src
git commit --no-verify -m "scaffold uv project for blog builder"
```

---

### Task 2: Builder pure functions (TDD)

All the no-side-effect logic: slug→title, markdown conversion with meta, post collection/sorting, sub-nav link generation, Pygments CSS.

**Files:**
- Create: `src/builder/build.py`
- Create: `src/test/test_build.py`

- [ ] **Step 1: Write the failing tests**

`src/test/test_build.py`:

```python
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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `(cd src && uv run pytest -v)`
Expected: FAIL — `AttributeError`/`ImportError` (module `builder.build` doesn't exist yet).

- [ ] **Step 3: Write the implementation**

`src/builder/build.py`:

```python
from pathlib import Path

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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `(cd src && uv run pytest -v)`
Expected: 8 passed.

- [ ] **Step 5: Commit**

```bash
git add src/builder/build.py src/test/test_build.py
git commit -m "add blog builder pure functions"
```

---

### Task 3: Templates and build_all (TDD)

`build_all()` is the one function with file-write side effects: it renders every post page, the blog index, and the Pygments CSS. Templating is `string.Template` (`$content`, `$subnav`, `$title`) — **not** `str.format`, because the templates contain CSS braces.

**Files:**
- Create: `src/post_template.html`
- Create: `src/blog_index_template.html`
- Modify: `src/builder/build.py` (append `build_all`, `main`)
- Modify: `src/test/test_build.py` (append tests)

- [ ] **Step 1: Write the failing tests**

Append to `src/test/test_build.py`:

```python
@pytest.fixture
def site(tmp_path):
    posts_path = tmp_path / 'posts'
    posts_path.mkdir()
    _write_post(posts_path, 'first-post', '2016-10-22')
    out_path = tmp_path / 'out'
    out_path.mkdir()
    post_template_path = tmp_path / 'post_template.html'
    post_template_path.write_text('<title>$title</title><nav>$subnav</nav><main>$content</main>')
    blog_index_template_path = tmp_path / 'blog_index_template.html'
    blog_index_template_path.write_text('<nav>$subnav</nav>')
    return {'blog_index_template_path': blog_index_template_path, 'out_path': out_path,
            'post_template_path': post_template_path, 'posts_path': posts_path}


def test_build_all_writes_blog_index(site):
    build.build_all(**site)
    assert 'href="/blog/first-post"' in (site['out_path'] / 'blog' / 'index.html').read_text()


def test_build_all_writes_post_pages(site):
    build.build_all(**site)
    post_html = (site['out_path'] / 'blog' / 'first-post' / 'index.html').read_text()
    assert '<title>First Post</title>' in post_html
    assert '<h2>first-post</h2>' in post_html
    assert 'href="/blog/first-post"' in post_html


def test_build_all_writes_pygments_css(site):
    build.build_all(**site)
    assert '.codehilite' in (site['out_path'] / 'pygments.css').read_text()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `(cd src && uv run pytest -v)`
Expected: 3 new FAILs — `AttributeError: module 'builder.build' has no attribute 'build_all'`.

- [ ] **Step 3: Implement `build_all` and `main`**

Append to `src/builder/build.py` (and add `from string import Template` to the stdlib imports at the top, keeping imports alphabetical):

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `(cd src && uv run pytest -v)`
Expected: 11 passed.

- [ ] **Step 5: Write `src/post_template.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="darkreader-lock">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Andy's biographical site for projects and random thoughts.">
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'self'; script-src-elem 'self' 'unsafe-inline' *.getclicky.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src *.getclicky.com">
    <title>$title — Andy Stanish</title>
    <link href="/icons/favicon.ico" rel="icon" type="image/ico">
    <link rel="preload" href="/fonts/B612-Regular/B612-Regular.woff" as="font" type="font/woff" crossorigin>
    <link rel="preload" href="/fonts/Inter/InterVariable.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/fonts/Inter/InterVariable-Italic.woff2" as="font" type="font/woff2" crossorigin>
    <style>
        body {
            visibility: hidden;
        }

        html {
            background-image: linear-gradient(270deg, #222 90%, #2A2A2A 100%);
        }

        @media (prefers-color-scheme: light) {
            html {
                background-image: linear-gradient(90deg, #f9f9f9 95%, #BBB 100%);
            }
        }
    </style>
    <link as="style" href="/styles.css" rel="preload">
    <link rel="stylesheet" href="/styles.css">
    <link rel="stylesheet" href="/blog/blog.css">
    <link rel="stylesheet" href="/pygments.css">
    <script type="module" src="/components.js"></script>
</head>
<body>
<site-header></site-header>
<sub-nav>
    <label>Posts</label>
    <nav>$subnav</nav>
</sub-nav>
<main>$content</main>
<site-footer></site-footer>
</body>
</html>
```

- [ ] **Step 6: Write `src/blog_index_template.html`**

Identical shell, different title/main/css links:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta name="darkreader-lock">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="Andy's biographical site for projects and random thoughts.">
    <meta http-equiv="Content-Security-Policy"
          content="default-src 'self'; script-src-elem 'self' 'unsafe-inline' *.getclicky.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src *.getclicky.com">
    <title>Blog — Andy Stanish</title>
    <link href="/icons/favicon.ico" rel="icon" type="image/ico">
    <link rel="preload" href="/fonts/B612-Regular/B612-Regular.woff" as="font" type="font/woff" crossorigin>
    <link rel="preload" href="/fonts/Inter/InterVariable.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/fonts/Inter/InterVariable-Italic.woff2" as="font" type="font/woff2" crossorigin>
    <style>
        body {
            visibility: hidden;
        }

        html {
            background-image: linear-gradient(270deg, #222 90%, #2A2A2A 100%);
        }

        @media (prefers-color-scheme: light) {
            html {
                background-image: linear-gradient(90deg, #f9f9f9 95%, #BBB 100%);
            }
        }
    </style>
    <link as="style" href="/styles.css" rel="preload">
    <link rel="stylesheet" href="/styles.css">
    <script type="module" src="/components.js"></script>
</head>
<body>
<site-header></site-header>
<sub-nav>
    <label>Posts</label>
    <nav>$subnav</nav>
</sub-nav>
<main>
    <h2>Random Musings and Rants</h2>
    <p>I'm starting this off with a post I made in Facebook back in 2016 from when I first realized
        I'm way more of a morning person. It's dated, but still a fun read. Hope you enjoy!</p>
</main>
<site-footer></site-footer>
</body>
</html>
```

- [ ] **Step 7: Commit**

```bash
git add src/builder/build.py src/test/test_build.py src/post_template.html src/blog_index_template.html
git commit -m "add build_all with post and blog index templates"
```

---

### Task 4: Dev server with rebuild watcher

Stdlib only: `http.server` serving the repo root on :5500, plus a daemon thread polling mtimes of `src/posts/*.md` and `src/*.html` every second, rebuilding on change. No livereload — browser refresh is manual.

**Files:**
- Create: `src/builder/serve.py`
- Modify: `src/test/test_build.py` → no; create `src/test/test_serve.py`

- [ ] **Step 1: Write the failing test**

`src/test/test_serve.py`:

```python
from builder import serve


def test__snapshot_maps_watched_files_to_mtimes(tmp_path):
    (tmp_path / 'posts').mkdir()
    post = tmp_path / 'posts' / 'a-post.md'
    post.write_text('hi')
    template = tmp_path / 'post_template.html'
    template.write_text('t')
    (tmp_path / 'ignored.css').write_text('not watched')
    assert set(serve._snapshot(tmp_path)) == {str(post), str(template)}
```

- [ ] **Step 2: Run test to verify it fails**

Run: `(cd src && uv run pytest test/test_serve.py -v)`
Expected: FAIL — `ImportError` (no module `builder.serve`).

- [ ] **Step 3: Write the implementation**

`src/builder/serve.py`:

```python
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from time import sleep

from builder.build import SRC_PATH, build_all

WATCH_GLOBS = ['*.html', 'posts/*.md']


def _snapshot(base_path: Path = SRC_PATH) -> dict[str, float]:
    return {str(p): p.stat().st_mtime for g in WATCH_GLOBS for p in Path(base_path).glob(g)}


def _watch() -> None:
    seen = _snapshot()
    while True:
        sleep(1)
        now = _snapshot()
        if now != seen:
            seen = now
            print('rebuilding blog...')
            build_all()


def main() -> None:
    build_all()
    Thread(target=_watch, daemon=True).start()
    server = ThreadingHTTPServer(
        ('', 5500), partial(SimpleHTTPRequestHandler, directory=str(SRC_PATH.parent)))
    print('serving at http://localhost:5500/')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `(cd src && uv run pytest -v)`
Expected: 12 passed.

- [ ] **Step 5: Commit**

```bash
git add src/builder/serve.py src/test/test_serve.py
git commit -m "add stdlib dev server with rebuild watcher"
```

---

### Task 5: Web components module

One vanilla ES module, zero dependencies, light DOM. `<sub-nav>` needs no JS at all (undefined custom elements still render children and can be styled), so only `site-header` and `site-footer` are defined. The Clicky `<script>` must be created via `document.createElement` — scripts injected with `innerHTML` never execute. The old `<noscript>` tracking pixel is dropped: the footer itself requires JS now, so a noscript fallback inside it is meaningless.

**Files:**
- Create: `components.js` (repo root)

- [ ] **Step 1: Write `components.js`**

```js
const navLink = (href, text) => {
    const current = location.pathname.startsWith(href) ? ' class="current"' : "";
    return `<a href="${href}"${current}>${text}</a>`;
};

customElements.define("site-header", class extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <header>
                <h1><a href="/">Andy Stanish</a></h1>
                <nav aria-label="Main">
                    ${navLink("/about", "About")}
                    ${navLink("/blog", "Blog")}
                    ${navLink("/projects", "Projects")}
                </nav>
            </header>`;
    }
});

customElements.define("site-footer", class extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
            <footer>
                <div id="social-media-links">
                    <a href="https://github.com/andybp85" target="_blank" title="Andy's Github (opens in new tab)">
                        <img id="github" alt="Andy's Github" src="/icons/GitHub-Mark-32px.png" height="32" width="32">
                    </a>
                    <a href="https://www.facebook.com/andrew.stanish" target="_blank" title="Andy's Facebook (opens in new tab)">
                        <img alt="Andy's Facebook" src="/icons/f_logo_RGB-Blue_1024.png" height="32" width="32">
                    </a>
                    <a href="https://twitter.com/andybp85" target="_blank" title="Andy's Twitter (opens in new tab)">
                        <img alt="Andy's Twitter" src="/icons/Twitter_Social_Icon_Rounded_Square_Color.png" height="32" width="32">
                    </a>
                    <a href="https://www.linkedin.com/in/andrewstanish/" target="_blank" title="Andy's LinkedIn (opens in new tab)">
                        <img alt="Andy's LinkedIn" src="/icons/In-Blue-34.png" height="32" width="32">
                    </a>
                </div>
                <div id="clicky">
                    <a title="Web Analytics (opens in new tab)" href="https://clicky.com/101459580" target="_blank">
                        <img alt="Clicky" src="/icons/click-badge.gif" height="15" width="80"></a>
                </div>
            </footer>`;
        const clicky = document.createElement("script");
        clicky.async = true;
        clicky.dataset.id = "101459580";
        clicky.src = "//static.getclicky.com/js";
        this.querySelector("#clicky").append(clicky);
    }
});
```

- [ ] **Step 2: Commit**

```bash
git add components.js
git commit -m "add zero-dependency web components for site chrome"
```

---

### Task 6: Global stylesheet (modern CSS, no Sass)

Translates `00-global` + `01-header` + `02-footer` + `03-light` + `_breakpoints` + `_code` + `_sub-nav` into one `styles.css`. Key changes from the Sass version:

- Breakpoint variables become literal range media queries (`width <= 30rem` for small, `width <= 55rem` for medium) — media queries can't read custom properties.
- `site-header`/`site-footer` get `display: contents` so the inner `<header>`/`<footer>` still participate in the body grid.
- Sub-nav styles target the `sub-nav` element (was `#subnav`), and the main-column override that the old `_sub-nav` partial applied per-page is now `body:has(sub-nav) main` — pure CSS, no per-page duplication.
- The `.current` underline no longer needs `!important` — the shorthand comes first, longhands after.
- The Pygments theme is NOT here — the builder writes it to `/pygments.css`, linked only by pages with code.

**Files:**
- Replace: `styles.css` (repo root — currently compiled Sass output)

- [ ] **Step 1: Replace `styles.css` with**

```css
@import url("/fonts/B612-Regular/B612.css");
@import url("/fonts/Inter/inter.css");
@import url("/fonts/Berkeley-Mono-Variable/Berkeley-Mono.css");

:root {
    --dark-red: darkred;
    --oasis-blue: rgb(46 184 255);
    --text-color: #f0f0f0;
}

body {
    color: var(--text-color);
    display: grid;
    font-family: InterVariable, sans-serif;
    font-optical-sizing: auto;
    gap: 2rem;
    grid-template-columns: repeat(4, 1fr);
    margin: 0 auto;
    max-width: 1024px;
    padding: 0 1rem;
    visibility: visible;

    & img {
        border-radius: 5px;
    }

    & main {
        grid-column: 1 / 5;

        & > p:first-child,
        & > h1:first-child,
        & > h2:first-child,
        & > h3:first-child,
        & > h4:first-child,
        & > h5:first-child,
        & > h6:first-child {
            margin-top: 0;
        }
    }
}

h1, h2, h3, h4, h5, h6 {
    font-family: B612-Regular, serif;
}

h1 {
    font-size: 3.157rem;
}

h2 {
    font-size: 2.369rem;
}

h3 {
    font-size: 1.777rem;
}

h4 {
    font-size: 1.333rem;
}

h5 {
    font-size: 1rem;
    font-weight: bold;
}

a {
    color: var(--oasis-blue);
    text-decoration: none;
}

blockquote {
    font-style: italic;
}

code {
    font-family: "Berkeley Mono Variable", monospace;
    font-weight: lighter;
}

pre {
    line-height: 125%;
    white-space: pre-wrap;
}

site-header,
site-footer {
    display: contents;
}

header {
    border-bottom: 1px solid var(--dark-red);
    display: grid;
    grid-column: 1 / 5;
    grid-template-columns: repeat(3, 1fr);

    & a {
        color: var(--text-color);
        text-decoration: none;
    }

    & h1 {
        grid-column: 1 / 3;
    }

    & nav {
        align-self: center;
        display: flex;
        font-family: B612-Regular, serif;
        font-size: 2rem;
        gap: 1rem;
        grid-column-end: 5;
        justify-content: end;

        & .current {
            text-decoration: underline;
            text-decoration-color: darkred;
            text-decoration-thickness: 3px;
            text-underline-offset: 10px;
        }
    }

    @media (width <= 30rem) {
        padding-bottom: 1em;

        & h1 {
            grid-column: 2;
            place-self: center;
            text-wrap: nowrap;
        }

        & nav {
            grid-column: 2;
            grid-row: 2;
            place-self: center;
        }
    }
}

footer {
    border-top: 1px solid var(--dark-red);
    display: grid;
    grid-column: 1 / 5;
    grid-template-columns: repeat(3, 1fr);
    padding: 2rem 0;
    row-gap: 1em;
}

#social-media-links {
    align-self: center;
    display: flex;
    gap: 1em;
    grid-column: 2;
    justify-content: center;

    & a {
        text-decoration: none;
    }
}

#clicky {
    place-self: end;

    @media (width <= 30rem) {
        grid-column: 2;
        grid-row: 2;
        place-self: center;
    }
}

#github {
    filter: invert(1);
}

sub-nav {
    display: block;
    grid-column: 4;
    grid-row: 2;

    & label {
        display: block;
        font-size: 1.5rem;
        line-height: 2rem;
        margin-bottom: 1rem;
    }

    & nav {
        text-indent: 1em hanging;
    }

    @media (width <= 55rem) {
        grid-column: 1 / 5;
        grid-row: 2;
    }
}

body:has(sub-nav) main {
    grid-column: 1 / 4;
    grid-row: 2;

    @media (width <= 55rem) {
        grid-column: 1 / 5;
        grid-row: 3;
    }
}

@media (prefers-color-scheme: light) {
    :root {
        --oasis-blue: rgb(0 120 180);
        --text-color: #444;
    }

    #github {
        filter: invert(0);
    }

    #pjhd-logo {
        filter: invert(1);
    }
}
```

- [ ] **Step 2: Commit**

```bash
git add styles.css
git commit -m "replace compiled sass with hand-written modern css"
```

---

### Task 7: Per-page stylesheets

Rewrites of the per-page Sass as plain CSS, in the locations the pages already link. The old per-page files compiled `@use 'sub-nav'` into themselves — that's now global, so these files only carry what's genuinely page-specific.

**Files:**
- Replace: `home.css`
- Replace: `about/about.css`
- Replace: `blog/blog.css` (now post-content styles, linked by generated post pages)
- Replace: `projects/projects.css` (now project-content styles, from the vim page's Sass)

- [ ] **Step 1: Replace `home.css` with**

```css
body main {
    display: grid;
    grid-template-columns: subgrid;
    grid-template-rows: 180px;
    justify-items: end;

    @media (width <= 55rem) {
        gap: 2rem;
        grid-template-columns: 1fr;
        grid-template-rows: auto;
    }
}

#about-me {
    font-size: 1.2rem;
    grid-column: 1 / 4;
    line-height: 1.6rem;

    @media (width <= 55rem) {
        grid-column: 1;
    }
}

#featured-projects {
    grid-column: 2;
    place-self: center;
    text-align: center;

    @media (width <= 55rem) {
        grid-column: 1;
        grid-row: 3;
    }

    & div {
        display: flex;
        gap: 1rem;
        justify-content: space-evenly;

        @media (width <= 30rem) {
            flex-direction: column-reverse;
        }
    }
}

#pic-of-me {
    @media (width <= 55rem) {
        display: flex;
        flex-wrap: wrap-reverse;
        grid-column: 1;
        grid-row: 2;
        justify-content: center;
        width: 100%;
    }
}
```

- [ ] **Step 2: Replace `about/about.css` with**

```css
body {
    gap: 1rem;

    & main {
        display: block;
    }
}
```

- [ ] **Step 3: Replace `blog/blog.css` with**

```css
main img {
    display: block;
    max-width: 100%;
}
```

- [ ] **Step 4: Replace `projects/projects.css` with**

```css
main div {
    width: 100%;

    & img {
        display: block;
        height: auto;
        margin: 0 auto;
        max-width: 100%;
    }
}
```

- [ ] **Step 5: Commit**

```bash
git add home.css about/about.css blog/blog.css projects/projects.css
git commit -m "rewrite per-page styles as plain modern css"
```

---

### Task 8: Convert the hand-written pages

Four pages become permanently hand-authored: `/index.html`, `/about/index.html`, `/projects/index.html`, `/projects/vim-config-with-YouCompleteMe/index.html`. Each gets the same mechanical edits; **the existing `<main>` content is kept byte-for-byte unless noted.**

**Files:**
- Modify: `index.html`
- Modify: `about/index.html`
- Modify: `projects/index.html`
- Modify: `projects/vim-config-with-YouCompleteMe/index.html`

- [ ] **Step 1: Apply the shared edits to all four pages**

In each file:

1. **CSP meta** — replace the `content` of the Content-Security-Policy meta with:
   ```
   default-src 'self'; script-src-elem 'self' 'unsafe-inline' *.getclicky.com; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src *.getclicky.com
   ```
   (adds `'self'` for `/components.js`, drops the livereload `localhost:5500` and `ws://localhost:5500` entries).
2. **Components script** — add as the last element inside `<head>`:
   ```html
   <script type="module" src="/components.js"></script>
   ```
3. **Header** — replace the entire `<header>…</header>` block with:
   ```html
   <site-header></site-header>
   ```
4. **Footer** — replace the entire `<footer>…</footer>` block (including the clicky script and noscript) with:
   ```html
   <site-footer></site-footer>
   ```

- [ ] **Step 2: Page-specific edits**

- `projects/index.html` and `projects/vim-config-with-YouCompleteMe/index.html`: replace the sub-nav wrapper — `<section id="subnav">` → `<sub-nav>` and its matching `</section>` → `</sub-nav>`, keeping the `<label>` and `<nav>` children. Rename any `--data-*` attributes on the links to valid `data-*` attributes.
- `projects/vim-config-with-YouCompleteMe/index.html`: replace the per-page stylesheet link (`vim-config-with-YouCompleteMe.css`) with:
  ```html
  <link rel="stylesheet" href="/projects/projects.css">
  <link rel="stylesheet" href="/pygments.css">
  ```
- `index.html` keeps its `/home.css` link; `about/index.html` keeps `/about/about.css`; `projects/index.html` keeps `/projects/projects.css`.
- Set each page's `<title>`: home stays `Andy Stanish`; the others become `About — Andy Stanish`, `Projects — Andy Stanish`, `Vim Config With YouCompleteMe — Andy Stanish`.

- [ ] **Step 3: Commit**

```bash
git add index.html about/index.html projects/index.html projects/vim-config-with-YouCompleteMe/index.html
git commit -m "convert static pages to web components"
```

---

### Task 9: Generate the blog and remove stale generated files

**Files:**
- Regenerate: `blog/index.html`, `blog/tips-for-waking-up-far-far-too-early/index.html`
- Create (generated): `pygments.css`
- Delete: `blog/tips-for-waking-up-far-far-too-early/tips-for-waking-up-far-far-too-early.css`

- [ ] **Step 1: Run the build**

Run: `(cd src && uv run build)`
Expected: prints `blog built`; `git status` shows `blog/index.html` and `blog/tips-for-waking-up-far-far-too-early/index.html` modified and `pygments.css` created.

- [ ] **Step 2: Verify the generated output**

Check `blog/index.html` contains `<site-header>`, `<sub-nav>`, and a post link with `data-date="2016-10-22"`; check the post page contains the post content and `<title>Tips For Waking Up Far Far Too Early — Andy Stanish</title>`.

- [ ] **Step 3: Remove the stale per-post stylesheet**

```bash
git rm blog/tips-for-waking-up-far-far-too-early/tips-for-waking-up-far-far-too-early.css
```

- [ ] **Step 4: Commit**

```bash
git add blog pygments.css
git commit -m "generate blog with new builder"
```

---

### Task 10: Delete the old build system

**Files to delete (tracked → `git rm`):**
- `src/build.py`, `src/test_build.py`, `src/__main__.py`, `src/__init__.py`
- `src/template.html`, `src/subnav_template.html`
- `src/setup.sh`, `src/requirements.txt`, `src/pytest.ini`
- `src/pages/` (entire tree — markdown already migrated; about/projects/home content lives in the hand-written HTML now)
- `src/sass-partials/`
- `_code.css`, `_sub-nav.css` (repo root — folded into `styles.css`)

**Untracked junk to remove:** `src/penv/`, `src/htmlcov/`, `src/.coverage`, `src/.pytest_cache/`, `src/__pycache__/`, `src/.DS_Store`

- [ ] **Step 1: Remove tracked files**

```bash
git rm -r src/build.py src/test_build.py src/__main__.py src/__init__.py \
    src/template.html src/subnav_template.html src/setup.sh src/requirements.txt \
    src/pytest.ini src/pages src/sass-partials _code.css _sub-nav.css
```

If any path errors as not tracked, remove it with plain `rm` instead and continue.

- [ ] **Step 2: Remove untracked junk**

```bash
rm -rf src/penv src/htmlcov src/.coverage src/.pytest_cache src/__pycache__ src/.DS_Store
```

- [ ] **Step 3: Verify nothing still references deleted files**

Run: `grep -rn "sass\|_code.css\|_sub-nav.css\|template.html\|livereload" --include="*.html" --include="*.css" --include="*.py" --include="*.js" . --exclude-dir=.git --exclude-dir=.venv --exclude-dir=docs --exclude-dir=penv`
Expected: no hits outside `src/post_template.html` / `src/blog_index_template.html` filenames themselves.

- [ ] **Step 4: Run the tests and the build to confirm nothing broke**

Run: `(cd src && uv run pytest && uv run build)`
Expected: 12 passed, `blog built`.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "remove old sass build system"
```

---

### Task 11: Root .gitignore

**Files:**
- Replace: `.gitignore` (repo root)

- [ ] **Step 1: Replace root `.gitignore` with**

```
.claude/
.coverage
.DS_Store
.idea
.memsearch/
.pytest_cache/
.venv/
__pycache__/
htmlcov/
```

- [ ] **Step 2: Untrack anything now ignored**

Run: `git status --short` — if `.claude/settings.local.json` or `.idea/` files show as tracked, run `git rm -r --cached .claude .idea` (ignore errors if untracked).

- [ ] **Step 3: Commit**

```bash
git add .gitignore
git commit -m "update gitignore"
```

---

### Task 12: Rewrite the README

**Files:**
- Replace: `README.md` — keep the existing **Code Style** section verbatim (minus the Sass-era bullet about side effects only if it no longer applies — it still does, keep it all), replace everything above it.

- [ ] **Step 1: Replace `README.md` content above the Code Style section with**

```markdown
# Andy's Site

Hand-written HTML with vanilla web components and modern CSS, plus a small
Python tool that builds the blog from Markdown. Zero JavaScript dependencies.

See it live at [www.andrewstanish.com](https://www.andrewstanish.com/)

## Getting Started

Install [uv](https://docs.astral.sh/uv/), then:

```shell
> cd src/
> uv run serve
```

This builds the blog and serves the site at [http://localhost:5500/](http://localhost:5500/),
rebuilding whenever a post or template changes (refresh the browser to see it).

To just build:

```shell
> cd src/
> uv run build
```

## How It Works

The repo root is the site, served as-is by GitHub Pages. The pages (home,
about, projects) are hand-written HTML. Shared chrome comes from three web
components in `components.js`:

- `<site-header>` — renders the masthead and main nav, and marks the current
  section from `location.pathname`.
- `<site-footer>` — renders the social links and analytics badge.
- `<sub-nav>` — never registered, just styled: its links are real light-DOM
  children written into each page, so they work without JavaScript.

All styling is plain modern CSS (custom properties, native nesting, `:has()`,
range media queries) — `styles.css` is global, plus a small per-page file
where a page needs its own layout.

### The Blog

Posts are Markdown files in `src/posts/`. Each needs a `date:` meta line
(`YYYY-MM-DD`, used for newest-first ordering) and may have a `categories:`
line (pipe-separated). The post's title comes from its filename:
`tips-for-waking-up.md` → "Tips For Waking Up".

`uv run build` renders each post into `/blog/<slug>/index.html` via
`src/post_template.html`, regenerates the post list in `/blog/index.html`
via `src/blog_index_template.html`, and writes the Pygments syntax
highlighting theme to `/pygments.css`. Code blocks are highlighted at build
time — no JavaScript in the browser.

### Tests

I practice TDD, mainly because it's faster and easier than constantly running
your code by hand. The tests (in `src/test/`) also serve as some of the
documentation.

```shell
> cd src/
> uv run pytest
```

Coverage:

```shell
> uv run pytest --cov=builder --cov-branch --cov-report=html
```

### Pre-Commit hook

`src/pre-commit` just runs the tests. Install it manually:

```shell
> cp src/pre-commit .git/hooks/ && chmod +x .git/hooks/pre-commit
```

## Deployment

The site is hosted on GitHub Pages: once it's good locally it's just a git
commit-push away from being live.
```

(The old "Dev Tools" section about ipython/ipdb goes away with the dependencies; the Code Style section stays.)

- [ ] **Step 2: Commit**

```bash
git add README.md
git commit -m "rewrite readme for web components architecture"
```

---

### Task 13: Final verification

- [ ] **Step 1: Full test suite**

Run: `(cd src && uv run pytest -v)`
Expected: 12 passed.

- [ ] **Step 2: Clean build from scratch**

Run: `(cd src && uv run build && git status --short)`
Expected: `blog built`; git status clean (build output is deterministic and already committed).

- [ ] **Step 3: Serve and spot-check every page**

Run `(cd src && uv run serve)` in the background, then fetch each page and check for the markers:

```bash
for p in / /about/ /blog/ /blog/tips-for-waking-up-far-far-too-early/ /projects/ /projects/vim-config-with-YouCompleteMe/; do
    curl -s "http://localhost:5500$p" | grep -c "site-header"
done
curl -s http://localhost:5500/components.js | head -1
curl -s http://localhost:5500/styles.css | head -1
curl -s http://localhost:5500/pygments.css | head -1
```

Expected: each page prints `1`; the three asset fetches return content (not 404 HTML).

Then verify visually in a real browser (dark and light schemes): header/nav/footer render, current nav item is underlined, sub-nav shows on blog and projects pages, the vim page's code blocks are highlighted, the home page grid matches the live site.

- [ ] **Step 4: Stop the server, final commit if anything moved**

```bash
git status --short
```

Expected: clean. If verification required fixes, commit them with a terse message.

---

## Self-Review Notes

- **Spec coverage:** site structure (Tasks 8–9), web components (Task 5), CSS (Tasks 6–7), Python builder + uv (Tasks 1–4), cleanup + gitignore + README (Tasks 10–12), testing (Tasks 2–4, 13). Pygments CSS generated at build time (Task 3/9). Pre-commit hook replacement (Task 1).
- **Known behavior changes (accepted in spec):** header/footer require JS; noscript Clicky pixel dropped; post pages get descriptive `<title>`s; livereload replaced by manual refresh.
- **Type consistency:** post dicts use keys `categories|content|date|slug|title` everywhere; `build_all` kwargs match the `site` fixture keys; `SRC_PATH` imported by `serve.py` from `build.py`.
