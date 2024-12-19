from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

from nwpu.utils.common import BoolString

USER_EVENT_TZ_NAME = "GMT+8:00 - 中国标准时间"


class ECampusHasNewEmailRequest(BaseModel):
    """
    GET
    https://portal-service.nwpu.edu.cn/portalCenter/v2/personalData/getEmailDataNew
    """
    pass

class ECampusHasNewEmailData(BaseModel):
    new_email_amount: Optional[int | str] = Field(alias='newEmailAmount', default=0)
    garbage_email_amount: Optional[int | str] = Field(alias='barbageEmailAmount', default=0)
    mailbox_unread_url: Optional[str] = Field(alias='mailboxUnreadUrl', default='')
    app_url: str = Field(alias='appUrl')
    is_main_email: bool = Field(alias='isMainEmail')
    email: str = Field(alias='email')

    class Config:
        populate_by_name = True

class ECampusHasNewEmailResponse(BaseModel):
    code: int
    message: str | None = Field(default='')
    data: Optional[List[ECampusHasNewEmailData]] | None = Field(default=None)

    class Config:
        populate_by_name = True


class ECampusUserInfoRequest(BaseModel):
    """
    GET
    https://authx-service.nwpu.edu.cn/personal/api/v1/personal/me/user
    """
    pass

class ECampusUserInfoAttributes(BaseModel):
    organization_id: str = Field(alias="organizationId")
    identity_type_code: str = Field(alias="identityTypeCode")
    account_id: str = Field(alias="accountId")
    organization_name: str = Field(alias="organizationName")
    organization_code: str = Field(alias="organizationCode")
    image_url: str = Field(alias="imageUrl")
    identity_type_name: str = Field(alias="identityTypeName")
    identity_type_id: str = Field(alias="identityTypeId")
    user_name: Optional[str] = Field(alias="userName")
    user_id: str = Field(alias="userId")
    user_uid: str = Field(alias="userUid")

    class Config:
        populate_by_name = True

class ECampusUserInfoData(BaseModel):
    username: str
    roles: List[str]
    attributes: Optional[ECampusUserInfoAttributes] = Field(default=None)

    class Config:
        populate_by_name = True

class ECampusUserInfoResponse(BaseModel):
    acknowledged: Optional[bool] = Field(alias="acknowleged", default=True)
    code: int
    message: Optional[str]
    data: Optional[ECampusUserInfoData] = Field(default=None)

    class Config:
        populate_by_name = True

class ECampusUserPortraitRequest(BaseModel):
    """
    GET
    https://authx-service.nwpu.edu.cn/personal/api/v1/me/portrait
    GET parameters
    """
    x_token: str = Field(alias='token')
    random_number: Optional[int | None] = Field(alias='random_number', default=None)

    class Config:
        populate_by_name = True


class ECampusUserPortraitResponse(BaseModel):
    """
    binary
    """
    pass

class ECampusUserInfoAccurateRequest(BaseModel):
    """
    GET
    https://authx-service.nwpu.edu.cn/personal/api/v1/personal/user/info
    """
    pass

