from typing import Optional, Any

from pydantic import BaseModel, Field

from nwpu.utils.parse import generate_fake_browser_fingerprint

class SmsLoginSendCodeRequest(BaseModel):
    """
    POST
    https://uis.nwpu.edu.cn/cas/passwordlessTokenSend
    form data
    """
    username: str

class SmsLoginSendCodeResponse(BaseModel):
    data: Any

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class SmsLoginFormRequest(BaseModel):
    """
    """
    username: str
    password: str = Field(alias='password')
    current_menu: int = Field(alias='currentMenu', default=2)
    #mfa_state: str = Field(alias='mfaState')
    geo_location: Optional[str] = Field(alias='geolocation', default='')
    fingerprint: str = Field(alias='fpVisitorId', default=generate_fake_browser_fingerprint()[0])
    event_id: str = Field(alias='_eventId', default='submitPasswordlessToken')
    execution: str = Field(alias='execution', default='')

    class Config:
        populate_by_name = True