import pytest
from common.api_utils import ApiRunner

from utils.data_utils import read_yaml_list


@pytest.mark.usefixtures("get_admin_token")
class TestAdminAPI:

    @pytest.mark.parametrize("data", read_yaml_list("data/test_data/admin_get_projects_approval_list.yaml"))
    @pytest.mark.api
    def test_get_projects_approval_list(self, data,get_admin_token):

        runner = ApiRunner(data,get_admin_token)
        runner.run()