# D:\AI\AI_Trading_System_ki\utils\encryption.py
import base64
from cryptography.fernet import Fernet
import keyring

SERVICE_NAME = "AI_Trading_System_v7"

def get_or_create_key():
    key = keyring.get_password(SERVICE_NAME, "master_key")
    if key is None:
        key = Fernet.generate_key().decode()
        keyring.set_password(SERVICE_NAME, "master_key", key)
    return key.encode()

def encrypt(raw: str) -> str:
    f = Fernet(get_or_create_key())
    return base64.b64encode(f.encrypt(raw.encode())).decode()

def decrypt(enc: str) -> str:
    f = Fernet(get_or_create_key())
    return f.decrypt(base64.b64decode(enc)).decode()