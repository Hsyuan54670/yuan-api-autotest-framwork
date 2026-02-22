import pytest
from common.api_utils import ApiRunner

from utils.data_utils import read_yaml_list, get_testcases


@pytest.mark.usefixtures("get_admin_token")
class TestAdminAPI:

    @pytest.mark.parametrize("data", get_testcases("data/ai_testcases/admin"))
    @pytest.mark.api
    @pytest.mark.final
    def test_get_projects_approval_list(self, data,get_admin_token):

        runner = ApiRunner(data,get_admin_token)
        runner.run()