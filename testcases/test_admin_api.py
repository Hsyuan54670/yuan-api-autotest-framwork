import allure
import pytest
import requests
import os

from common.config import SERVER_URL

@allure.epic("InvEntropy")
@allure.feature("管理员模块")
@allure.story("获取项目审批列表接口")
@pytest.mark.api
def test_get_projects_approval_list():
    TOKEN = os.environ["TOKEN"]
    headers = {
        "Token": TOKEN
    }
    resp = requests.request("GET", SERVER_URL+"/admin/projectsApprovalList",
                            headers=headers,
                            params={"page": 1, "size": 5}
                            )
    assert resp.status_code == 200
    assert resp.json()["code"] == 200
    assert resp.json()["msg"] == "success"
    assert 'data' in resp.json()
    assert 'records' in resp.json()['data']