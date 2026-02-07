import pytest
import os



# 启动测试
pytest.main()

# 生成测试报告
os.system("allure generate -o report -c temps")