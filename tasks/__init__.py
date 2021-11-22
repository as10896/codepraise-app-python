from invoke import Collection

from . import spec
from . import quality
from . import api
from . import console


ns = Collection(spec.spec, quality, api, console.console)
