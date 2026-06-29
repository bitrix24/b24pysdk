from importlib import import_module
from typing import TYPE_CHECKING, Any, Dict, Text

if TYPE_CHECKING:
    from .documentation import Documentation
    from .humanresources import Humanresources
    from .mail import Mail
    from .main import Main
    from .rest import Rest
    from .tasks import Tasks

__all__ = [
    "Documentation",
    "Humanresources",
    "Mail",
    "Main",
    "Rest",
    "Tasks",
]

_SCOPE_MODULES: Dict[Text, Text] = {
    "Documentation": ".documentation",
    "Humanresources": ".humanresources",
    "Mail": ".mail",
    "Main": ".main",
    "Rest": ".rest",
    "Tasks": ".tasks",
}


def __getattr__(name: Text) -> Any:
    try:
        module_path = _SCOPE_MODULES[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None

    module = import_module(module_path, __name__)
    value = getattr(module, name)
    globals()[name] = value

    return value
