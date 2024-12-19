import random
from math import floor

from aiohttp import ClientSession
from yarl import URL

from nwpu.oa.mfa import CheckMfaRequiredResponse, MfaVerifyMethod, MfaInitResponse, MfaSendAppPushResponse, \
    MfaCheckAppPushStatusResponse, MfaSendSmsResponse, MfaVerifySmsResponse, MfaVerifyMailResponse, MfaSendMailResponse
from nwpu.oa.password import CheckMfaRequiredRequest, PasswordLoginFormRequest
from nwpu.oa.qrcode import QrInitResponse, QrLoginFormRequest, QrCometResponse
from nwpu.utils.common import DEFAULT_HEADER, timestamp_mill
from nwpu.utils.parse import StringArgsBuilder, find_tracer_id
from nwpu.oa.dyncode import SmsLoginSendCodeRequest, SmsLoginSendCodeResponse, SmsLoginFormRequest


class OaRequestUrl:
    #OA_BEGIN_AUTHORIZE = 'https://uis.nwpu.edu.cn/cas/oauth2.0/authorize'
    OA_PUBLIC_KEY = 'https://uis.nwpu.edu.cn/cas/jwt/publicKey'
    OA_QR_INIT = 'https://uis.nwpu.edu.cn/cas/qr/init'
    OA_QR_IMAGE = 'https://uis.nwpu.edu.cn/cas/qr/qrcode'
    OA_QR_COMET = 'https://uis.nwpu.edu.cn/cas/qr/comet'
    OA_SMS_SEND = 'https://uis.nwpu.edu.cn/cas/passwordlessTokenSend'
    OA_LOGIN = 'https://uis.nwpu.edu.cn/cas/login'
    OA_PWD_DETECT = 'https://uis.nwpu.edu.cn/cas/mfa/detect'

    OA_MFA_INIT = "https://uis.nwpu.edu.cn/cas/mfa/initByType"


