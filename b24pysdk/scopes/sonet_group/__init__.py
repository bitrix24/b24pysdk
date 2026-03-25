from functools import cached_property
from typing import Iterable, Literal, Optional, Text, Union

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
            description: Optional[Text] = None,
            visible: Optional[Union[bool, B24BoolStrict]] = None,
            opened: Optional[Union[bool, B24BoolStrict]] = None,
            closed: Optional[Union[bool, B24BoolStrict]] = None,
            keywords: Optional[Text] = None,
            initiate_perms: Optional[Literal["A", "E", "K"]] = None,
            project: Optional[Union[bool, B24BoolStrict]] = None,
            project_date_start: Optional[Text] = None,
            project_date_finish: Optional[Text] = None,
            scrum_master_id: Optional[int] = None,
            owner_id: Optional[int] = None,
            image: Optional[Iterable[Text]] = None,
            image_file_id: Optional[int] = None,
            site_id: Optional[Iterable[Text]] = None,
            subject_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "NAME": name,
        }

        if description is not None:
            params["DESCRIPTION"] = description

        if visible is not None:
            params["VISIBLE"] = B24BoolStrict(visible).to_b24()

        if opened is not None:
            params["OPENED"] = B24BoolStrict(opened).to_b24()

        if closed is not None:
            params["CLOSED"] = B24BoolStrict(closed).to_b24()

        if keywords is not None:
            params["KEYWORDS"] = keywords

        if initiate_perms is not None:
            params["INITIATE_PERMS"] = initiate_perms

        if project is not None:
            params["PROJECT"] = B24BoolStrict(project).to_b24()

        if project_date_start is not None:
            params["PROJECT_DATE_START"] = project_date_start

        if project_date_finish is not None:
            params["PROJECT_DATE_FINISH"] = project_date_finish

        if scrum_master_id is not None:
            params["SCRUM_MASTER_ID"] = scrum_master_id

        if owner_id is not None:
            params["OWNER_ID"] = owner_id

        if image is not None:
            if image.__class__ is not list:
                image = list(image)

            params["IMAGE"] = image

        if image_file_id is not None:
            params["IMAGE_FILE_ID"] = image_file_id

        if site_id is not None:
            if site_id.__class__ is not list:
                site_id = list(site_id)

            params["SITE_ID"] = site_id

        if subject_id is not None:
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
            order: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            is_admin: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if order is not None:
            params["ORDER"] = order

        if filter is not None:
            params["FILTER"] = filter

        if is_admin is not None:
            params["IS_ADMIN"] = B24BoolStrict(is_admin).to_b24()

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
