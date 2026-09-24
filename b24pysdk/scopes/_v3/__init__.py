from importlib import import_module
from typing import TYPE_CHECKING, Any, Dict, Text

if TYPE_CHECKING:
    from .call import Call
    from .documentation import Documentation
    from .humanresources import Humanresources
    from .mail import Mail
    from .main import Main
    from .note import Note
    from .rest import Rest
    from .tasks import Tasks
    from .timeman import Timeman

__all__ = [
    "Call",
    "Documentation",
    "Humanresources",
    "Mail",
    "Main",
    "Note",
    "Rest",
    "Tasks",
    "Timeman",
]

_SCOPE_MODULES: Dict[Text, Text] = {
    "Call": ".call",
    "Documentation": ".documentation",
    "Humanresources": ".humanresources",
    "Mail": ".mail",
    "Main": ".main",
    "Note": ".note",
    "Rest": ".rest",
    "Tasks": ".tasks",
    "Timeman": ".timeman",
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
