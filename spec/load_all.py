import os
import sys

WORKDIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(WORKDIR)

from app.infrastructure import ApiGateway
from config import get_settings
