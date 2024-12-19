import base64

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

ENCRYPTED_PASSWORD_PREFIX = '__RSA__'

def encrypt_password(password: str, public_key: str) -> str:
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    encrypted_text = base64.b64encode(cipher.encrypt(password.encode(encoding='utf-8')))
    return encrypted_text.decode(encoding='utf-8')


def wrap_password(password_encrypted: str):
    return ENCRYPTED_PASSWORD_PREFIX + password_encrypted

def process_password(password: str, public_key: str) -> str:
    password_rsa = encrypt_password(password, public_key)
    if password_rsa.startswith(ENCRYPTED_PASSWORD_PREFIX):
        return password_rsa
    else:
        return wrap_password(encrypt_password(password, public_key))