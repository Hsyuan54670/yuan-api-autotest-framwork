import allure
import pytest
import requests
import time
import logging

from common.api_utils import ApiRunner
from common.config import PUBLIC_KEY, SERVER_URL
from utils.data_utils import read_yaml
from utils.rsa_utils import PasswordEncryptor

# 配置日志记录器
logger = logging.getLogger("Hsyuan")

# 读取测试数据
data_one = read_yaml("data/test_data/login_public_key.yaml")["get_public_key"]

data_two = read_yaml("data/test_data/login.yaml")["login"]

data = data_one
class TestLoginAPI:

    @allure.epic(data["meta"]["epic"])
    @allure.feature(data["meta"]["feature"])
    @allure.story(data["meta"]["story"])
    @pytest.mark.api
    def test_get_public_key(self):

        """测试获取RSA公钥接口"""
        runner = ApiRunner(data["steps"])
        runner.run()


    @allure.epic("InvEntropy")
    @allure.feature("登录模块")
    @allure.story("登录接口")
    @pytest.mark.api
    def test_login(self):
        data = data_two
        """测试登录接口"""
        # 发送POST请求进行登录

        encryptor = PasswordEncryptor()
        public_key=read_yaml("config/extract.yaml")["publicKey"]
        pem_public_key = "-----BEGIN PUBLIC KEY-----" + public_key + "-----END PUBLIC KEY-----"
        encryptor.set_public_key(pem_public_key)

        data["steps"]["request"]["json"]["password"] = encryptor.encryptPassword(data["steps"]["request"]["json"]["password"])
        data["steps"]["request"]["json"]["timestamp"] = int(time.time() * 1000)

        runner = ApiRunner(data_two["steps"])
        runner.run()

        logger.info(f"登录成功！")