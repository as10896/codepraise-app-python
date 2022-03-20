# codepraise-app-python
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Web client for [codepraise-api-python](https://github.com/as10896/codepraise-api-python).

## Prerequisite
### Install Docker
Make sure you have the latest version of [Docker 🐳](https://www.docker.com/get-started) installed on your local machine.

### Set up session secret for cookie-based session management
Put your session secret key under `config/secrets/<env>/SESSION_SECRET`.

Or just set the environment variable `SESSION_SECRET`:
```shell
export SESSION_SECRET=<your secret>
```

One way to generate a key is to use `openssl rand`
```shell
openssl rand -hex 32
```

## Run with Docker
You can start the app easily with Docker Compose.

Before starting, remember to run [API](https://github.com/as10896/codepraise-api-python#run-with-docker) in advance and make sure you have all the configurations set up as mentioned above.

### Development

Uvicorn (1 worker)
```shell
docker compose up -d  # run services in the background
docker compose run --rm console  # run application console
docker compose down  # shut down all the services
```
After starting, you can visit http://localhost:3000 to see the application's page.

### Production
Gunicorn + Uvicorn (4 workers)
```shell
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d  # run services in the background
docker compose -f docker-compose.yml -f docker-compose.prod.yml run --rm console  # run application console
docker compose -f docker-compose.yml -f docker-compose.prod.yml down  # shut down all the servicesvolumes
```
After starting, you can visit http://localhost:3000 to see the application's page.

### BDD Testing

Before testing, remember to run API under [test environment](https://github.com/as10896/codepraise-api-python#testing) in advance.

For users of Intel or AMD64 devices, you can run BDD testing as follows:
```shell
docker compose -f docker-compose.test.yml run --rm spec
```

If you're testing on ARM64 devices (e.g. Apple M1), use the following command instead:
```shell
docker compose -f docker-compose.test.yml run --rm spec-arm
```


## Invoke tasks
Here we use [invoke](https://docs.pyinvoke.org/) as our task management tool.

You can use the container's bash to test these commands.
```shell
docker compose run --rm bash
```

### Commands
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
