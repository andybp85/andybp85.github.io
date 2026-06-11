# Sub-nav Restyle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restyle the `<sub-nav>` menus as a darkred ruled list with balanced title wrapping and a visible current-page marker.

**Architecture:** Pure-CSS restyle in the global `styles.css` (the `sub-nav` element block), plus a small TDD'd builder change so generated post pages mark their own sub-nav link with `class="current"`, a casing fix in the two hand-written sub-navs, and a gitignore entry. Spec: `docs/superpowers/specs/2026-06-11-subnav-restyle-design.md`.

**Tech Stack:** Modern CSS (native nesting, `text-wrap: balance`), Python 3 (uv-managed builder in `src/`, pytest).

**Context for workers:** Repo root is the served site (GitHub Pages). The builder lives in `src/` (`cd src && uv run pytest` / `uv run build`). A pre-commit hook runs the test suite — never use `--no-verify`. Current test count: 12; after Task 1 it is 14. Sub-navs appear on four pages: `blog/index.html` and `blog/<slug>/index.html` (generated), `projects/index.html` and `projects/vim-config-with-YouCompleteMe/index.html` (hand-written).

---

### Task 1: Builder marks the current post (TDD)

**Files:**
- Modify: `src/builder/build.py` (`_subnav` at lines 34-39, `build_all` at lines 46-71)
- Test: `src/test/test_build.py`

- [ ] **Step 1: Write the failing tests**

Append after `test__subnav_omits_empty_categories` (line 52) in `src/test/test_build.py`:

```python
def test__subnav_marks_only_the_current_slug():
    posts = [{'categories': '', 'content': '', 'date': '2020-01-01',
              'slug': 'b-post', 'title': 'B Post'},
             {'categories': '', 'content': '', 'date': '2016-10-22',
              'slug': 'a-post', 'title': 'A Post'}]
    assert build._subnav(posts, 'a-post') == (
        '<a href="/blog/b-post" data-date="2020-01-01">B Post</a>'
        '<a href="/blog/a-post" data-date="2016-10-22" class="current">A Post</a>')
```

And append at the end of the file:

```python
def test_build_all_marks_current_post_only_on_its_page(site):
    build.build_all(**site)
    assert 'class="current"' in (
        site['out_path'] / 'blog' / 'first-post' / 'index.html').read_text()
    assert 'class="current"' not in (site['out_path'] / 'blog' / 'index.html').read_text()
```

(No new test for the no-`current_slug` case: `test__subnav_makes_links_with_data_attrs` and `test__subnav_omits_empty_categories` already pin the unmarked output via the default argument.)

- [ ] **Step 2: Run the new tests to verify they fail**

Run: `(cd src && uv run pytest -v -k "current")`
Expected: 2 failures — `test__subnav_marks_only_the_current_slug` with `TypeError: _subnav() takes 1 positional argument but 2 were given`, `test_build_all_marks_current_post_only_on_its_page` with `AssertionError` (no `class="current"` in the post page).

- [ ] **Step 3: Implement**

In `src/builder/build.py`, replace `_subnav` (lines 34-39) with:

```python
def _subnav(posts: list[dict[str, str]], current_slug: str | None = None) -> str:
    return ''.join(
        f'<a href="/blog/{p["slug"]}" data-date="{p["date"]}"'
        + (f' data-categories="{p["categories"]}"' if p['categories'] else '')
        + (' class="current"' if p['slug'] == current_slug else '')
        + f'>{p["title"]}</a>'
        for p in posts)
```

In `build_all`, delete the line `subnav = _subnav(posts)` (line 58) and change the two `substitute` calls so each post page gets its own marked sub-nav and the index gets an unmarked one:

```python
    posts = _posts(posts_path)
    blog_path = Path(out_path, 'blog')
    blog_path.mkdir(parents=True, exist_ok=True)

    post_template = Template(Path(post_template_path).read_text())
    for post in posts:
        post_path = blog_path / post['slug'] / 'index.html'
        post_path.parent.mkdir(exist_ok=True)
        post_path.write_text(post_template.substitute(
            content=post['content'], subnav=_subnav(posts, post['slug']),
            title=post['title']))

    (blog_path / 'index.html').write_text(
        Template(Path(blog_index_template_path).read_text()).substitute(subnav=_subnav(posts)))
    Path(out_path, 'pygments.css').write_text(_pygments_css())
```

- [ ] **Step 4: Run the full suite to verify everything passes**

Run: `(cd src && uv run pytest -v)`
Expected: 14 passed.

- [ ] **Step 5: Commit**

```bash
git add src/builder/build.py src/test/test_build.py
git commit -m "mark current post in generated subnav"
```

---

### Task 2: Sub-nav CSS restyle

**Files:**
- Modify: `styles.css` (the `sub-nav` block, lines 175-195)

