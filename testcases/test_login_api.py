import pytest
import requests
import time
import logging

from common.api_utils import ApiRunner
from utils.allure_utils import AllureUtils
from utils.data_utils import read_yaml, read_yaml_list
from utils.rsa_utils import PasswordEncryptor

# 配置日志记录器
logger = logging.getLogger("Hsyuan")

allure_utils = AllureUtils()

class TestLoginAPI:

    @pytest.mark.parametrize("data", read_yaml_list("data/test_data/login_public_key.yaml"))
    def test_get_public_key(self,data):
        """测试获取RSA公钥接口"""

        allure_utils.allure_load(data["allure"])
        runner = ApiRunner(requests.Session(),data["steps"],data["case_id"])
        runner.run()

    @pytest.mark.api
    @pytest.mark.parametrize("data", read_yaml_list("data/test_data/login.yaml"))
    def test_login(self,data):
        """测试登录接口"""

        allure_utils.allure_load(data["allure"])

        encryptor = PasswordEncryptor()
        public_key=read_yaml("config/extract.yaml")["publicKey"]
        pem_public_key = "-----BEGIN PUBLIC KEY-----" + public_key + "-----END PUBLIC KEY-----"
        encryptor.set_public_key(pem_public_key)

        data["steps"]["request"]["json"]["password"] = encryptor.encryptPassword(data["steps"]["request"]["json"]["password"])
        data["steps"]["request"]["json"]["timestamp"] = int(time.time() * 1000)

        runner = ApiRunner(requests.Session(),data["steps"],data["case_id"])
        runner.run()




if __name__ == "__main__":
    TestLoginAPI.test_get_public_key()
