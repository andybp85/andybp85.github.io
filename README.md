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

## Code Style

Brevity is readability. Hence: Python. Here's some of my preferences:

- Indents are four spaces.
    - There should be a small but accumulative penalty for indenting. Ask
      [Linus Torvalds](https://www.kernel.org/doc/html/v4.10/process/coding-style.html#indentation)
      about this.
- 100 character line width.
    - This fits nicely in my editor with multiple panes (and my 14" MBP is set to 2048x1330).
    - Also, I tend to write long lines of Python, so this helps reel them in.
- Max 250 lines in a source (non-test) file.
    - It's way easier to have separate files in panes than to have to scroll or keep track of
      multiple panes with the same file.
- Variables should never be named `value` or `data`.
    - We know that already. What's the actual purpose of the thing?
- Functions have action names, verbs are nouns, and make sure to pluralize correctly.
    - Single-letter var names are okay in iteration contexts.
- Functions do what the name says, and that's it.
    - If you feel dumb typing the name of a function, it probably shouldn't be one.
- Function should have Max 20 lines & 10 cognitive complexity.
- Functions take and return the most primitive type possible.
    - Helps ensure an easy-to-grok interface.
- Functions starting with `_` are private to the module.
- Everything should be sorted alphabetically wherever possible
- Side effects (in this case writing to files) are localized to one function per kind.
    - This makes for easier testing.
- Prefer functions over OOP.
    - I need to write a blog post about this at some point, but basically if you're not actually
      modeling the interaction of objects, OOP isn't the best abstraction.
- All patching/spys/etc. are set up in the unit tests in which they're used.
    - Yes, this violates DRY. In this case, it's better for readability (especially for the next 
      guy) to not have to wonder what magic is happening somewhere else in the file to get the 
      test to pass. 

(This is a bit of a rant, for [why](https://www.andrewstanish.com/about#about-site) go read the
site :)
