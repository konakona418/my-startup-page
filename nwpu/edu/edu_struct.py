from pydantic import BaseModel, Field

from typing import List, Any, Optional

class EduNotificationRequest(BaseModel):
    """
    GET
    https://jwxt.nwpu.edu.cn/student/my-notification/get-notifications
    """
    pass

class EduNotificationData(BaseModel):
    id: int
    person_assoc: int = Field(alias='personAssoc')
    item: str
    type: str
    content: str
    perm_code: str = Field(alias='permCode')
    create_date_time: str = Field(alias='createDateTime')
    read: bool
    info_url: str = Field(alias='infoUrl')
    alert: bool
    effective: bool


class EduNotificationPage(BaseModel):
    current_page: int = Field(alias='currentPage')
    rows_in_page: int = Field(alias='rowsInPage')
    rows_per_page: int = Field(alias='rowsPerPage')
    total_rows: int = Field(alias='totalRows')
    total_pages: int = Field(alias='totalPages')


class NotificationCount(BaseModel):
    notification_count: int = Field(alias='notificationCount')
    no_read_count: int = Field(alias='noReadCount')
    read_count: int = Field(alias='readCount')


class EduNotificationSort(BaseModel):
    field: str
    type: str
    type_string: str = Field(alias='typeString')


class EduNotificationResponse(BaseModel):
    parent_url: str = Field(alias='parentrUrl')
    student_url: str = Field(alias='studentUrl')
    teacher_url: str = Field(alias='teacherUrl')
    data: List[EduNotificationData] | Any = Field(default=None)
    page: EduNotificationPage = Field(alias='_page_')
    notification_count: NotificationCount = Field(alias='notificationCount')
    sorts: List[EduNotificationSort] = Field(alias='_sorts_')
    manager_url: str = Field(alias='managerUrl')

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True