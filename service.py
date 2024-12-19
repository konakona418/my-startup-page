import datetime
import sqlite3 as sqlite
import json
from hashlib import sha256
from typing import List

from aiohttp import ClientSession
from pydantic import BaseModel, Field

from nwpu.ecampus.ec_request import ECampusRequest
from nwpu.ecampus.ec_struct import ECampusUserEventsRequest, ECampusNewsFeedContentRequest
from nwpu.edu.edu_oa import EduOaRequest
from nwpu.edu.edu_request import EduRequest
from nwpu.mail.mail_oa import MailOaRequest
from nwpu.mail.mail_request import MailRequest
from nwpu.mail.mail_struct import MailCategoryResponse, MailListRequest, ReadMailResponse, ReadMailFormRequest
from nwpu.market.market_oa import MarketOaRequest
from nwpu.market.market_request import MarketRequest
from nwpu.oa.mfa import MfaVerifyMethod
from nwpu.oa.oa_request import OaRequest
from nwpu.ecampus.ec_oa import ECampusOaRequest
from nwpu.oa.password import CheckMfaRequiredRequest, PasswordLoginFormRequest
from nwpu.utils.crypto import process_password
from nwpu.utils.parse import generate_fake_browser_fingerprint

session: ClientSession = ClientSession(proxy=None)

conn: sqlite.Connection = sqlite.connect('data.db')

data_fetched = False

def sha256_anything(data: bytes) -> str:
    return sha256(data).hexdigest()

async def login_with_credentials(username: str, password: str) -> bool:
    redirect = ECampusOaRequest.get_redirect_url()
    oa_req = OaRequest(session)
    await oa_req.begin_login(redirect)
    rsa = await oa_req.get_public_key()

    mfa_required = await oa_req.password_init(
        CheckMfaRequiredRequest(username=username, password=process_password(password, rsa)))
    if mfa_required.data.mfa_required:
        mfa = await oa_req.begin_mfa(MfaVerifyMethod.sms, mfa_required.data.state)
        await oa_req.mfa_send_sms(mfa)
        mfa_result = await oa_req.mfa_verify_sms(mfa, input('Requires sms verification; Code:'))

        if mfa_result.code == 0:
            return True
        else:
            return False

    password_login = PasswordLoginFormRequest(username=username, password=process_password(password, rsa),
                                              mfa_state=mfa_required.data.state,
                                              fingerprint=generate_fake_browser_fingerprint()[0])

    await oa_req.finish_password_login(password_login, redirect)

    return True

async def login() -> bool:
    with open('config.json', 'r') as f:
        conf = json.loads(f.read())
        uname = conf['username']
        pwd = conf['password']

        try:
            print('Logging in...')
            return await login_with_credentials(uname, pwd)
        except:
            print('Login failed.')
            return False

async def fetch_mail_list():
    await MailOaRequest.authorize(session)

    mail_req = MailRequest(session)
    category: MailCategoryResponse = await mail_req.get_mail_category()

    mail_list = await mail_req.get_mail_list(MailListRequest())

    for mail in mail_list.categories:
        id = sha256_anything((mail.id + mail.subject + mail.summary).encode())
        cursor = conn.cursor()
        if mail.subject == '':
            mail.subject = '无标题邮件'
        cursor.execute("insert into notifications values(?,?,?,?,?,?)",
                       (id, mail.subject, mail.summary, mail.received_date,
                        mail.id, mail.from_.split(' <')[0][1:-1]))

    conn.commit()

async def fetch_market_messages():
    # todo
    token = await MarketOaRequest.authorize(session)
    market_req = MarketRequest(session, token)

    messages = await market_req.get_message_list()

async def fetch_ecampus_messages() -> bool:
    token = await ECampusOaRequest.authorize(session)
    ec_req = ECampusRequest(session, token)

    columns = await ec_req.get_news_feed_columns()
    for column in columns.data:
        events = await ec_req.get_news_feed_content(
            ECampusNewsFeedContentRequest(column_id=column.id, page_number=1, page_size=10))
        for event in events.data.all_contents:
            id = sha256_anything((event.id + event.title).encode())
            cursor = conn.cursor()
            cursor.execute("insert into notifications values(?,?,?,?,?,?)",
                           (id, event.title, event.title, event.create_time, event.url, event.release_dept_name))

    conn.commit()
    return True

async def fetch_edu_messages() -> bool:
    await EduOaRequest.authorize(session)
    edu_req = EduRequest(session)
    notifications = await edu_req.get_notification()
    for notification in notifications.data:
        id = sha256_anything((str(notification.id) + notification.item + notification.content).encode())
        cursor = conn.cursor()
        cursor.execute("insert into notifications values(?,?,?,?,?,?)",
                       (id, notification.item, notification.content, notification.create_date_time,
                        notification.info_url, '翱翔教务系统'))
    conn.commit()
    return True

async def fetch_notifications() -> bool:
    await fetch_mail_list()
    await fetch_edu_messages()
    await fetch_ecampus_messages()
    try:
        return True
    except:
        return False


async def init_all_tables():
    cursor = conn.cursor()
    cursor.execute("""create table if not exists notifications(id text primary key, 
                    title text, summary text, date text, url text, source text)""")
    cursor.execute("delete from notifications where 1=1")
    conn.commit()

    await login()
    await fetch_notifications()

    global data_fetched
    data_fetched = True

async def get_notification_count() -> int:
    cursor = conn.cursor()
    cursor.execute("select count(*) from notifications")
    return cursor.fetchone()[0]


class Notification(BaseModel):
    id: str
    title: str | None = Field(default=None)
    summary: str | None = Field(default=None)
    date: str | None = Field(default=None)
    url: str | None = Field(default=None)
    source: str | None = Field(default=None)


async def get_notifications() -> List[Notification]:
    cursor = conn.cursor()
    cursor.execute("select * from notifications")
    return [Notification(id=row[0], title=row[1], summary=row[2], date=row[3],
                         url=row[4], source=row[5])
            for row in cursor.fetchall()]


async def close_service():
    await session.close()
    conn.close()
