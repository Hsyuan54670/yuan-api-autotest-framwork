import logging
import pytest
from common.api_utils import ApiRunner

from utils.allure_utils import AllureUtils
from utils.data_utils import read_yaml_list

logger = logging.getLogger("Hsyuan")
allure_utils = AllureUtils()

@pytest.mark.usefixtures("get_admin_token")
class TestAdminAPI:

    @pytest.mark.parametrize("data", read_yaml_list("data/test_data/admin_get_projects_approval_list.yaml"))
    @pytest.mark.api
    def test_get_projects_approval_list(self, data,get_admin_token):

        allure_utils.allure_load(data["allure"])

        runner = ApiRunner(get_admin_token,data["steps"],data["case_id"])
        runner.run()