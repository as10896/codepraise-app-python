# codepraise-app-python
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Web client for [codepraise-api-python](https://github.com/as10896/codepraise-api-python).

## Prerequisite
### Create virtual environment
Here we use [Pipenv](https://pipenv.pypa.io/en/latest/) to create our virtual environment.

```bash
pip install pipenv  # install pipenv
pipenv --python 3.9  # create Python 3.9 virtualenv under current directory
pipenv shell  # activate the virtualenv of the current directory
pipenv install --dev  # install required dependencies with Pipfile
```

## Usage
Here we use [invoke](https://docs.pyinvoke.org/) as our task management tool.

```bash
inv -l  # show all tasks
inv [task] -h  # show task help message
inv console  # run console
inv spec  # run all test scripts
inv api.run -m [mode] -p [port]  # run FastAPI server with specified settings (add `-r` or `--reload` to use auto-reload)
inv api.run.dev -p [port]  # rerun FastAPI server in development environment
inv api.run.test -p [port]  # run FastAPI server in test environment
inv quality.style  # examine coding style with flake8
inv quality.metric  # measure code metric with radon
inv quality.all  # run all quality tasks (style + metric)
inv quality.reformat  # reformat your code using the black code style
inv quality.typecheck  # check type with mypy
inv quality  # same as `inv quality.all`
inv rmvcr  # delete cassette fixtures (test stubs generated with vcrpy)
```
