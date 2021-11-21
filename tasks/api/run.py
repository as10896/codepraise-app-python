from invoke import task


@task(
    default=True,
    help={
        "mode": "Deployment mode for running API server. ['test'|'development'|'production'] [default: 'development']",
        "reload": "Restart your app when a file changes. This consumes much more resources and is more unstable. It helps a lot during development, but you shouldn't use it in production. [default: False]",
        "port": "Bind socket to this port.  [default: 3000]",
    },
)
def run(c, mode="development", reload=False, port=3000):
    """
    run fastapi server with specified settings
    """
    if reload:
        c.run(
            f"ENV={mode} uvicorn application.app:app --reload --port {port}", pty=True
        )
    else:
        c.run(f"ENV={mode} uvicorn application.app:app --port {port}", pty=True)


@task(help={"port": "Bind socket to this port.  [default: 3000]"})
def dev(c, port=3000):
    """
    rerun fastapi server in development environment
    """
    c.run(
        f"ENV=development uvicorn application.app:app --reload --port {port}", pty=True
    )


@task(help={"port": "Bind socket to this port.  [default: 3030]"})
def test(c, port=3030):
    """
    run fastapi server in test environment
    """
    c.run(f"ENV=test uvicorn application.app:app --port {port}", pty=True)
