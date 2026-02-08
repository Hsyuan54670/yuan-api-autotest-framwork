import os

from common.config import SERVER_URL, PUBLIC_KEY
import pytest
import time
import requests

from testcases.test_login_api import TestLoginAPI
from utils.data_utils import clear_extract_yaml, extract_yaml, read_yaml_list, read_yaml
from utils.rsa_utils import PasswordEncryptor
import logging


# 配置日志记录器
logger = logging.getLogger("Hsyuan")

@pytest.fixture(scope='module',autouse=False)
def get_admin_token():

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

    session = requests.Session()
    resp = session.request("POST", SERVER_URL+"/login", json=params)
    resp.raise_for_status()
    token = resp.json()["data"]["token"]
    session.headers.update({
        "Token": token
    })
    extract_yaml("init_token", token)

    yield session

    session.close()



@pytest.fixture(scope='session',autouse=True)
def setup_and_teardown():

    logger = logging.getLogger("Hsyuan")
    logger.info("初始化配置中...测试会话即将开始...")

    clear_extract_yaml()

    get_public_key = TestLoginAPI()
    get_public_key.test_get_public_key(read_yaml_list("data/test_data/login_public_key.yaml")[0])

    PUBLIC_KEY=read_yaml("config/extract.yaml")["publicKey"]

    logger.info("初始化配置完成,测试会话开始!")
    yield
    logger.info("测试会话结束...关闭测试环境...")






