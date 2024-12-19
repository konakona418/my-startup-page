from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class QrStatus(int, Enum):
    initialize = 0
    sent = 1
    valid = 2
    invalid = 3
    cancel = 5
    scanned = 8
    expired = 9

class QrResponseQr(BaseModel):
    accounts: Optional[list[str] | str] = None
    app_token: Optional[str] = Field(alias='apptoken')
    device: Optional[str] = None
    status: Optional[QrStatus] = Field(default=QrStatus.initialize)
    timestamp: int

    class Config:
        populate_by_name = True


class QrInitResponseData(BaseModel):
    qr_code: QrResponseQr = Field(alias='qrCode')
    state_key: str = Field(alias='stateKey')

    class Config:
        populate_by_name = True

class QrInitRequest(BaseModel):
    """
    POST
    https://uis.nwpu.edu.cn/cas/qr/init
    """
    pass

class QrInitResponse(BaseModel):
    code: int
    data: Optional[QrInitResponseData] = None
    message: Optional[str] = None


class QrImageRequest(BaseModel):
    """
    GET
    https://uis.nwpu.edu.cn/cas/qr/qrcode?r=<ts_mill> + floor(math.random() * 24)
    """
    r: int

class QrImageResponse(BaseModel):
    """
    Raw Image Data
    """
    pass

class QrCometRequest(BaseModel):
    """
    POST
    https://uis.nwpu.edu.cn/cas/qr/comet
    """
    pass

class QrCometResponse(QrInitResponse):
    """
    Same as QrInitResponse
    """
    pass


class QrLoginFormRequest(BaseModel):
    """
    POST
    https://uis.nwpu.edu.cn/cas/login?service=<redirect_url>
    """
    qr_state_key: str = Field(alias='qrCodeKey')
    current_menu: int = Field(alias='currentMenu', default=3)
    geo_location: Optional[str] = Field(alias='geolocation', default='')
    fingerprint: str = Field(alias='fpVisitorId')

    #username: str
    ##password: str = Field(alias='password')
    #mfa_state: str = Field(alias='mfaState')
    event_id: str = Field(alias='_eventId', default='submit')
    execution: str = Field(alias='execution', default='')

    class Config:
        populate_by_name = True