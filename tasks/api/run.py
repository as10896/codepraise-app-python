from invoke import task


@task(
    default=True,
    help={
        "mode": "Deployment mode for running API server. ['test'|'development'|'production'] [default: 'development']",
        "reload": "Restart your app when a file changes. This consumes much more resources and is more unstable. It helps a lot during development, but you shouldn't use it in production. [default: False]",
        "port": "Bind socket to this port. [default: 3000]",
        "host": "Bind socket to this host. [default: 127.0.0.1]",
    },
)
def run(c, mode="development", reload=False, port=3000, host="127.0.0.1"):
    """
    Run fastapi server with specified settings
    """
    cmd = f"ENV={mode} uvicorn app.application.controllers.app:app"

    if reload:
        cmd = f"{cmd} --reload"

    c.run(
        f"{cmd} --host {host} --port {port}",
        pty=True,
    )


@task(
    help={
        "port": "Bind socket to this port. [default: 3000]",
        "host": "Bind socket to this host. [default: 127.0.0.1]",
    }
)
def dev(c, port=3000, host="127.0.0.1"):
    """
    Rerun fastapi server in development environment
    """
    c.run(
        f"ENV=development uvicorn app.application.controllers.app:app --reload --host {host} --port {port}",
        pty=True,
    )


@task(help={"port": "Bind socket to this port. [default: 3030]"})
def test(c, port=3030):
    """
    Run fastapi server in test environment
    """
    c.run(
        f"ENV=test uvicorn app.application.controllers.app:app --port {port}",
        pty=True,
    )


@task(
    help={
        "port": "Bind socket, to this port. [default: 3000]",
        "host": "Bind socket to this host. [default: 0.0.0.0]",
        "workers": "The number of worker processes for handling requests. [default: 4]",
    }
)
def prod(c, port=3000, host="0.0.0.0", workers=4):
    """
    Run fastapi server in production environment
    """
    c.run(
        f"gunicorn app.application.controllers.app:app --workers {workers} --worker-class uvicorn.workers.UvicornWorker --env ENV=production --bind {host}:{port}",
        pty=True,
    )
