# Invoke tasks
Here we use <a href="https://docs.pyinvoke.org/" target="_blank">Invoke</a> as our task management tool.

You can use the container's bash to test these commands.
```shell
docker compose run --rm bash
```

## Commands
```shell
inv -l  # show all tasks
inv [task] -h  # show task help message
inv console -e [env]  # run application console (ipython)
inv spec  # run BDD testing (need to run `inv api.run.test` in another process, and make sure the API server has been started)
inv api.run -e [env] -p [port]  # run FastAPI server with specified settings (add `-r` or `--reload` to use auto-reload)
inv api.run.dev -p [port]  # rerun FastAPI server in development environment
inv api.run.test -p [port]  # run FastAPI server in test environment
inv api.run.prod -p [port] -h [host] -w [workers]  # run FastAPI server in production environment (with gunicorn)
inv quality.style  # examine coding style with flake8
inv quality.metric  # measure code metric with radon
inv quality.all  # run all quality tasks (style + metric)
inv quality.reformat  # reformat your code using isort and the black coding style
inv quality.typecheck  # check type with mypy
inv quality  # same as `inv quality.all`
```
