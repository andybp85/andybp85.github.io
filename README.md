# Andy's Site

A simple custom build system in a proper tooling language: Python!

See it live at [www.andrewstanish.com](https://www.andrewstanish.com/)

## Getting Started

First we need to install [dart-sass](https://sass-lang.com/documentation/cli/dart-sass/), since 
they can't be bothered maintaining wrapper libs anymore:
```shell
> brew install sass
```

`src/` is a module and I made a setup script, so this is stupid easy:

```shell
> cd src/
> sh setup.sh
> source src/penv/bin/activate
> python .
```

This makes you a nice [virtualenv](https://docs.python.org/3/library/venv.html#how-venvs-work)
in `src/penv`, loads up [LiveReload](https://livereload.readthedocs.io/en/stable/), and serves the
site at [http://localhost:5500/](http://localhost:5500/)

### Build All

```shell
> python -c "import build; build.build_all()"
```

This is also run first when you run the module to make sure the site is in a consistent state.

## How It Works

The site structure is defined in `src/pages`. Any top-level folder in here will become a path
in the nav, and any Markdown file in one of these folders (including `src/pages`) will become
and `index.html` for that path. It does this by dumping the contents of the Markdown into the
`main` tag of `src/template.html`. Multiple Markdown files in a folder are not handled.

### Subpages

Any Markdown files in sub dirs of `src/pages` will be built out and added to the hierarchy in the
sub nav on the right side of the page.

```
// TODO:

Deleting a Markdown file in a folder with no subfolders will delete the folder as
well, and remove it from the nav (if applicable).
```

### Styles

All Sass files starting with numbers in `src/pages` are top-level; they get compiled and
jammed in order in `/styles.css`, which is present in the template so is on every page. Any Sass
file with the same name as a Markdown file will be compiled and appended to the `index.html` in
the same dir.

### Tests

I practice TDD, mainly because it's faster and easier than constantly running your code by hand.
The tests (in `src/test_build.py`) also serve as some of the documentation.

Run all commands from `src/`.

```shell
> pytest
```

Watch:

```shell
> ptw --ext=sass,html,md,py -- -vv
```

Coverage:

```shell
> pytest --cov=src --cov-branch --cov-report=html
```

The HTML report is in `src/htmlcov`.

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
