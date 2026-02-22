import copy

import pytest
import time

from common.api_utils import ApiRunner
from common.config import PUBLIC_KEY
from utils.allure_utils import AllureUtils
from utils.data_utils import read_yaml, read_yaml_list
from utils.rsa_utils import PasswordEncryptor


allure_utils = AllureUtils()

class TestLoginAPI:

    @pytest.mark.api
    @pytest.mark.parametrize("data", read_yaml_list("data/test_data/login_public_key.yaml"))
    @pytest.mark.final
    def test_get_public_key(self,data):
        """测试获取RSA公钥接口"""
        runner = ApiRunner(data)
        runner.run()


    @pytest.mark.login
    @pytest.mark.parametrize("data", read_yaml_list("data/ai_testcases/login/test_post_login.yml"))
    @pytest.mark.final
    def test_login(self,data):
        """测试登录接口"""

        test_data = copy.deepcopy(data)
        encryptor = PasswordEncryptor()
        # public_key=read_yaml("config/extract.yaml")["publicKey"]
        public_key = PUBLIC_KEY
        pem_public_key = "-----BEGIN PUBLIC KEY-----" + public_key + "-----END PUBLIC KEY-----"
        encryptor.set_public_key(pem_public_key)

        test_data["steps"]["request"]["json"]["password"] = encryptor.encryptPassword(test_data["steps"]["request"]["json"]["password"])
        test_data["steps"]["request"]["json"]["timestamp"] = int(time.time() * 1000)

        runner = ApiRunner(test_data)
        runner.run()





