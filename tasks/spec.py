from invoke import task


@task(default=True)
def spec(c):
    """
    Run tests
    """
    c.run(
        f"pytest -s -v spec/*_spec.py",
        pty=True,
    )
