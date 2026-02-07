import pytest
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()


# 启动测试
pytest.main()

# 生成测试报告
os.system("allure generate -o report -c temps")