class OaRequest:
    sess: ClientSession
    tracer_id: str
    def __init__(self, sess: ClientSession):
        self.sess: ClientSession = sess
        self.tracer_id = ''

    def set_cookie(self, cookie: str):
        self.sess.cookie_jar.update_cookies({'SESSION': cookie})

    async def begin_login(self, redirect_url =''):
        """
        Begin a new OA session.
        :param redirect_url: the redirect url of the targeted application.
        :return: True if the session is not configured, otherwise False.
        """
        resp = await self.sess.get(
            OaRequestUrl.OA_LOGIN + (('?service=' + redirect_url) if redirect_url != '' else ''),
            headers=DEFAULT_HEADER,
            allow_redirects=True)
        # if the user has not logged in.
        if not resp.history:
            if len((tracer := find_tracer_id(await resp.text()))) > 0:
                self.tracer_id = tracer[0]
        return not resp.history

    async def get_public_key(self) -> str:
        """
        Get the RSA PCKS1-1.5 public key.
        :return: the public key.
        """
        resp = await self.sess.get(OaRequestUrl.OA_PUBLIC_KEY, headers=DEFAULT_HEADER)
        return await resp.text()

    async def qr_init(self) -> QrInitResponse:
        """
        Initialize the QR code login.
        :return:
        """
        resp = await self.sess.post(OaRequestUrl.OA_QR_INIT, headers=DEFAULT_HEADER)
        return QrInitResponse(**await resp.json())

    async def qr_get_image(self) -> bytes:
        """
        Get the QR code image.
        :return:
        """
        ts_mill = timestamp_mill() + floor(random.random() * 24)
        resp = await self.sess.get(
            StringArgsBuilder(OaRequestUrl.OA_QR_IMAGE)
                .add_param('r', str(ts_mill))
                .build(),
            headers=DEFAULT_HEADER,
        )
        return await resp.read()

    async def qr_comet(self) -> QrCometResponse:
        """
        Probes the state of the QR code scanning.
        :return:
        """
        resp = await self.sess.post(OaRequestUrl.OA_QR_COMET, headers=DEFAULT_HEADER)
        return QrCometResponse(**await resp.json())

    async def password_init(self, form_data: CheckMfaRequiredRequest) -> CheckMfaRequiredResponse:
        """
        Checks the mfa state. If the data.mfa_required == True, the user should go through the mfa process.
        :param form_data:
        :return:
        """
        data = form_data.model_dump(by_alias=True)
        resp = await self.sess.post(
            OaRequestUrl.OA_PWD_DETECT,
            headers=DEFAULT_HEADER,
            data=data,
        )
        return CheckMfaRequiredResponse(**await resp.json())

    async def sms_init(self, req: SmsLoginSendCodeRequest) -> SmsLoginSendCodeResponse:
        """
        sends the verification code via sms.
        :param req:
        :return:
        """
        data = req.model_dump(by_alias=True)
        resp = await self.sess.post(
            OaRequestUrl.OA_SMS_SEND,
            headers=DEFAULT_HEADER,
            data=data,)
        return SmsLoginSendCodeResponse(**await resp.json())


    async def finish_qr_login(self, form_data: QrLoginFormRequest, redirect_url ='') -> list[URL]:
        """
        Finish the QR code login. Auto-redirects to the target application.
        :param redirect_url:
        :param form_data:
        :return: The redirect history.
        """
        redirects = list()
        if self.tracer_id != '':
            print('tracer_id: ' + self.tracer_id)
            form_data.execution = self.tracer_id
        data = form_data.model_dump(by_alias=True)
        resp = await self.sess.post(
            StringArgsBuilder(OaRequestUrl.OA_LOGIN)
                .add_param('service', redirect_url)
                .build(),
            headers=DEFAULT_HEADER,
            data=data,
            allow_redirects=True
        )
        for i in resp.history:
            redirects.append(i.url)

        return redirects

    async def finish_password_login(self, form_data: PasswordLoginFormRequest, redirect_url: str = '') -> list[URL]:
        """
        Finish the password login. Auto-redirects to the target application.
        :param redirect_url:
        :param form_data:
        :return: The redirect history.
        """
        redirects = list()
        if self.tracer_id != '':
            #print('tracer_id: ' + self.tracer_id)
            form_data.execution = self.tracer_id
        data = form_data.model_dump(by_alias=True)

        resp = await self.sess.post(
            OaRequestUrl.OA_LOGIN + (('?service=' + redirect_url) if redirect_url != '' else ''),
            headers=DEFAULT_HEADER,
            allow_redirects=True,
            data=data)

        for i in resp.history:
            redirects.append(i.url)
        return redirects

    async def finish_sms_login(self, form_data: SmsLoginFormRequest, redirect_url: str = '') -> list[URL]:
        redirects = list()
        if self.tracer_id != '':
            form_data.execution = self.tracer_id
        data = form_data.model_dump(by_alias=True)

        resp = await self.sess.post(
            OaRequestUrl.OA_LOGIN + (('?service=' + redirect_url) if redirect_url != '' else ''),
            headers=DEFAULT_HEADER,
            allow_redirects=True,
            data=data)

        for i in resp.history:
            redirects.append(i.url)
        return redirects


    async def begin_mfa(self, mfa_type: MfaVerifyMethod, mfa_state: str) -> MfaInitResponse:
        resp = await self.sess.get(
            OaRequestUrl.OA_MFA_INIT + '/' + mfa_type.value + '?state=' + mfa_state,
            headers=DEFAULT_HEADER,)

        print(await resp.text())
        return MfaInitResponse(**await resp.json())

    async def mfa_send_app_push(self, mfa_init_response: MfaInitResponse) -> MfaSendAppPushResponse:
        attest_url = mfa_init_response.data.attest_server_url
        gid = mfa_init_response.data.gid

        resp = await self.sess.post(
            attest_url + '/api/guard/apppush/send',
            headers=DEFAULT_HEADER,
            json={'gid': gid})

        return MfaSendAppPushResponse(**await resp.json())

    async def mfa_verify_app_push(self, mfa_init_response: MfaInitResponse) -> MfaCheckAppPushStatusResponse:
        attest_url = mfa_init_response.data.attest_server_url
        gid = mfa_init_response.data.gid

        resp = await self.sess.post(
            attest_url + '/api/guard/apppush/status',
            headers=DEFAULT_HEADER,
            json={'gid': gid})

        return MfaCheckAppPushStatusResponse(**await resp.json())


    async def mfa_send_sms(self, mfa_init_response: MfaInitResponse) -> MfaSendAppPushResponse:
        attest_url = mfa_init_response.data.attest_server_url
        gid = mfa_init_response.data.gid

        resp = await self.sess.post(
            attest_url + '/api/guard/securephone/send',
            headers=DEFAULT_HEADER,
            json={'gid': gid})

        return MfaSendSmsResponse(**await resp.json())

    async def mfa_verify_sms(self, mfa_init_response: MfaInitResponse, verify_code: str) -> MfaVerifySmsResponse:
        attest_url = mfa_init_response.data.attest_server_url
        gid = mfa_init_response.data.gid

        resp = await self.sess.post(
            attest_url + '/api/guard/securephone/valid',
            headers=DEFAULT_HEADER,
            json={'gid': gid, 'code': verify_code})

        return MfaVerifySmsResponse(**await resp.json())

    async def mfa_send_email(self, mfa_init_response: MfaInitResponse) -> MfaSendMailResponse:
        attest_url = mfa_init_response.data.attest_server_url
        gid = mfa_init_response.data.gid

        resp = await self.sess.post(
            attest_url + '/api/guard/secureemail/send',
            headers=DEFAULT_HEADER,
            json={'gid': gid})

        return MfaSendMailResponse(**await resp.json())

    async def mfa_verify_email(self, mfa_init_response: MfaInitResponse, verify_code: str) -> MfaVerifyMailResponse:

        attest_url = mfa_init_response.data.attest_server_url
        gid = mfa_init_response.data.gid

        resp = await self.sess.post(
            attest_url + '/api/guard/secureemail/valid',
            headers=DEFAULT_HEADER,
            json={'gid': gid, 'code': verify_code})

        return MfaVerifyMailResponse(**await resp.json())