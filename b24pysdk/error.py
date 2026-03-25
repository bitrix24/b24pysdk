import logging
import sys

from . import errors as _errors
from .errors import *  # noqa: F401, F403, RUF100
from .errors import oauth as _oauth
from .errors import v3

logging.getLogger(__name__).warning(
    "Module b24pysdk.error is deprecated, use b24pysdk.errors instead",
)

sys.modules[f"{__name__}.v3"] = v3
sys.modules[f"{__name__}.oauth"] = _oauth
__path__ = []

for _name in _oauth.__all__:
    globals()[_name] = getattr(_oauth, _name)

__all__ = [str(name) for name in [*_errors.__all__, *_oauth.__all__]]