class ECampusUserInfoAccurateUserStats(BaseModel):
    certificate_type_id: str = Field(alias='certificateTypeId')
    birthday: str
    country: Optional[str | Any] = Field(alias='country', default=None)
    address: Optional[str | Any] = Field(alias='address', default=None)
    gender: str
    nation: str
    gender_id: str = Field(alias='genderId')
    nation_id: str = Field(alias='nationId')
    country_id: Any = Field(alias='countryId')
    address_id: Any = Field(alias='addressId')
    all_address_info: Any = Field(alias='allAddressInfo')
    full_name_spelling: str = Field(alias='fullNameSpelling')
    uid: str
    phone_number: Any = Field(alias='phoneNumber')
    certificate_number: str = Field(alias='certificateNumber')
    password_state: int = Field(alias='passwordState')
    image_url: str = Field(alias='imageUrl')
    name: str
    id: str
    default_account_name: Optional[str | Any] = Field(alias='defaultAccountName', default=None)
    activation: int
    name_spelling: str = Field(alias='nameSpelling')
    email: Optional[str | Any] = Field(alias='email', default=None)
    certificate_type: str = Field(alias='certificateType')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserInfoAccurateAccount(BaseModel):
    identity_type_code: str = Field(alias='identityTypeCode')
    birthday: str
    account_locked: Optional[bool | str | int | Any] = Field(alias='accountLocked', default=None)
    organization_name: str = Field(alias='organizationName')
    community_organizations: List = Field(alias='communityOrganizations')
    account_name: str = Field(alias='accountName')
    identity_type_name: str = Field(alias='identityTypeName')
    account_expiry_date: Optional[str | Any] = Field(alias='accountExpiryDate', default=None)
    user_name: str = Field(alias='userName')
    is_data_center: int = Field(alias='isDataCenter')
    user_id: str = Field(alias='userId')
    part_time_organizations: Optional[List[Any]] = Field(alias='partTimeOrganizations')
    labels: Optional[List[Any]]
    organization_id: str = Field(alias='organizationId')
    organization_code: str = Field(alias='organizationCode')
    identity_type_id: str = Field(alias='identityTypeId')
    id: str
    state: str
    activation: int
    user_uid: str = Field(alias='userUid')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserInfoAccurateSecurity(BaseModel):
    security_level: int = Field(alias='securityLevel')
    mobile_bound: bool = Field(alias='mobileBinded')
    email_address_bound: bool = Field(alias='emailAddressBinded')
    question_bound: bool = Field(alias='questionBinded')
    mobile: str
    email_address: str = Field(alias='emailAddress')
    question1: Optional[str | Any] = Field(alias='question1')
    question2: Optional[str | Any] = Field(alias='question2')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserInfoAccurateData(BaseModel):
    user: Optional[ECampusUserInfoAccurateUserStats] = Field(default=None)
    accounts: Optional[List[ECampusUserInfoAccurateAccount]] = Field(default=None)
    user_security: Optional[ECampusUserInfoAccurateSecurity] = Field(alias='userSecurity', default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserInfoAccurateResponse(BaseModel):
    acknowledged: bool = Field(alias='acknowleged', default=True)
    code: int
    message: Optional[str] = Field(default='')
    data: Optional[ECampusUserInfoAccurateData] = Field(default=None)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ECampusUserPapersRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getPaper
    """
    pass

class ECampusUserPapersResponse(BaseModel):
    code: int = Field(alias='code', default=0)
    message: Optional[str] = Field(default='')
    data: Optional[Dict[str, Any]] | None = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ECampusUserCardRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getMyECard
    """
    
class ECampusUserCardExpenditure(BaseModel):
    time: str
    amount: str
    address: Optional[str] = ""
    pay_way: str = Field(alias="payWay")

    class Config:
        populate_by_name = True


class ECampusUserCardLastCas(BaseModel):
    time: Optional[str] = ""
    address: Optional[str] = ""

    class Config:
        populate_by_name = True


class ECampusUserCardData(BaseModel):
    last_expenditure: List[ECampusUserCardExpenditure | Any] | None = Field(alias="lastExpenditure", default=None)
    last_income: List = Field(alias="lastIncome")
    balance: str
    e_card_type: str = Field(alias="eCardType")
    card_status: str = Field(alias="cardStatus")
    open_date: Optional[str] = Field(alias="openDate", default="")
    month_balance: str = Field(alias="monthBalance")
    app_url: str = Field(alias="appUrl")
    pc_url: Optional[str] = Field(alias="pcUrl", default="")
    last_cas: Optional[ECampusUserCardLastCas] = Field(alias="lastCas", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserCardResponse(BaseModel):
    code: int
    message: Optional[str]
    data: Optional[ECampusUserCardData] = Field(default=None)

    class Config:
        populate_by_name = True


class ECampusUserConsumptionHistoryType(str, Enum):
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class ECampusUserConsumptionHistoryRequest(BaseModel):
    """
    GET
    https://portal-service.nwpu.edu.cn/portalCenter/api/rest/center/personalData/getMyCost
    GET params
    """
    time_range: ECampusUserConsumptionHistoryType | str = Field(alias='timeRange', default=ECampusUserConsumptionHistoryType.day.value)
    begin_time: date = Field(alias='beginTime', default=date.today())
    end_time: date = Field(alias='endTime', default=date.today())
    page_size: int = Field(alias='pageSize', default=10)
    page_index: int = Field(alias='pageIndex', default=0)
    random_number: int = Field(alias='random_number', default=0)

    def model_dump(self, **kwargs) -> dict[str, Any]:
        kwargs['by_alias'] = True
        dumped = super().model_dump(**kwargs)

        dumped['beginTime'] = dumped['beginTime'].strftime("%Y-%m-%d")
        dumped['endTime'] = dumped['endTime'].strftime("%Y-%m-%d")
        dumped['timeRange'] = dumped['timeRange'].value \
            if isinstance(dumped['timeRange'], ECampusUserConsumptionHistoryType) \
            else dumped['timeRange']
        return dumped

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

        json_encoders = {
            date: lambda v: v.strftime("%Y-%m-%d"),
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
            ECampusUserConsumptionHistoryType: lambda v: v.value,
        }

        
class ECampusUserConsumptionListItem(BaseModel):
    balance: float = Field(alias='blance')
    operation_title: str = Field(alias='operationTitle')
    occurrence_time: str = Field(alias='occurrenceTime')
    payment: str
    operation_type: str = Field(alias='operationType')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserConsumptionHistoryDataInner(BaseModel):
    total_sum: int = Field(alias='totalSum')
    total_items: int = Field(alias='totalItems')
    cost_list: Optional[List[ECampusUserConsumptionListItem | Any]] | Any = Field(alias='costList', default=None)
    consume: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserConsumptionHistoryData(BaseModel):
    data: Optional[ECampusUserConsumptionHistoryDataInner] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserConsumptionHistoryResponse(BaseModel):
    code: int
    message: Optional[str] = Field(default='')
    data: Optional[ECampusUserConsumptionHistoryData] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserNetworkFeeRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getNetworkFeeInfo
    """
    pass


class ECampusUserNetworkFeeFlow(BaseModel):
    flow_month: str = Field(alias="flowMonth")
    flow_sum_bytes: str = Field(alias="flowSumBytes")
    flow_used_bytes: str = Field(alias="flowUsedBytes")

    class Config:
        populate_by_name = True


class ECampusUserNetworkFeeData(BaseModel):
    user_balance: str = Field(alias="userBalance")
    package_name: str = Field(alias="packageName")
    pc_url: str = Field(alias="pcUrl")
    app_url: str = Field(alias="appUrl")
    package_flow: str = Field(alias="packageFlow")
    residue_flow: str = Field(alias="residueFlow")
    account_balance: str = Field(alias="accountBalance")
    residue_balance: str = Field(alias="residueBalance")
    flow_list: List[ECampusUserNetworkFeeFlow | Any] | None = Field(alias="flowList", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserNetworkFeeResponse(BaseModel):
    code: int
    message: Optional[str] = None
    data: Optional[ECampusUserNetworkFeeData] = Field(default=None)

    class Config:
        populate_by_name = True


class ECampusUserBorrowBooksRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getMyBooks
    """
    pass


class ECampusUserBorrowBooksShouldRepayBook(BaseModel):
    should_repay_book_name: str = Field(alias="shouldRepayBookName")
    should_repay_book_date: str = Field(alias="shouldRepayBookDate")

    class Config:
        populate_by_name = True


class ECampusUserBorrowBooksData(BaseModel):
    book_id: Optional[str] = Field(None, alias="bookId")
    borrow_count: str = Field(alias="borrowCount")
    book_average: str = Field(alias="bookArrearage")
    book_past_due: str = Field(alias="bookPastDue")
    pc_url: str = Field(alias="pcUrl")
    app_url: str = Field(alias="appUrl")
    should_repay_list: List[ECampusUserBorrowBooksShouldRepayBook] | None = Field(alias="shouldRepayList", default=None)

    class Config:
        populate_by_name = True


class ECampusUserBorrowBooksResponse(BaseModel):
    code: int
    message: Optional[str]
    data: Optional[ECampusUserBorrowBooksData] = Field(default=None)

    class Config:
        populate_by_name = True


class ECampusUserPropertyRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v2/personalData/getPropertyInfo
    """
    pass

class ECampusUserPropertyData(BaseModel):
    property_sum: str = Field(alias="propertySum")
    property_sum_unit: str = Field(alias="propertySumUnit")
    property_amount: float = Field(alias="propertyAmount")
    property_amount_unit: str = Field(alias="propertyAmountUnit")
    pc_url: str = Field(alias="pcUrl")
    app_url: str = Field(alias="appUrl")
    property_info_list: List[dict | Any] | None = Field(alias="propertyInfoList", default=None)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserPropertyResponse(BaseModel):
    code: int
    message: Optional[str]
    data: Optional[ECampusUserPropertyData] | None = Field(default=None)
    
    class Config:
        populate_by_name = True

class ECampusUserEventsMode(str, Enum):
    date_view = "DateView"
    week_view = "WeekView"
    month_view = "MonthView"

class ECampusUserEventsRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/getEvents?
    GET params
    """

    start_date: date = Field(alias="startDate")
    end_date: date = Field(alias="endDate")
    mode: ECampusUserEventsMode = Field(alias="reqType", default=ECampusUserEventsMode.date_view)
    random_number: str | int | None = Field(alias="randomNumber", default=0)

    def model_dump(self, **kwargs) -> dict[str, Any]:
        kwargs['by_alias'] = True
        dumped = super().model_dump(**kwargs)

        dumped["startDate"] = dumped["startDate"].strftime("%Y-%m-%d")
        dumped["endDate"] = dumped["endDate"].strftime("%Y-%m-%d")
        dumped["reqType"] = ECampusUserEventsMode(dumped["reqType"]).value
        return dumped

    class Config:
        populate_by_name = True
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S"),
            date: lambda d: d.strftime("%Y-%m-%d"),
            ECampusUserEventsMode: lambda m: m.value,
        }

        

class ECampusUserEventsCalendarEntry(BaseModel):
    id: str
    calendar_id: Optional[str] = Field(None, alias="calendarId")
    title: str
    is_whole_day: str = Field(alias="isWholeDay")
    start_date: str = Field(alias="startDate")
    start_time: str = Field(alias="startTime")
    end_date: str = Field(alias="endDate")
    end_time: str = Field(alias="endTime")
    repeat_type: Optional[str] = Field(None, alias="repeatType")
    repeat_cycle_type: Optional[str] = Field(None, alias="repeatCycleType")
    repeat_cycle_space: Optional[str] = Field(None, alias="repeatCycleSpace")
    repeat_cycle_exp: Optional[str] = Field(None, alias="repeatCycleExp")
    repeat_end_type: Optional[str] = Field(None, alias="repeatEndType")
    repeat_end_date: Optional[str] = Field(None, alias="repeatEndDate")
    repeat_end_times: Optional[int] = Field(None, alias="repeatEndTimes")
    address: Optional[str]
    remark: Optional[str]
    create_user: Optional[str] = Field(None, alias="createUser")
    update_user: Optional[str] = Field(None, alias="updateUser")
    create_time: Optional[str] = Field(None, alias="createTime")
    update_time: Optional[str] = Field(None, alias="updateTime")
    start_date_str: str = Field(alias="startDateStr")
    end_date_str: str = Field(alias="endDateStr")
    repeat_end_date_str: Optional[str] = Field(None, alias="repeatEndDateStr")
    create_time_str: Optional[str] = Field(None, alias="createTimeStr")
    create_user_name: Optional[str] = Field(None, alias="createUserName")
    create_user_code: Optional[str] = Field(None, alias="createUserCode")
    update_user_code: Optional[str] = Field(None, alias="updateUserCode")
    timezone: str
    color: str
    cu_color: Optional[str] = Field(None, alias="cucolor")
    calendar_name: str = Field(alias="calendarName")
    remind_type: Optional[str] = Field(None, alias="remindType")
    schedule_date: Optional[str] = Field(None, alias="scheduleDate")
    schedule_date_id: Optional[str] = Field(None, alias="scheduleDateId")
    repeat_cycle_count: Optional[int] = Field(None, alias="repeatCycleCount")
    schedule_type: Optional[str] = Field(None, alias="scheduleType")
    terminal_type: Optional[str] = Field(None, alias="terminalType")
    remind_date: Optional[str] = Field(None, alias="remindDate")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserEventsScheduleDate(BaseModel):
    calendar_list: List[ECampusUserEventsCalendarEntry | Any] | None = Field(alias="calendarList", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserEventsData(BaseModel):
    schedule: Dict[str, ECampusUserEventsScheduleDate | Any] | None = Field(default=None)
    req_type: str = Field(alias="reqType")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserEventsResponse(BaseModel):
    code: int
    message: str
    data: Optional[ECampusUserEventsData] = Field(default=None)

    class Config:
        populate_by_name = True

class ECampusUserEventCalendarRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/getPersonlCalendar
    """
    pass

class ECampusUserEventCalendarItem(BaseModel):
    id: str
    name: str
    color: str
    create_time: str | Any = Field(alias='createTime', default=None)
    update_time: str | Any = Field(alias='updateTime', default=None)
    create_user_name: str = Field(alias='createUserName', default=None)
    depart: Any = Field(alias='depart', default=None)
    depart_name: Any = Field(alias='departName', default=None)
    is_subscribed: Any = Field(alias='isSubscribed', default=None)
    is_force_subscribed: Any = Field(alias='isForceSubscribed', default=None)
    create_user_id: Any = Field(alias='createUserId', default=None)
    update_user_entity: Any = Field(alias='updateUserEntity', default=None)
    remark: Any = Field(alias='remark', default=None)
    create_time_str: Any = Field(alias='createTimeStr', default=None)
    cu_color: Any = Field(alias='cucolor', default=None)
    department_name: Any = Field(alias='depaptmentName', default=None)
    create_user_code: str = Field(alias='createUserCode', default=None)
    update_user_code: Any = Field(alias='updateUserCode', default=None)
    display_status: str = Field(alias='displayStatus', default=None)
    subscription_status: Any = Field(alias='subscriptionStatus', default=None)
    department_ids: Any = Field(alias='departmentIds', default=None)
    role_ids: Any = Field(alias='roleIds', default=None)
    group_ids: Any = Field(alias='groupIds', default=None)
    calendar_type: int = Field(alias='calendarType', default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusUserEventCalendarResponse(BaseModel):
    code: int
    message: Optional[str] = Field(default=None)
    data: Optional[List[ECampusUserEventCalendarItem]] = Field(default=None)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ECampusUserEventRepeatType(str, Enum):
    no_repeat = "01"
    daily = "02"
    weekly = "03"
    workday = "04"
    weekend = "05"
    custom = "06"

class ECampusUserEventIsWholeDay(str, Enum):
    no = "0"
    yes = "1"

class ECampusUserEventCycleType(str, Enum):
    daily = "1"
    weekly = "2"
    monthly = "3"
    yearly = "4"

class ECampusUserEventRepeatEndType(str, Enum):
    no_end = "1"
    after_n_times = "2"
    on_date = "3"

class ECampusUserEventRemindType(str, Enum):
    no_remind = "0"
    when_begin = "1"
    five_minutes_ahead = "2"
    one_quarter_ahead = "3"
    half_hour_ahead = "4"
    one_hour_ahead = "5"
    one_day_ahead = "6"


class ECampusAddUserEventRequest(BaseModel):
    """
    POST
    https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/save
    POST json data
    """
    timezone: str = Field(alias='timezone', default=USER_EVENT_TZ_NAME)
    repeat_type: ECampusUserEventRepeatType = Field(alias='repeatType', default=ECampusUserEventRepeatType.no_repeat)
    is_whole_day: ECampusUserEventIsWholeDay = Field(alias='isWholeDay', default=ECampusUserEventIsWholeDay.no)
    address: str = Field(default="")

    # the description of the event
    remark: str = Field(default="")

    # note that this field should match 'repeat_type' (if the repeat_type.value == Literal['daily', 'weekly', 'monthly', 'yearly'])
    repeat_cycle_type: ECampusUserEventCycleType = Field(alias='repeatCycleType', default=ECampusUserEventCycleType.weekly)

    # maximum number of repetition cycles.
    # usually this param is available when repeat_type.value == Literal['custom']
    # for instance, when repeat_cycle_type is 'weekly', and this field is set to 12,
    # then the event will only be available for 12 weeks.
    repeat_cycle_count: str = Field(alias='repeatCycleCount', default="1")

    # this field should match 'repeat_end_type'
    # when the repeat_end_type.value == Literal['after_n_times'], this field should be a number->str, for instance, '12';
    # when the repeat_end_type.value == Literal['on_date'], this field should be a date(YYYY-mm-dd HH:MM:SS)->str, for instance, '2024-01-01 00:00:00';
    # when the repeat_end_type.value == Literal['no_end'], this field should be an empty string.
    repeat_end_params: str = Field(alias='repeatEndType', default="")
    repeat_end_type: ECampusUserEventRepeatEndType = Field(alias='repeatEndRadio', default=ECampusUserEventRepeatEndType.no_end)
    remind_type: ECampusUserEventRemindType = Field(alias='remindDate', default=ECampusUserEventRemindType.no_remind)

    start_date: datetime = Field(alias='startDate', default=datetime.now())
    end_date: datetime = Field(alias='endDate', default=datetime.now())

    # the name of the event
    title: str

    # unknown
    schedule_type: str = Field(alias='scheduleType', default="1")
    calendar_id: str = Field(alias='calendarId')

    def model_dump(self, **kwargs) -> dict:
        kwargs['by_alias'] = True
        dumped = super().model_dump(**kwargs)

        dumped['startDate'] = dumped['startDate'].strftime("%Y-%m-%d %H:%M:%S")
        dumped['endDate'] = dumped['endDate'].strftime("%Y-%m-%d %H:%M:%S")

        dumped['repeatType'] = dumped['repeatType'].value
        dumped['isWholeDay'] = dumped['isWholeDay'].value
        dumped['repeatCycleType'] = dumped['repeatCycleType'].value
        dumped['repeatEndType'] = dumped['repeatEndType']
        dumped['remindDate'] = dumped['remindDate'].value

        return dumped

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
            date: lambda v: v.strftime("%Y-%m-%d"),

            ECampusUserEventRepeatType: lambda v: v.value,
            ECampusUserEventIsWholeDay: lambda v: v.value,
            ECampusUserEventCycleType: lambda v: v.value,
            ECampusUserEventRepeatEndType: lambda v: v.value,
            ECampusUserEventRemindType: lambda v: v.value
        }

class ECampusAddUserEventResponse(BaseModel):
    code: int
    message: Optional[str] | Any = Field(default=None)
    data: Optional[str] | Any # the id of the event

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class ECampusDeleteUserEventType(int, Enum):
    remove_all = 1
    remove_after_date = 2
    remove_once = 3

class ECampusDeleteUserEventRequest(BaseModel):
    """
    POST
    https://ecampus.nwpu.edu.cn/portal-api/v1/calendar/share/schedule/deleteSchedule
    url params
    """
    schedule_id: str = Field(alias='scheduleId')
    schedule_date: date = Field(alias='scheduleDate')
    data_change_type: ECampusDeleteUserEventType = Field(alias='dataChangeType', default=ECampusDeleteUserEventType.remove_all)

    def model_dump(self, **kwargs) -> dict:
        kwargs['by_alias'] = True
        dumped = super().model_dump(**kwargs)

        dumped['scheduleDate'] = dumped['scheduleDate'].strftime("%Y-%m-%d")
        dumped['dataChangeType'] = dumped['dataChangeType'].value
        return dumped

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

        json_encoders = {
            date: lambda v: v.strftime("%Y-%m-%d"),
            ECampusDeleteUserEventType: lambda v: v.value
        }

class ECampusDeleteUserEventResponse(BaseModel):
    code: int
    message: Optional[str] | Any = Field(default=None)
    data: Optional[str] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusNewsFeedColumnListRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v1/cms/Column/getColumnList
    """
    pass

class ECampusNewsFeedColumn(BaseModel):
    id: str
    column_name: str = Field(alias='columnName')
    column_code: str = Field(alias='columnCode')
    p_id: Optional[str] = Field(alias='pId')
    column_url: Optional[str | Any] = Field(alias='columnUrl', default=None)
    flow_id: Optional[str] = Field(alias='flowId')
    sort: int
    create_time: Optional[str] = Field(alias='createTime')
    update_time: Optional[str] = Field(alias='updateTime')
    column_level: int = Field(alias='columnLevel')
    rss: Optional[bool]
    create_user_code: Optional[str] = Field(alias='createUserCode')
    update_user_code: Optional[str] = Field(alias='updateUserCode')
    public_access: Optional[str] = Field(alias='publicAccess')
    column_desc: Optional[str | Any] = Field(alias='columnDesc', default=None)
    release_address: Optional[str] = Field(alias='releaseAddress')
    link: Optional[str | Any] = Field(alias='link', default=None)
    zl_sort: Optional[str | Any] = Field(alias='zlSort', default=None)
    display_way: Optional[str | Any] = Field(alias='displayWay', default=None)
    view_departments: Optional[str | Any] = Field(alias='viewDepts', default=None)
    view_groups: Optional[str | Any] = Field(alias='viewGroups', default=None)
    view_roles: Optional[str | Any] = Field(alias='viewRoles', default=None)
    p_column_name: Optional[str | Any] = Field(alias='pcolumnName', default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusNewsFeedColumnListResponse(BaseModel):
    code: int
    message: Optional[str] = Field(default=None)
    data: Optional[List[ECampusNewsFeedColumn]] = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class ECampusNewsFeedContentRequest(BaseModel):
    """
    GET
    https://ecampus.nwpu.edu.cn/portal-api/v3/cms/content/getColumncontents?
    GET params
    """
    kw: str = Field(default='')
    column_id: str = Field(alias='columnId')
    page_number: int = Field(alias='pageNo', default=1)
    page_size: int = Field(alias='pageSize', default=30)
    load_content: str = Field(alias='loadContent', default=BoolString.false.value)
    load_picture_contents: str = Field(alias='loadPicContents', default=BoolString.false.value)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        

class ECampusNewsFeedContentItem(BaseModel):
    id: str
    column_id: str | Any = Field(alias='columnId')
    release_user: Optional[str | Any] = Field(alias='releaseUser', default=None)
    release_start_time: Optional[str | datetime | Any] = Field(alias='releaseStartTime', default=None)
    release_end_time: Optional[str | datetime | Any] = Field(alias='releaseEndTime', default=None)
    top_status: str | Any = Field(alias='topStatus')
    top_time: Optional[str] | Any = Field(alias='topTime')
    title: str | Any
    title_image: Optional[str] = Field(alias='titleImage')
    content: Optional[str | Any] = Field(alias='content', default=None)
    create_time: str | Any = Field(alias='createTime')
    update_time: str | Any = Field(alias='updateTime')
    release_dept_name: str | Any = Field(alias='releaseDeptName')
    read_count: int | Any = Field(alias='readCount')
    public_access: str | Any = Field(alias='publicAccess')
    content_desc: str | Any = Field(alias='contentDesc')
    force_read: Optional[str | Any] = Field(alias='forceRead', default=None)
    column_name: str | Any = Field(alias='columnName')
    file_link: Optional[str | Any] = Field(alias='fileLink', default=None)
    telephone: Optional[str | Any] = Field(alias='telephone')
    author: Optional[str | Any] = Field(alias='author')
    picture_author: Optional[str | Any] = Field(alias='pictureAuthor')
    review_people: Optional[str | Any] = Field(alias='reviewPeople')
    red_title: Optional[str | Any] = Field(alias='redTitle')
    number_title: Optional[str | Any] = Field(alias='numberTitle')
    title_file: Optional[str | Any] = Field(alias='titleFile')
    release_file_year: Optional[str | Any] = Field(alias='releaseFileYear')
    thumb_count: int | Any = Field(alias='thumbCount')
    release_status: str | Any = Field(alias='releaseStatus')
    review_status: Optional[str | Any] = Field(alias='reviewStatus')
    review_advice: Optional[str | Any] = Field(alias='reviewAdvice')
    top_continue: Optional[str | Any] = Field(alias='topContinue')
    template: Optional[str | Any] = Field(alias='template', default=None)
    process_instance_id: Any = Field(alias='processInstanceId')
    release_dept_code: str | Any = Field(alias='releaseDeptCode', default=None)
    ffid: Optional[str | Any]
    pv: Optional[str | Any]
    url: Optional[str | Any]
    inherit: str | Any = Field(alias='inherit', default=None)
    lk_dept: Optional[str | Any] = Field(alias='lkDept')
    lk_time: Optional[str | Any] = Field(alias='lkTime')
    create_user_code: Optional[str | Any] = Field(alias='createUserCode')
    release_user_code: Optional[str | Any] = Field(alias='releaseUserCode')
    old_id: Optional[str | Any] = Field(alias='oldId')
    top_end_time: Optional[str | Any] = Field(alias='topEndTime')
    form_title_image: Optional[str | Any] = Field(alias='formTitleImage')
    is_notice: Optional[str | Any] = Field(alias='isNotice')
    catalog_id: Optional[str | Any] = Field(alias='catalogId')
    catalog_name: Optional[str | Any] = Field(alias='catalogName')
    content_files: Optional[str | Any] = Field(alias='contentFiles')
    title_image_list: Optional[str | Any] = Field(alias='titleImageList')
    form_content_id: Optional[str | Any] = Field(alias='formContentId')
    collect: str | Any
    news_type: Optional[str | Any] = Field(alias='newsType')
    external_news_url: Optional[str | Any] = Field(alias='externalNewsUrl')
    release_area: Optional[str | Any] = Field(alias='releaseArea')
    thumb: Optional[str | Any]
    read: str | Any
    release: Optional[str | Any]
    view_groups: Optional[str | Any] = Field(alias='viewGroups')
    view_depts: Optional[str | Any] = Field(alias='viewDepts')
    view_roles: Optional[str | Any] = Field(alias='viewRoles')
    file_list: Optional[str | Any] = Field(alias='fileList')
    column_pid: Optional[str | Any] = Field(alias='columnPid')
    collect_time: Optional[str | Any] = Field(alias='collectTime')
    row_num: Optional[str | int | Any] = Field(alias='rownum_')


class ECampusNewsFeedContentData(BaseModel):
    all_contents: Optional[List[ECampusNewsFeedContentItem]] = Field(alias='allContents', default=None)
    count: int
    pic_contents: Optional[List] | Any = Field(alias='picContents', default=None)


class ECampusNewsFeedContentResponse(BaseModel):
    code: int
    message: Any
    data: Optional[ECampusNewsFeedContentData] = Field(default=None)
