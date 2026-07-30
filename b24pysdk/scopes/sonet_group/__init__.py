from functools import cached_property
from typing import Iterable, Literal, Optional, Text, Union

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import B24BoolStrict, JSONDict, Timeout
from .._base_scope import BaseScope
from .feature import Feature
from .user import User

__all__ = [
    "SonetGroup",
]


class SonetGroup(BaseScope):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "sonet_group"

    @cached_property
    def feature(self) -> Feature:
        """"""
        return Feature(self)

    @cached_property
    def user(self) -> User:
        """"""
        return User(self)

    @type_checker
    def create(  # noqa: C901, PLR0912
            self,
            name: Text,
            *,
            description: Optional[Text] = MISSING,
            visible: Optional[Union[bool, B24BoolStrict]] = MISSING,
            opened: Optional[Union[bool, B24BoolStrict]] = MISSING,
            closed: Optional[Union[bool, B24BoolStrict]] = MISSING,
            keywords: Optional[Text] = MISSING,
            initiate_perms: Optional[Literal["A", "E", "K"]] = MISSING,
            project: Optional[Union[bool, B24BoolStrict]] = MISSING,
            project_date_start: Optional[Text] = MISSING,
            project_date_finish: Optional[Text] = MISSING,
            scrum_master_id: Optional[int] = MISSING,
            owner_id: Optional[int] = MISSING,
            image: Optional[Iterable[Text]] = MISSING,
            image_file_id: Optional[int] = MISSING,
            site_id: Optional[Iterable[Text]] = MISSING,
            subject_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "NAME": name,
        }

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if visible is not MISSING:
            params["VISIBLE"] = B24BoolStrict(visible).to_b24()

        if opened is not MISSING:
            params["OPENED"] = B24BoolStrict(opened).to_b24()

        if closed is not MISSING:
            params["CLOSED"] = B24BoolStrict(closed).to_b24()

        if keywords is not MISSING:
            params["KEYWORDS"] = keywords

        if initiate_perms is not MISSING:
            params["INITIATE_PERMS"] = initiate_perms

        if project is not MISSING:
            params["PROJECT"] = B24BoolStrict(project).to_b24()

        if project_date_start is not MISSING:
            params["PROJECT_DATE_START"] = project_date_start

        if project_date_finish is not MISSING:
            params["PROJECT_DATE_FINISH"] = project_date_finish

        if scrum_master_id is not MISSING:
            params["SCRUM_MASTER_ID"] = scrum_master_id

        if owner_id is not MISSING:
            params["OWNER_ID"] = owner_id

        if image is not MISSING:
            if image.__class__ is not list:
                image = list(image)

            params["IMAGE"] = image

        if image_file_id is not MISSING:
            params["IMAGE_FILE_ID"] = image_file_id

        if site_id is not MISSING:
            if site_id.__class__ is not list:
                site_id = list(site_id)

            params["SITE_ID"] = site_id

        if subject_id is not MISSING:
            params["SUBJECT_ID"] = subject_id

        return self._make_bitrix_api_request(
            api_wrapper=self.create,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            group_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "GROUP_ID": group_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            order: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            is_admin: Optional[Union[bool, B24BoolStrict]] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if order is not MISSING:
            params["ORDER"] = order

        if filter is not MISSING:
            params["FILTER"] = filter

        if is_admin is not MISSING:
            params["IS_ADMIN"] = B24BoolStrict(is_admin).to_b24()

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def setowner(
            self,
            group_id: int,
            user_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "GROUP_ID": group_id,
            "USER_ID": user_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.setowner,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            group_id: int,
            name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "GROUP_ID": group_id,
            "NAME": name,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
