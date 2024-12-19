from enum import Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

# mail categories
class MailCategoryFlags(BaseModel):
    system: bool


class MailCategoryItemStats(BaseModel):
    message_count: int = Field(alias="messageCount")
    unread_message_count: int = Field(alias="unreadMessageCount")
    message_size: Optional[int] = Field(alias="messageSize", default=0)
    unread_message_size: Optional[int] = Field(alias="unreadMessageSize", default=0)

    class Config:
        populate_by_name = True


class MailCategoryItem(BaseModel):
    id: int
    name: str
    flags: MailCategoryFlags
    keep_period: Optional[int] = Field(alias="keepPeriod", default=0)
    stats: MailCategoryItemStats

    class Config:
        populate_by_name = True

class MailCategoryFormRequest(BaseModel):
    """
    https://mail.nwpu.edu.cn/coremail/XT5/jsp/mail.jsp?sid=<SID>&func=getAllFolders
    getAllFolders
    """
    stats: bool = True
    threads: bool = False


class MailCategoryResponse(BaseModel):
    code: Optional[str] = None
    categories: Optional[List[MailCategoryItem]] = Field(alias="var", default=None)
    error_msg: Optional[str] = Field(alias="errorMsg", default=None)
    error_code: Optional[str] = Field(alias="errorCode", default=None)

    class Config:
        populate_by_name = True


# inbox
class FilterFlags(BaseModel):
    pass


class Filter(BaseModel):
    pass


class EmailFlags(BaseModel):
    read: Optional[bool] = False
    archived: Optional[bool] = False


class MailListItem(BaseModel):
    id: str
    fid: int
    size: int
    from_: str = Field(alias="from")
    to: str
    subject: str
    sent_date: str = Field(alias="sentDate")
    received_date: str = Field(alias="receivedDate")
    modified_date: str = Field(alias="modifiedDate")
    priority: int
    background_color: int = Field(alias="backgroundColor")
    anti_virus_status: str = Field(alias="antiVirusStatus")
    label0: int
    flags: Optional[EmailFlags] = None
    hmid: str
    sender: str
    summary: Optional[str] = None

    class Config:
        populate_by_name = True


class MailListFID(int, Enum):
    inbox = 1
    draft = 2
    sent = 3


class MailListOrder:
    descending = True
    ascending = False

class MailListOrderFlag(str, Enum):
    receivedDate = "receivedDate"
    sender = "from"
    subject = "subject"
    size = "size"

class MailListRequest(BaseModel):
    """
    https://mail.nwpu.edu.cn/coremail/s/json?sid=<SID>&func=<func>
    mbox:listMessages
    """
    start: int = 0
    limit: int = 20
    mode: str = "count"
    sort_by: MailListOrderFlag = Field(alias="order", default=MailListOrderFlag.receivedDate)
    sort_order: bool = Field(alias="desc", default=MailListOrder.descending)
    return_total: bool = Field(alias="returnTotal", default=True)
    summary_window_size: int = Field(alias="summaryWindowSize", default=20)
    skip_locked_folders: bool = Field(alias="skipLockedFolders", default=False)
    fid: Optional[MailListFID] = MailListFID.inbox
    fids: Optional[List[int]] = None
    mboxa: str = ""
    top_first: bool = Field(alias="topFirst", default=True)
    filter: Filter = Filter()
    filter_flags: FilterFlags = Field(alias="filterFlags", default=FilterFlags())

    class Config:
        populate_by_name = True

class MailListResponse(BaseModel):
    code: str
    mid_offset: int = Field(alias="midoffset")
    total: Optional[int] = 0
    categories: Optional[List[MailListItem]] = Field(alias="var")

    class Config:
        populate_by_name = True


class UserAvatarRequest(BaseModel):
    """
    https://mail.nwpu.edu.cn/coremail/s/json?sid=<SID>&func=<func>&ts=<ts_mill>
    user:AgetHeadImageData
    """
    pass


class MailFlags(BaseModel):
    read: bool
    archived: bool
    attached: Optional[bool] = None


