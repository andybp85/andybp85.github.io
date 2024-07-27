# Andy's Site

A simple custom build system in a proper tooling language: Python!

## Getting Started

`src/` is a module and I made a setup script, so this is stupid easy:

```shell
> cd src/
> sh setup.sh
> source src/pyenv/bin/activate
> python .
```

This makes you a nice [virtualenv](https://docs.python.org/3/library/venv.html#how-venvs-work)
in `src/pyenv`, loads up [LiveReload](https://livereload.readthedocs.io/en/stable/), and serves
the site at [http://localhost:5500/](http://localhost:5500/)

## How to Read the Code

Like any good software, this is covered by extensive unit tests. Check out `src/test_build.py`
to see what's going on.

### Code Style

For me, brevity is readability. Here's some of my preferences:

- Indents are four spaces.
    - There should be a small but accumulative penalty for indenting. Ask
      [Linus Torvalds](https://www.kernel.org/doc/html/v4.10/process/coding-style.html#indentation)
      about this.
- 100 character line width.
    - This fits nicely in my editor with multiple panes (and my 14" MBP is set to 2048x1330).
- Max 250 lines in a source (non-test) file.
    - It's way easier to have separate files in panes than to have to scroll or keep track of 
      multiple panes with the same file.
- Prefer double-quoted strings, for consistency between langs.
    - If strings contain double quotes, it's okay to single-quote them for readability.
- Function should have Max 20 lines & 15 cognitive complexity.
- Functions take and return the most primitive type possible.
    - Help ensure an easy-to-grok interface.
- Functions have action names, verbs are nouns, and make sure to pluralize correctly.
- Functions do what the name says, and that's it.
    - If you feel dumb typing the name of a function, it probably shouldn't be one.
- Functions starting with `_` are private to the module.
    - Everything else gets unit tests.
- Everything should be alphabetically ordered wherever possible
- Side effects (in this case writing to files) are localized to one function per kind.
    - This makes for easier testing.
- Prefer functions over OOP.
    - I need to write a blog post about this at some point, but basically if you're not actually
      modeling the interaction of objects, OOP isn't the best abstraction.

(This is a bit of a rant, for [why](https://www.andrewstanish.com/about#about-site) go read the site :)

## How It Works

The site structure is defined in `src/pages`. Any top-level folder in here will become a path
in the nav, and any markdown file in one of these folders will become and `index.html` for that
path. It does this by dumping the contents of the markdown into the `main` tag of
`src/template.html`.

### Subpages

Any pages in sub dirs of `src/pages` will be built out and added to the hierarchy in the sub nav
on the right side of the page.

`// TODO: more`

### Styles

First it compiles the Sass files starting with numbers in `src/pages` and jams everything in
order in `/styles.css`. Any Sass file in a sub dir will be compiled and appended to the specific
page, as well as all subpages.

### Tests

Run all from `src/`

```shell
> pytest
```

Watch:

```shell
> ptw -- -vv
```

(Although I'm just using the auto-run in Pycharm.)

Coverage:

```shell
> pytest --cov=src --cov-branch --cov-report=html
```

The HTML report is in `src/htmlcov`.

Build All:

```shell
python -c "import build; build.build_all()"
```

Convenience method to quickly build the whole site.

## Dev Tools

### `ipython`

Good god, I have no words for how awesome an environment this is to work with. I miss it every day
I do Javascript. Some of its killer features include amazing command completion, inspection, and
a built-in editor for executing scripts or long commands.

### `ipdb`

This is the `ipython` debugger, installed separately. Just put this anywhere to breakpoint:

[//]: # (@formatter:off)
```python
import ipdb; ipdb.set_trace()
```
[//]: # (@formatter:on)

### Pre-Commit hook

```
/src/pre-commit
```

This get installed by `setup.sh`. It just runs the tests, since Python requires well-formatted
code to run (although I'm using SonarLint in PyCharm for linting). Of course, if you modify it
you'll have to move it into `.git/hooks` manually.

## Deployment

Since this is a simple site, that's literally it for the build process, and since it's hosted on
GitHub Pages once it's good locally it's just a git commit-push away from being live.
