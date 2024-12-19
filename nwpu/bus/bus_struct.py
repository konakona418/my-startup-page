import datetime
from enum import Enum
from typing import List, Any, Optional

from pydantic import BaseModel, Field

class BusAppointmentStatusType(str, Enum):
    needs_verification = '待核验'

class BusUserAppointmentsRequest(BaseModel):
    """
    POST
    https://hq-bus.nwpu.edu.cn/api/GetMyAppointment
    form data
    """
    student_id: str = Field(alias='YYRGH')
    reservation_status: BusAppointmentStatusType = Field(alias='YYZT', default=BusAppointmentStatusType.needs_verification)
    user_number: str | None = Field(alias='no', default=None) # same as student_id

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    def model_dump(self, **kwargs):
        if not 'by_alias' in kwargs.keys():
            kwargs['by_alias'] = True
        dumped = super().model_dump(**kwargs)

        if self.user_number is None:
            dumped['no'] = self.student_id
        dumped['YYZT'] = self.reservation_status.value

        return dumped
    

class BusUserAppointmentData(BaseModel):
    records: List[Any] | Any = Field(alias='list', default=None) # todo: needs to be filled
    is_need_server_time: bool = Field(alias='isNeedServerTime')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class BusUserAppointmentResponse(BaseModel):
    is_success: bool = Field(alias='isSuccess')
    data: Optional[BusUserAppointmentData] | Any = Field(default=None)
    is_open_dialog: bool = Field(alias='IsOpenDialog')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class BusRouteType(str, Enum):
    commuting_car = '通勤车'

class BusRouteByTypeRequest(BaseModel):
    """
    POST
    https://hq-bus.nwpu.edu.cn/api/GetRouteByType
    form data
    """
    type_: BusRouteType = Field(alias='type', default=BusRouteType.commuting_car)
    student_id: str = Field(alias='no')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    def model_dump(self, **kwargs):
        if not 'by_alias' in kwargs.keys():
            kwargs['by_alias'] = True
        dumped = super().model_dump(**kwargs)
        dumped['type'] = self.type_.value

        return dumped

class FilteredBusRoute(BaseModel):
    id: str = Field(alias='Objid')
    type: str = Field(alias='Type')
    name: str = Field(alias='Name')
    start_station: str = Field(alias='StartStation')
    end_station: str = Field(alias='EndStation')
    student_charge: str = Field(alias='StudentCharge')
    teacher_staff_charge: str = Field(alias='TeacherStaffCharge')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class BusRouteReservationDays(BaseModel):
    wtf_yywyxzts: str = Field(alias='YYWYXZTS')
    wtf_reserve_in_advance: str = Field(alias='TQYYXZTS')
    wtf_jctqyyxzts: str = Field(alias='JCTQYYXZTS')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class BusRouteData(BaseModel):
    filtered_routes: List[FilteredBusRoute] = Field(alias='filteredBusRoutes')
    reservation_days: BusRouteReservationDays = Field(alias='reservationDays')
    is_need_server_time: bool = Field(alias='isNeedServerTime')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class BusRouteByTypeResponse(BaseModel):
    is_success: bool = Field(alias='isSuccess')
    data: Optional[BusRouteData] | Any = Field(default=None)
    is_open_dialog: bool = Field(alias='IsOpenDialog')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class BusRouteDetailRequest(BaseModel):
    """
    POST
    https://hq-bus.nwpu.edu.cn/api/GetReserveInfoList
    form data
    """
    date: datetime.date = Field(alias='rq', default=datetime.date.today)
    route_type: BusRouteType = Field(alias='xllx', default=BusRouteType.commuting_car)
    # should match FilteredBusRoute.id
    route_id: str = Field(alias='xlId')
    student_id: str = Field(alias='gh')
    # same as student_id
    student_no: str | None = Field(alias='no', default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

    def model_dump(self, **kwargs):
        if not 'by_alias' in kwargs.keys():
            kwargs['by_alias'] = True
        dumped = super().model_dump(**kwargs)
        if self.student_no is None:
            dumped['no'] = self.student_id
        dumped['rq'] = self.date.strftime('%Y/%m/%d')
        dumped['xllx'] = self.route_type.value
        return dumped

class BusRouteDetailData(BaseModel):
    id: str = Field(alias='objId')
    departure_time: str = Field(alias='fcsj') # 发车时间
    reserved_seats: int = Field(alias='yyrs') # 预约人数
    available_seats: str = Field(alias='kyyrs') # 可预约座位
    notice_message: str = Field(alias='tsxx') # 提示信息
    reservation_due_message: str = Field(alias='yyjzxx') # 预约截止信息
    is_reservable: bool = Field(alias='sfkyy') # 是否可预约
    verified_student_count: int = Field(alias='xshyrs') # 学生核验人数
    verified_teacher_count: int = Field(alias='jshyrs') # 教师核验人数
    verified_count: int = Field(alias='zhyrs') # 总核验人数
    route_description: str = Field(alias='bcms') # 班次描述

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class BusRouteDetailResponse(BaseModel):
    is_success: bool = Field(alias='isSuccess')
    data: List[BusRouteDetailData] | Any = Field(default=None)
    is_open_dialog: bool = Field(alias='IsOpenDialog')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

