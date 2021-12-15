from invoke import Collection

from . import api, console, quality, spec

ns = Collection(spec, api, console, quality)
