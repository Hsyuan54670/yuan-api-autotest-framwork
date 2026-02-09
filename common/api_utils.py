import logging
import jsonpath
import requests
import re
from common.config import SERVER_URL
from common.response_checker import ResponseChecker
from utils.allure_utils import AllureUtils
from utils.data_utils import extract_yaml

logger = logging.getLogger("Hsyuan")


class ApiRunner:

    resp = None
    allure_utils = AllureUtils()
    def __init__(self,data,session=requests.Session()):
        self.session = session
        self.steps = data["steps"]
        self.allure = data["allure"]

    def send_request(self,**kwargs):
        try:
            kwargs["url"] = SERVER_URL + kwargs.get("url", "")
            response = self.session.request(**kwargs)
            response.raise_for_status()  # 检查HTTP错误
            return response
        except requests.RequestException as e:
            logger.info(f"请求失败: {e}")
            return None

    def check_response(self,expected=None):
        checker = ResponseChecker(self.resp)
        checker.check_response(expected)


    def extract(self,var_name,var_exp):
        try:
            self.resp.json = self.resp.json()
        except Exception:
            self.resp.json = {}
        value = jsonpath.jsonpath(self.resp.json,var_exp)
        if value:
            logger.info(f'提取变量成功: {var_name} = {value[0]}')
            extract_yaml(var_name,value[0])
            return value[0]
        else:
            logger.info(f'提取变量失败: {var_name}，表达式: {var_exp}')
            return None



    def core(self,k,v):
        match k:
            case 'request':
                logger.info('1.正在发送请求')
                logger.info(f'{v}')
                self.resp=self.send_request(**v)
            case 'expected':
                logger.info('2.正在断言响应')
                logger.info(f'{v}')
                self.check_response(v)
            case 'extract':
                logger.info('3.正在提取变量')
                if self.resp is not None:
                    for var_name,var_exp in v.items():
                        self.extract(var_name,var_exp)
                else:
                    logger.info('无法提取变量，因为请求失败，没有响应对象。')

    def run(self):
        self.allure_utils.allure_load(self.allure)
        start =self.allure["title"].center(120,"=")
        logger.info(start)
        for k,v in self.steps.items():
            self.core(k,v)


