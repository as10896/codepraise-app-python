from invoke import task


@task
def spec(c):
    """
    run tests
    """
    c.run(
        f"pytest -s -v spec/*_spec.py",
        pty=True,
    )
