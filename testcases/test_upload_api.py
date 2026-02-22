import pytest
import os

from common.config import SERVER_URL
from utils.data_utils import get_testcases
from common.api_utils import ApiRunner

@pytest.mark.usefixtures("get_user_token")
class TestUploadAPI:

    @pytest.mark.final
    @pytest.mark.file
    @pytest.mark.api
    @pytest.mark.parametrize("data", get_testcases("data/ai_testcases/file"))
    def test_upload_file_success(self,data, get_user_token):
        runner = ApiRunner(data, get_user_token)
        runner.run()
