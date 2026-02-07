import allure
import pytest
import requests
import time
import logging

from common.config import PUBLIC_KEY, SERVER_URL
from utils.rsa_utils import PasswordEncryptor

# 配置日志记录器
logger = logging.getLogger("Hsyuan")

@allure.epic("InvEntropy")
@allure.feature("登录模块")
@allure.story("获取RSA公钥")
@pytest.mark.api
def test_get_public_key():
    """测试获取RSA公钥接口"""
    # 发送GET请求获取公钥
    resp = requests.request("GET", SERVER_URL+"/login/auth/publicKey")
    # 断言响应状态码和内容
    assert resp.status_code == 200
    assert resp.json()["code"] == 200
    assert resp.json()["msg"] == "success"
    assert 'data' in resp.json()
    assert 'publicKey' in resp.json()['data']
    assert 'timestamp' in resp.json()['data']
    assert 'algorithm' in resp.json()['data']
    assert resp.json()['data']['algorithm'] == 'RSA'
    # 提取公钥和时间戳
    public_key = resp.json()['data']['publicKey']

@allure.epic("InvEntropy")
@allure.feature("登录模块")
@allure.story("登录接口")
@pytest.mark.api
def test_login():
    """测试登录接口"""
    # 发送POST请求进行登录
    username = 'admin'
    password = "123456"
    user_type = "admin"
    entrytor = PasswordEncryptor()
    pem_public_key = "-----BEGIN PUBLIC KEY-----"+PUBLIC_KEY+"-----END PUBLIC KEY-----"
    entrytor.set_public_key(pem_public_key)
    try:
        password_rsa = entrytor.encryptPassword(password)
    except Exception as e:
        print("加密失败：", str(e))
        return
    params = {
        "username": username,
        "password": password_rsa,
        "userType": user_type,
        "timestamp": int(time.time() * 1000)
    }



    resp = requests.request("POST", SERVER_URL+"/login", json=params)

    # 断言响应状态码和内容
    assert resp.status_code == 200
    assert resp.json()["code"] == 200
    assert resp.json()["msg"] == "success"
    assert resp.json()["data"]["userType"] == user_type
    assert "token" in resp.json()["data"]
    logger.info(f"登录成功！")