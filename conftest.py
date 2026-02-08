import os

from common.config import PUBLIC_KEY, SERVER_URL
import pytest
import time
import requests

from utils.data_utils import clear_extract_yaml
from utils.rsa_utils import PasswordEncryptor
import logging

@pytest.fixture(scope='session',autouse=True)
def get_token():
    # 配置日志记录器
    logger = logging.getLogger("Hsyuan")

    username = 'admin'
    password = "123456"
    user_type = "admin"

    entrytor = PasswordEncryptor()
    pem_public_key = "-----BEGIN PUBLIC KEY-----"+PUBLIC_KEY+"-----END PUBLIC KEY-----"
    entrytor.set_public_key(pem_public_key)
    password_rsa = entrytor.encryptPassword(password)

    params = {
        "username": username,
        "password": password_rsa,
        "userType": user_type,
        "timestamp": int(time.time() * 1000)
    }

    resp = requests.request("POST", SERVER_URL+"/login", json=params)
    resp.raise_for_status()
    token = resp.json()["data"]["token"]
    logger.info(f"初始化配置，获取TOKEN成功！\n TOKEN:{token}")

    os.environ["TOKEN"] = token
    return token

@pytest.fixture(scope='session',autouse=True)
def setup_and_teardown():
    logger = logging.getLogger("Hsyuan")
    logger.info("测试会话开始，执行前置操作")
    clear_extract_yaml()
    yield
    logger.info("测试会话结束，执行后置操作")






