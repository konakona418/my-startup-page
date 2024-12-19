import datetime
from datetime import date
from enum import Enum
from typing import List, Optional, Any, Dict

from pydantic import BaseModel, Field

class IdleClassroomAllCampusRequest(BaseModel):
    """
    GET
    https://idle-classroom.nwpu.edu.cn/api/idleclassroom/campus
    """
    pass

class IdleClassroomAllCampusResponse(BaseModel):
    success: Optional[bool | str] | Any = Field(default=None)
    code: int
    msg: Optional[str] = Field(default=None)

    # campus names here
    data: List[str] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class IdleClassroomTeachingBuildingRequest(BaseModel):
    """
    GET
    https://idle-classroom.nwpu.edu.cn/api/idleclassroom/building/<campus name>
    """
    pass

class IdleClassroomTeachingBuildingResponse(BaseModel):
    success: Optional[bool | str] | Any = Field(default=None)
    code: int
    msg: Optional[str] = Field(default=None)

    # teaching building names here
    data: List[str] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class IdleClassroomTeachingWeeksRequest(BaseModel):
    """
    GET
    https://idle-classroom.nwpu.edu.cn/api/idleclassroom/week/<campus name>
    """
    pass

class IdleClassroomTeachingWeeksData(BaseModel):
    semester_name: str = Field(alias='semesterName')
    week_of_semester: int = Field(alias='weekOfSemester')

    # unix timestamp ms
    start_day_ts_mills: int = Field(alias='startDay')
    # unix timestamp ms
    end_day_ts_mills: int = Field(alias='endDay')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdleClassroomTeachingWeeksResponse(BaseModel):
    success: bool
    code: int
    msg: str
    data: List[IdleClassroomTeachingWeeksData] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdleClassroomListRequest(BaseModel):
    """
    GET
    https://idle-classroom.nwpu.edu.cn/api/idleclassroom/classroom
    url params
    """

    # corresponds to the teaching building name
    building: str = Field(default='-2')

    # corresponds to campus name
    campus: str = Field(default='-2')

    # corresponds to week_of_semester in IdleClassroomTeachingWeeksData
    week_of_semester: int = Field(alias='weekOfSemester')

    end_date_of_week: date = Field(alias='endDateOfWeek')
    start_date_of_week: date = Field(alias='startDateOfWeek')

    # unknown
    room_type: int = Field(alias='roomType', default=-2)
    seat_code: int = Field(alias='seatCode', default=-2)

    # filter by unit. optional.
    start_unit: Optional[int] | None = Field(alias='startUnit', default=None)
    end_unit: Optional[int] | None = Field(alias='endUnit', default=None)

    def model_dump(self, **kwargs):
        if not 'by_alias' in kwargs.keys():
            kwargs['by_alias'] = True
        if not 'exclude_none' in kwargs.keys():
            kwargs['exclude_none'] = True

        dumped = super().model_dump(**kwargs)

        dumped['endDateOfWeek'] = dumped['endDateOfWeek'].strftime('%Y-%m-%d')
        dumped['startDateOfWeek'] = dumped['startDateOfWeek'].strftime('%Y-%m-%d')

        return dumped

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

        json_encoders = {
            datetime.date: lambda v: v.strftime('%Y-%m-%d'),
            datetime.datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class IdleClassroomListCountMapItem(BaseModel):
    classroom_name: str = Field(alias='classroomName')
    unit_list: List[str] = Field(alias='unitList')
    is_idle: bool = Field(alias='isIdle')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class IdleClassroomListData(BaseModel):
    # 1, 2, 3, ... -> List[CountMapItem]
    count_map: Dict[str, List[IdleClassroomListCountMapItem] | Any] = Field(alias='countMap')

    # 1, 2, 3, ... -> timestamp
    date_map: Dict[str, int | Any] = Field(alias='dateMap')

    # units list contains all the existing courses
    units_list: List[int] = Field(alias='unitsList')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdleClassroomListResponse(BaseModel):
    success: Optional[bool | str] | Any = Field(default=None)
    code: int
    msg: Optional[str] | Any = Field(default=None)
    data: Optional[IdleClassroomListData] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdleClassroomByTimeRequest(BaseModel):
    """
    GET
    https://idle-classroom.nwpu.edu.cn/api/idleclassroom/table
    url params
    """
    building: str = Field(default='-2')
    campus: str = Field(default='-2')
    week_of_semester: int = Field(alias='weekOfSemester')

    end_date_of_week: date = Field(alias='endDateOfWeek')
    start_date_of_week: date = Field(alias='startDateOfWeek')

    start_unit: Optional[int] | None = Field(alias='startUnit', default=None)
    end_unit: Optional[int] | None = Field(alias='endUnit', default=None)

    def model_dump(self, **kwargs):
        if not 'by_alias' in kwargs.keys():
            kwargs['by_alias'] = True
        if not 'exclude_none' in kwargs.keys():
            kwargs['exclude_none'] = True

        dumped = super().model_dump(**kwargs)

        dumped['endDateOfWeek'] = dumped['endDateOfWeek'].strftime('%Y-%m-%d')
        dumped['startDateOfWeek'] = dumped['startDateOfWeek'].strftime('%Y-%m-%d')

        return dumped

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

        json_encoders = {
            datetime.date: lambda v: v.strftime('%Y-%m-%d'),
            datetime.datetime: lambda v: v.strftime('%Y-%m-%d %H:%M:%S')
        }

class IdleClassroomByTimeCountMapItem(BaseModel):
    unit: str
    num: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class IdleClassroomByTimeData(BaseModel):
    count_map: Dict[str, List[IdleClassroomByTimeCountMapItem] | Any] = Field(alias='countMap')
    date_map: Dict[str, int] | Any = Field(alias='dateMap')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class IdleClassroomByTimeResponse(BaseModel):
    success: Optional[bool | str] | Any = Field(default=None)
    code: int
    msg: Optional[str] | Any = Field(default=None)
    data: Optional[IdleClassroomByTimeData] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

class IdleClassroomRoomTypeRequest(BaseModel):
    """
    GET
    https://idle-classroom.nwpu.edu.cn/api/idleclassroom/roomtype/<campus>
    """
    pass

class IdleClassroomRoomTypeResponse(BaseModel):
    success: Optional[bool | str] | Any = Field(default=None)
    code: int
    msg: Optional[str] = Field(default=None)
    data: List[str] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdleClassroomSeatCodeRequest(BaseModel):
    """
    GET
    https://idle-classroom.nwpu.edu.cn/api/base/dict/children/room_type
    """
    pass

class IdleClassroomSeatCodeItem(BaseModel):
    id: str
    parent_id: str = Field(alias='parentId')
    top_id: str = Field(alias='topId')
    code: str
    name: str
    eng_name: str = Field(alias='engName')
    sort: int
    remark: str
    is_deleted: int = Field(alias='isDeleted')


class IdleClassroomSeatCodeResponse(BaseModel):
    success: Optional[bool | str] | Any = Field(default=None)
    code: int
    msg: Optional[str] = Field(default=None)
    data: List[IdleClassroomSeatCodeItem] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
    

class IdleClassroomDetailRequest(BaseModel):
    """
    GET
    https://idle-classroom.nwpu.edu.cn/api/idleclassroom/detail
    url params
    """
    building: str = Field(default='-2')
    campus: str = Field(default='-2')
    classroom: str = Field(default='-2')

    week_of_semester: int = Field(alias='weekOfSemester')
    weekday: int = Field(alias='weekday')
    end_date_of_week: date = Field(alias='endDateOfWeek')
    start_date_of_week: date = Field(alias='startDateOfWeek')

    room_type: int = Field(alias='roomType', default=-2)
    seat_code: int = Field(alias='seatCode', default=-2)

    start_unit: int = Field(alias='startUnit', default=1)
    end_unit: int = Field(alias='endUnit', default=12)

    current_page: int = Field(alias='current', default=1)
    page_size: int = Field(alias='size', default=10)

    def model_dump(self, **kwargs):
        if not 'by_alias' in kwargs.keys():
            kwargs['by_alias'] = True
        if not 'exclude_none' in kwargs.keys():
            kwargs['exclude_none'] = True

        dumped = super().model_dump(**kwargs)
        dumped['endDateOfWeek'] = dumped['endDateOfWeek'].strftime('%Y-%m-%d')
        dumped['startDateOfWeek'] = dumped['startDateOfWeek'].strftime('%Y-%m-%d')
        return dumped

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        
class IdleClassroomDetailRecord(BaseModel):
    id: str
    campus: str
    building: str
    classroom: str
    classroom_code: str = Field(alias='classroomCode')
    room_type: str = Field(alias='roomType')
    seat: str
    weeks: Any
    units: Any
    weekday: Any
    room_key: str = Field(alias='roomKey')

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdleClassroomDetailData(BaseModel):
    records: Optional[List[IdleClassroomDetailRecord]] | Any = Field(default=None)
    total: int
    size: int
    current: int
    orders: Optional[List[Any]] | Any = Field(default=None)
    optimize_count_sql: bool = Field(alias='optimizeCountSql')
    hit_count: bool = Field(alias='hitCount')
    count_id: Any = Field(alias='countId')
    max_limit: Any = Field(alias='maxLimit')
    search_count: bool = Field(alias='searchCount')
    pages: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class IdleClassroomDetailResponse(BaseModel):
    success: Optional[bool | str] | Any = Field(default=None)
    code: int
    msg: Optional[str] = Field(default=None)
    data: Optional[IdleClassroomDetailData] | Any = Field(default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


