from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

class MfaStatus(int, Enum):
    initialize = 0
    sent = 1
    valid = 2
    invalid = 3
    cancel = 5
    expired = 9

class MfaVerifyMethod(str, Enum):
    app_push = "apppush" # push a message to the phone
    sms = "securephone" # send sms to the phone
    email = "secureemail" # send email to the verified email addr
    qr_code = "qrcode" # scan qr on the mobile app
    face_verify = "faceverify" # deprecated

class CheckMfaRequiredData(BaseModel):
    mfa_type_secure_phone: bool = Field(alias="mfaTypeSecurePhone")
    mfa_type_qr_code: bool = Field(alias="mfaTypeQrCode")
    mfa_required: bool = Field(alias="need")
    mfa_type_app_push: bool = Field(alias="mfaTypeAppPush")
    mfa_type_face_verify: bool = Field(alias="mfaTypeFaceVerify")
    mfa_enabled: bool = Field(alias="mfaEnabled")
    state: str
    mfa_type_secure_email: bool = Field(alias="mfaTypeSecureEmail")

    class Config:
        populate_by_name = True

class CheckMfaRequiredResponse(BaseModel):
    code: int
    data: CheckMfaRequiredData

    class Config:
        populate_by_name = True

class MfaInitData(BaseModel):
    secure_phone: Optional[bool | str] = Field(alias="securePhone", default='')
    secure_email: Optional[bool | str] = Field(alias="secureEmail", default='')
    qr_code: Optional[str | bool] = Field(alias="qrCode", default='')

    attest_server_url: str = Field(alias="attestServerUrl")
    gid: str = Field(alias="gid")

    class Config:
        populate_by_name = True

class MfaInitResponse(BaseModel):
    code: int
    data: MfaInitData

    class Config:
        populate_by_name = True


class MfaSendAppPushRequest(BaseModel):
    gid: str

    class Config:
        populate_by_name = True

class MfaAppPushData(BaseModel):
    callback_code: str = Field(alias="callbackCode")

    class Config:
        populate_by_name = True


class MfaSendAppPushResponse(BaseModel):
    code: int
    data: MfaAppPushData

    class Config:
        populate_by_name = True

class MfaCheckAppPushStatusRequest(BaseModel):
    gid: str

    class Config:
        populate_by_name = True

class MfaCheckAppPushStatusData(BaseModel):
    status: MfaStatus

    class Config:
        populate_by_name = True


class MfaCheckAppPushStatusResponse(BaseModel):
    code: int
    data: MfaCheckAppPushStatusData

    class Config:
        populate_by_name = True

class MfaSendSmsRequest(BaseModel):
    gid: str

    class Config:
        populate_by_name = True


class MfaSendSmsData(BaseModel):
    result: str

    class Config:
        populate_by_name = True


class MfaSendSmsResponse(BaseModel):
    code: int
    data: MfaSendSmsData


class MfaVerifySmsData(BaseModel):
    status: MfaStatus


class MfaVerifySmsResponse(BaseModel):
    code: int
    data: MfaVerifySmsData


class MfaSendMailRequest(BaseModel):
    gid: str

    class Config:
        populate_by_name = True


class MfaSendMailData(BaseModel):
    result: str

    class Config:
        populate_by_name = True

class MfaSendMailResponse(BaseModel):
    code: int
    data: MfaSendMailData

    class Config:
        populate_by_name = True

class MfaVerifyMailData(BaseModel):
    status: MfaStatus

    class Config:
        populate_by_name = True

class MfaVerifyMailResponse(BaseModel):
    code: int
    data: MfaVerifyMailData

    class Config:
        populate_by_name = True

