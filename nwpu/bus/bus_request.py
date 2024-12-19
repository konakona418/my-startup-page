from aiohttp import ClientSession

from nwpu.bus.bus_oa import BusOaRequest
from nwpu.bus.bus_struct import *
from nwpu.utils.common import DEFAULT_HEADER

class BusUrls:
    BUS_APPOINTMENTS = "https://hq-bus.nwpu.edu.cn/api/GetMyAppointment"
    BUS_ROUTES = "https://hq-bus.nwpu.edu.cn/api/GetRouteByType"
    BUS_ROUTE_DETAILS = "https://hq-bus.nwpu.edu.cn/api/GetReserveInfoList"


class BusRequest:
    sess: ClientSession
    headers: dict = DEFAULT_HEADER.copy()

    def __init__(self, sess: ClientSession, force_auth: bool = False):
        self.sess = sess
        if force_auth:
            BusOaRequest.authorize(sess)

    async def get_user_appointments(self, req: BusUserAppointmentsRequest) -> BusUserAppointmentResponse:
        resp = await self.sess.post(BusUrls.BUS_APPOINTMENTS,
                                    headers=self.headers,
                                    data=req.model_dump(by_alias=True))

        return BusUserAppointmentResponse(**await resp.json())

    async def get_bus_route(self, req: BusRouteByTypeRequest) -> BusRouteByTypeResponse:
        resp = await self.sess.post(BusUrls.BUS_ROUTES,
                                      headers=self.headers,
                                      data=req.model_dump(by_alias=True))

        return BusRouteByTypeResponse(**await resp.json())

    async def get_bus_route_detail(self, req: BusRouteDetailRequest) -> BusRouteDetailResponse:
        resp = await self.sess.post(BusUrls.BUS_ROUTE_DETAILS,
                                      headers=self.headers,
                                      data=req.model_dump(by_alias=True))

        return BusRouteDetailResponse(**await resp.json())
