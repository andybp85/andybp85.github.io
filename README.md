# Andy's Site
A simple custom build system in a proper tooling language: Python!

## Getting Started
The whole thing is a module and I made a setup script, so this is stupid easy:
```shell
> sh setup.sh
> source src/pyenv/bin/activate
> python .
```

This loads up [LiveReload](https://livereload.readthedocs.io/en/stable/),
makes you a nice [virtualenv](https://docs.python.org/3/library/venv.html#how-venvs-work) in `src/pyenv`,
and serves the site at [http://localhost:5500/](http://localhost:5500/)

## How It Works
First it compiles the Sass in `src/sass` and jams it all in `/main.css`.

Then it grabs any non-README markdown file it sees in the top-level dirs and uses `src/template.html` to build an
`index.html` file in the same dir by dumping the markdown contents into the `<main>` section of the template, and
updating the class on the nav to underline it.

Since this is a simple site, that's literally it for the build process, and once it's good locally it's just a
git commit-push away from being live.

### Tests
Run all from `src/`

```shell
> pytest
```
Watch:
```shell
> ptw
```

Coverage:
```shell
> pytest --cov=src --cov-branch --cov-report=html
```
HTML report is in `src/htmlcov`

### Development
Ipython and ipdb! Just put this anywhere to breakpoint:
```python
import ipdb; ipdb.set_trace()
```

## Why?
Go read the [site](https://www.andrewstanish.com/about) :)
