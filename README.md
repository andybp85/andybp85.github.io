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

This loads up [LiveReload](https://livereload.readthedocs.io/en/stable/),
makes you a nice [virtualenv](https://docs.python.org/3/library/venv.html#how-venvs-work) in `src/pyenv`,
and serves the site at [http://localhost:5500/](http://localhost:5500/)

## How It Works
First it compiles the Sass files and jams everything `/styles.css`. These go in alpha order, so I just prefixed a 
number to the ones that matter.

Then it grabs any non-README markdown file it sees in the top-level dirs and uses `src/template.html` to build an
`index.html` file in the same dir by dumping the markdown contents into the `<main>` section of the template.

There's a trick to the nav: the markdown file must match the text of the link, e.g. `Page.md` will update the link to
`Page`. It simply adds a class that underlines it.

Since this is a simple site, that's literally it for the build process, and once it's good locally it's just a
git commit-push away from being live.

### Tests
Run all from `src/`

```shell
> pytest
```
Watch:
```shell
> ptw -- -vv
```

Coverage:
```shell
> pytest --cov=src --cov-branch --cov-report=html
```
The HTML report is in `src/htmlcov`.

### Dev Tools
`ipython` and `ipdb`! Just put this anywhere to breakpoint:
```python
import ipdb; ipdb.set_trace()
```

#### Pre-Commit hook
```
/src/pre-commit
```
This get installed by `setup.sh`. It just runs the tests, since Python requires well formatted code to run! If you
modify it you'll have to move it into `.git/hooks` manually.

## Why?
Go read the [site](https://www.andrewstanish.com/about) :)
