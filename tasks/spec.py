from invoke import task


@task(default=True)
def spec(c):
    """
    Run tests (need to `inv api.run.test` in another process, and make sure you've started the API server and the background worker in test mode)
    """
    c.run(
        f"pytest -s -v spec/*_spec.py",
        pty=True,
    )