- [ ] **Step 1: Replace the `sub-nav` block**

In `styles.css`, the current block reads:

```css
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
```

Replace it with (the `& nav` rule becomes `& nav a`; everything else in the block is unchanged):

```css
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

    & nav a {
        border-top: 1px solid var(--dark-red);
        display: block;
        padding: 0.7rem 0;
        text-wrap: balance;

        &.current {
            color: var(--text-color);
            text-decoration: underline;
            text-decoration-color: darkred;
            text-decoration-thickness: 3px;
            text-underline-offset: 6px;
        }
    }

    @media (width <= 55rem) {
        grid-column: 1 / 5;
        grid-row: 2;
    }
}
```

Notes: every entry gets a top rule (one sits between the label and the first title — intended, per the approved mockup). `text-wrap: balance` makes multi-line titles break evenly. The `.current` treatment mirrors the header nav's underline with a 6px offset (header uses 10px on larger text). Light mode needs nothing: `var(--dark-red)` and `var(--text-color)` already adapt.

- [ ] **Step 2: Commit**

```bash
git add styles.css
git commit -m "restyle subnav as ruled list with current marker"
```

---

### Task 3: Fix sub-nav title casing on hand-written pages

**Files:**
- Modify: `projects/index.html`
- Modify: `projects/vim-config-with-YouCompleteMe/index.html`

- [ ] **Step 1: Correct the link text in both files**

In each file's `<sub-nav>` block, the link text reads `Vim Config With Youcompleteme` (bad casing inherited from the old slug-derived generation). Change the link TEXT to `Vim Config With YouCompleteMe`. Do not touch the `href` (the directory really is `vim-config-with-YouCompleteMe`) or any attributes.

- [ ] **Step 2: Verify no other casing instances remain**

Run: `grep -rn "Youcompleteme" --include="*.html" . --exclude-dir=.git`
Expected: no output.

- [ ] **Step 3: Commit**

```bash
git add projects/index.html projects/vim-config-with-YouCompleteMe/index.html
git commit -m "fix YouCompleteMe casing in subnav links"
```

---

### Task 4: Gitignore + regenerate the blog

**Files:**
- Modify: `.gitignore` (repo root)
- Regenerate: `blog/index.html`, `blog/tips-for-waking-up-far-far-too-early/index.html`

- [ ] **Step 1: Add `.superpowers/` to `.gitignore`**

Insert `.superpowers/` between `.pytest_cache/` and `.venv/` (the list is alphabetical):

```
.claude/
.coverage
.DS_Store
.idea
.memsearch/
.pytest_cache/
.superpowers/
.venv/
__pycache__/
htmlcov/
```

- [ ] **Step 2: Regenerate the blog**

Run: `(cd src && uv run build)`
Expected: `blog built`. Then `git status --short` shows ONLY `M .gitignore`, `M blog/tips-for-waking-up-far-far-too-early/index.html` (its sub-nav link gains `class="current"`), and nothing for `blog/index.html` (the index sub-nav is unchanged — no marker). `.superpowers/` must no longer appear as untracked.

- [ ] **Step 3: Verify the regenerated post page**

Run: `grep -c 'class="current"' blog/tips-for-waking-up-far-far-too-early/index.html`
Expected: `1`.

- [ ] **Step 4: Commit**

```bash
git add .gitignore blog
git commit -m "regenerate blog with current subnav marker; ignore .superpowers"
```

---

### Task 5: Final verification

- [ ] **Step 1: Full suite + idempotent build**

Run: `(cd src && uv run pytest && uv run build && git status --porcelain)`
Expected: 14 passed, `blog built`, empty status.

- [ ] **Step 2: Serve and spot-check the four sub-nav pages**

Start `(cd src && uv run serve)` in the background, then:

```bash
for p in /blog/ /blog/tips-for-waking-up-far-far-too-early/ /projects/ /projects/vim-config-with-YouCompleteMe/; do
    printf '%s ' "$p"; curl -s "http://localhost:5500$p" | grep -c "sub-nav"
done
curl -s http://localhost:5500/blog/tips-for-waking-up-far-far-too-early/ | grep -c 'class="current"'
curl -s http://localhost:5500/styles.css | grep -c "text-wrap: balance"
```

Expected: each page prints `2` (open + close tag), then `1`, then `1`. Stop the server afterward.

- [ ] **Step 3: Visual check (human)**

In a real browser (dark and light schemes): darkred rules between sub-nav entries on all four pages, long titles wrap balanced with no hanging indent, the vim page and the blog post page show the darkred-underlined body-color current link, and the medium-width layout (≤55rem) still stacks the sub-nav above main.

- [ ] **Step 4: Commit if anything moved**

Expected: nothing moved; working tree clean.
