from importlib import import_module
from typing import TYPE_CHECKING, Any, Dict, Text

if TYPE_CHECKING:
    from . import v3 as v3
    from .access import Access
    from .ai_admin import AI
    from .app import App
    from .biconnector import Biconnector
    from .bizproc import Bizproc
    from .booking import Booking
    from .calendar import Calendar
    from .catalog import Catalog
    from .crm import CRM
    from .department import Department
    from .disk import Disk
    from .documentgenerator import Documentgenerator
    from .entity import Entity
    from .event import Event
    from .events import Events
    from .feature import Feature
    from .im import Im
    from .imbot import Imbot
    from .imconnector import Imconnector
    from .imopenlines import Imopenlines
    from .landing import Landing
    from .lists import Lists
    from .mailservice import Mailservice
    from .messageservice import Messageservice
    from .method import Method
    from .placement import Placement
    from .profile import Profile
    from .pull import Pull
    from .rpa import Rpa
    from .sale import Sale
    from .salescenter import Salescenter
    from .scope import Scope
    from .server import Server
    from .sign import Sign
    from .socialnetwork import Socialnetwork
    from .sonet_group import SonetGroup
    from .task import Task
    from .tasks import Tasks
    from .telephony import Telephony
    from .timeman import Timeman
    from .user import User
    from .userconsent import Userconsent
    from .userfieldconfig import Userfieldconfig
    from .userfieldtype import Userfieldtype
    from .vote import Vote
    from .voximplant import Voximplant

__all__ = [
    "AI",
    "CRM",
    "Access",
    "App",
    "Biconnector",
    "Bizproc",
    "Booking",
    "Calendar",
    "Catalog",
    "Department",
    "Disk",
    "Documentgenerator",
    "Entity",
    "Event",
    "Events",
    "Feature",
    "Im",
    "Imbot",
    "Imconnector",
    "Imopenlines",
    "Landing",
    "Lists",
    "Mailservice",
    "Messageservice",
    "Method",
    "Placement",
    "Profile",
    "Pull",
    "Rpa",
    "Sale",
    "Salescenter",
    "Scope",
    "Server",
    "Sign",
    "Socialnetwork",
    "SonetGroup",
    "Task",
    "Tasks",
    "Telephony",
    "Timeman",
    "User",
    "Userconsent",
    "Userfieldconfig",
    "Userfieldtype",
    "Vote",
    "Voximplant",
    "v3",
]

_SCOPE_MODULES: Dict[Text, Text] = {
    "Access": ".access",
    "AI": ".ai_admin",
    "App": ".app",
    "Biconnector": ".biconnector",
    "Bizproc": ".bizproc",
    "Booking": ".booking",
    "Calendar": ".calendar",
    "Catalog": ".catalog",
    "CRM": ".crm",
    "Department": ".department",
    "Disk": ".disk",
    "Documentgenerator": ".documentgenerator",
    "Entity": ".entity",
    "Event": ".event",
    "Events": ".events",
    "Feature": ".feature",
    "Im": ".im",
    "Imbot": ".imbot",
    "Imconnector": ".imconnector",
    "Imopenlines": ".imopenlines",
    "Landing": ".landing",
    "Lists": ".lists",
    "Mailservice": ".mailservice",
    "Messageservice": ".messageservice",
    "Method": ".method",
    "Placement": ".placement",
    "Profile": ".profile",
    "Pull": ".pull",
    "Rpa": ".rpa",
    "Sale": ".sale",
    "Salescenter": ".salescenter",
    "Scope": ".scope",
    "Server": ".server",
    "Sign": ".sign",
    "Socialnetwork": ".socialnetwork",
    "SonetGroup": ".sonet_group",
    "Task": ".task",
    "Tasks": ".tasks",
    "Telephony": ".telephony",
    "Timeman": ".timeman",
    "User": ".user",
    "Userconsent": ".userconsent",
    "Userfieldconfig": ".userfieldconfig",
    "Userfieldtype": ".userfieldtype",
    "Vote": ".vote",
    "Voximplant": ".voximplant",
    "v3": ".v3",
}


def __getattr__(name: Text) -> Any:
    try:
        module_path = _SCOPE_MODULES[name]
    except KeyError:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}") from None

    module = import_module(module_path, __name__)

    if name == "v3":
        value = module
    else:
        value = getattr(module, name)

    globals()[name] = value

    return value
