import aiohttp
from aiohttp.streams import StreamReader

from nwpu.mail.mail_oa import extract_sid
from nwpu.mail.mail_struct import *
from nwpu.utils.common import DEFAULT_HEADER
from nwpu.utils.parse import StringArgsBuilder


class MailUrls:
    MAIL_CATEGORY = "https://mail.nwpu.edu.cn/coremail/XT5/jsp/mail.jsp"
    MAIL_LIST = "https://mail.nwpu.edu.cn/coremail/s/json"
    MAIL_USER_AVATAR = "https://mail.nwpu.edu.cn/coremail/s/json"
    MAIL_READ_MAIL = "https://mail.nwpu.edu.cn/coremail/XT5/jsp/readMessage.jsp"
    MAIL_GET_ALL_CONTACTS = "https://mail.nwpu.edu.cn/coremail/s/json"
    MAIL_SEARCH_CONTACT = "https://mail.nwpu.edu.cn/coremail/XT5/jsp/contact.jsp"


class MailRequest:
    """
    Mail request
    """

    session: aiohttp.ClientSession
    sid: str
    def __init__(self, session: aiohttp.ClientSession, sid: str = ""):
        self.session = session
        if sid == "":
            self.sid = extract_sid(session)
        else:
            self.sid = sid

    async def get_mail_category(self, request_form: MailCategoryFormRequest = MailCategoryFormRequest()) -> MailCategoryResponse:
        """
        Get mail category
        :return: MailCategoryResponse
        """
        form: dict = request_form.model_dump(by_alias=True)
        resp = await self.session.post(
            StringArgsBuilder(MailUrls.MAIL_CATEGORY)
                .add_param("sid", self.sid)
                .add_param("func", "getAllFolders")
                .build(),
            data=form,
            headers=DEFAULT_HEADER)

        return MailCategoryResponse(**await resp.json(content_type="text/x-json"))

    async def get_mail_list(self, request_json: MailListRequest) -> MailListResponse:
        """
        Get mail list
        :param request_json: MailListRequest
        :return: MailListResponse
        """
        json_data = request_json.model_dump(by_alias=True)
        resp = await self.session.post(
            StringArgsBuilder(MailUrls.MAIL_LIST)
                .add_param("sid", self.sid)
                .add_param("func", "mbox:listMessages")
                .build(),
            json=json_data,
            headers=DEFAULT_HEADER)
        return MailListResponse(**await resp.json(content_type="text/x-json"))


    async def get_user_avatar(self, request_json: UserAvatarRequest) -> StreamReader:
        """
        Get user avatar
        :param request_json: UserAvatarRequest
        :return: UserAvatarResponse
        """
        json_data = request_json.model_dump(by_alias=True)
        resp = await self.session.post(
            StringArgsBuilder(MailUrls.MAIL_USER_AVATAR)
                .add_param("sid", self.sid)
                .add_param("func", "user:AgetHeadImageData")
            .build(),
            json=json_data,
            headers=DEFAULT_HEADER
        )
        return resp.content

    async def read_mail(self, request_data: ReadMailFormRequest) -> ReadMailResponse:
        """
        Read mail
        :param request_data: ReadMailFormRequest
        :return: ReadMailResponse
        """
        data = request_data.model_dump(by_alias=True)
        print(data)
        resp = await self.session.post(
            StringArgsBuilder(MailUrls.MAIL_READ_MAIL)
                .add_params(**data)
                .build(),
            data=data,
            headers=DEFAULT_HEADER)
        return ReadMailResponse(**await resp.json(content_type="text/x-json"))

    async def get_all_contact_group(self) -> AllMailContactGroupResponse:
        """
        Get all contact group
        :return: AllMailContactGroupResponse
        """
        resp = await self.session.post(
            StringArgsBuilder(MailUrls.MAIL_GET_ALL_CONTACTS)
                .add_param("sid", self.sid)
                .add_param("func", "pab:getAllGroups")
                .build(),
            headers=DEFAULT_HEADER)
        return AllMailContactGroupResponse(**await resp.json(content_type="text/x-json"))

    async def search_contact(self, request_data: SearchContactFormRequest) -> SearchContactResponse:
        """
        Search contact
        :param request_data: SearchContactFormRequest
        :return: SearchContactResponse
        """
        form_data = request_data.model_dump(by_alias=True)
        resp = await self.session.post(
            StringArgsBuilder(MailUrls.MAIL_SEARCH_CONTACT)
                .add_param("sid", self.sid)
                .add_param("func", "pab:search")
                .build(),
            data=form_data,
            headers=DEFAULT_HEADER)
        return SearchContactResponse(**await resp.json(content_type="text/x-json"))