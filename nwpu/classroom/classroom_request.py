from aiohttp import ClientSession

from nwpu.classroom.classroom_oa import IdleClassroomOaRequest
from nwpu.classroom.classroom_struct import *
from nwpu.utils.common import DEFAULT_HEADER
from nwpu.utils.parse import concat_url


class IdleClassroomUrl:
    CLASSROOM_ALL_CAMPUS = "https://idle-classroom.nwpu.edu.cn/api/idleclassroom/campus"
    CLASSROOM_TEACHING_BUILDINGS = "https://idle-classroom.nwpu.edu.cn/api/idleclassroom/building"
    CLASSROOM_TEACHING_WEEKS = "https://idle-classroom.nwpu.edu.cn/api/idleclassroom/week/"

    CLASSROOM_IDLE_LIST = "https://idle-classroom.nwpu.edu.cn/api/idleclassroom/classroom"
    CLASSROOM_SELECT_BY_TIME = "https://idle-classroom.nwpu.edu.cn/api/idleclassroom/table"

    CLASSROOM_ROOM_TYPES = "https://idle-classroom.nwpu.edu.cn/api/idleclassroom/roomtype"
    CLASSROOM_SEAT_CODES = "https://idle-classroom.nwpu.edu.cn/api/base/dict/children/room_type"
    CLASSROOM_IDLE_DETAILS = "https://idle-classroom.nwpu.edu.cn/api/idleclassroom/detail"

class IdleClassroomRequest:
    sess: ClientSession
    headers: dict = DEFAULT_HEADER.copy()

    def __init__(self, sess: ClientSession, x_token: str):
        self.sess: ClientSession = sess

        if x_token:
            self.headers['X-Id-Token'] = x_token
        else:
            raise ValueError("X-Id-Token is required.")

    async def get_token(self) -> str:
        token = await IdleClassroomOaRequest.authorize(self.sess)
        self.headers['X-Id-Token'] = token
        return token

    async def get_all_campus(self) -> IdleClassroomAllCampusResponse:
        resp = await self.sess.get(IdleClassroomUrl.CLASSROOM_ALL_CAMPUS,
                                    headers=self.headers)
        return IdleClassroomAllCampusResponse(**await resp.json())

    async def get_teaching_buildings(self, campus_name: str) -> IdleClassroomTeachingBuildingResponse:
        resp = await self.sess.get(
            concat_url(IdleClassroomUrl.CLASSROOM_TEACHING_BUILDINGS, campus_name),
            headers=self.headers)
        return IdleClassroomTeachingBuildingResponse(**await resp.json())

    async def get_teaching_weeks(self, campus_name) -> IdleClassroomTeachingWeeksResponse:
        resp = await self.sess.get(
            concat_url(IdleClassroomUrl.CLASSROOM_TEACHING_WEEKS, campus_name),
            headers=self.headers)
        return IdleClassroomTeachingWeeksResponse(**await resp.json())

    async def get_idle_classroom_list(self, req: IdleClassroomListRequest) -> IdleClassroomListResponse:
        """
        list all the classrooms, with idle time attached.
        :param req:
        :return:
        """
        resp = await self.sess.get(
            IdleClassroomUrl.CLASSROOM_IDLE_LIST,
            params=req.model_dump(),
            headers=self.headers)
        return IdleClassroomListResponse(**await resp.json())

    async def get_idle_classroom_count_by_time(self, req: IdleClassroomByTimeRequest) -> IdleClassroomByTimeResponse:
        """
        list the count of the classrooms that satisfy the requirements.
        note that this will not return the details of the classrooms.
        :param req:
        :return:
        """
        resp = await self.sess.get(
            IdleClassroomUrl.CLASSROOM_SELECT_BY_TIME,
            params=req.model_dump(by_alias=True, exclude_none=True),
            headers=self.headers)
        return IdleClassroomByTimeResponse(**await resp.json())

    async def get_room_type(self, campus_name: str) -> IdleClassroomRoomTypeResponse:
        resp = await self.sess.get(
            concat_url(IdleClassroomUrl.CLASSROOM_ROOM_TYPES, campus_name),
            headers=self.headers)
        return IdleClassroomRoomTypeResponse(**await resp.json())

    async def get_seat_code(self) -> IdleClassroomSeatCodeResponse:
        resp = await self.sess.get(
            IdleClassroomUrl.CLASSROOM_SEAT_CODES,
            headers=self.headers)
        return IdleClassroomSeatCodeResponse(**await resp.json())

    async def get_idle_classroom_detail(self, req: IdleClassroomDetailRequest) -> IdleClassroomDetailResponse:
        resp = await self.sess.get(
            IdleClassroomUrl.CLASSROOM_IDLE_DETAILS,
            params=req.model_dump(by_alias=True, exclude_none=True),
            headers=self.headers)
        return IdleClassroomDetailResponse(**await resp.json())
