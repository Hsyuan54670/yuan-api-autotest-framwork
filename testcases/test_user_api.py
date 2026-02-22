import pytest
from common.api_utils import ApiRunner

from utils.data_utils import read_yaml_list, get_testcases


@pytest.mark.usefixtures("get_user_token")
class TestUserAPI:

    @pytest.mark.parametrize("data", get_testcases("data/ai_testcases/user"))
    @pytest.mark.api
    @pytest.mark.final
    def test_get_projects_approval_list(self, data,get_user_token):

        runner = ApiRunner(data,get_user_token)
        runner.run()