import pytest

from common.api_utils import ApiRunner
from utils.data_utils import read_yaml_list


@pytest.mark.ai
@pytest.mark.parametrize("data",read_yaml_list("./ai_auto_testcases/ai_testcases/test_get_admin_funds.yml"))
def test_common(data,get_admin_token):
    runner = ApiRunner(data,get_admin_token)
    runner.run()