class MailAttachment(BaseModel):
    id: str
    filename: str
    content_type: str = Field(alias="contentType")
    content_length: int = Field(alias="contentLength")
    encoding: str
    content_offset: int = Field(alias="contentOffset")
    estimate_size: int = Field(alias="estimateSize")

    class Config:
        populate_by_name = True


class MailHeaders(BaseModel):
    From: str
    Content_Type: str = Field(alias="Content-Type")

    class Config:
        populate_by_name = True


class MainPartData(BaseModel):
    extended: bool
    content: str


class Mail(BaseModel):
    from_: List[str] = Field(alias="from")
    to: List[str]
    cc: List[str]
    bcc: List[str]
    request_read_receipt: bool = Field(alias="requestReadReceipt")
    is_manual_disposition: bool = Field(alias="isManualDisposition")
    subject: str
    headers: MailHeaders
    attachments: List[MailAttachment]
    inline_attachments: List[MailAttachment] = Field(alias="inlineAttachments")
    main_part_data: MainPartData = Field(alias="mainPartData")

    class Config:
        populate_by_name = True


class MailInfo(BaseModel):
    mail_id: str = Field(alias="id")
    fid: int
    size: int
    from_: str = Field(alias="from")
    to: str
    subject: str
    sent_date: str = Field(alias="sentDate")
    received_date: str = Field(alias="receivedDate")
    modified_date: str = Field(alias="modifiedDate")
    priority: int
    background_color: int = Field(alias="backgroundColor")
    anti_virus_status: str = Field(alias="antiVirusStatus")
    label0: int
    flags: MailFlags
    hmid: str
    sender: str

    class Config:
        populate_by_name = True


class ReadMailResponseBody(BaseModel):
    mail: Mail
    info: MailInfo = Field(alias="mailInfo")
    mail_cipher_encrypted: bool = Field(alias="mailCipherEncrypted")
    smime_pkcs7_enveloped: bool = Field(alias="smimePkcs7Enveloped")

    class Config:
        populate_by_name = True


class ReadMailResponse(BaseModel):
    code: str
    body: ReadMailResponseBody = Field(alias="var")

    class Config:
        populate_by_name = True


class ReadMailFormRequest(BaseModel):
    """
    POST
    https://mail.nwpu.edu.cn/coremail/XT5/jsp/readMessage.jsp
    """
    mid: str = Field(alias="mid")
    mboxa: str = ""
    part: str = ""
    mail_cipher_password: str = Field(alias="mailCipherPassword", default="")


    class Config:
        populate_by_name = True


class MailAttachmentRequest(BaseModel):
    """
    POST
    https://mail.nwpu.edu.cn/coremail/mbox-data?part=<attachment_id>&mid=<mail_id>&mode=download
    """
    pass


class AllMailContactGroupRequest(BaseModel):
    """
    POST
    https://mail.nwpu.edu.cn/coremail/s/json?sid=<sid>&func=<func>
    pab:getAllGroups
    """
    pass

class AllMailContactGroupItem(BaseModel):
    id: str
    name: str
    members: List[Any]
    reserved: bool
    rev: int

class AllMailContactGroupResponse(BaseModel):
    code: str
    contact_groups: List[AllMailContactGroupItem] = Field(alias="var")

    class Config:
        populate_by_name = True


class SearchContactFormRequest(BaseModel):
    """
    POST
    https://mail.nwpu.edu.cn/coremail/XT5/jsp/contact.jsp?sid=<sid>&func=<func>
    pab:search
    """
    group_id: str = Field(alias="groupid", default="")
    reload: bool = True
    limit: int = 20

    class Config:
        populate_by_name = True


class SearchContactItem(BaseModel):
    email_pref: str = Field(alias="EMAIL;PREF")
    contact_name: str = Field(alias="FN")
    groups: List[str]
    id: str
    rev: int

    class Config:
        populate_by_name = True


class SearchContactResponse(BaseModel):
    code: str
    grp_name: Any = Field(alias="grpName")
    list: List[SearchContactItem]
    total: int

    class Config:
        populate_by_name = True