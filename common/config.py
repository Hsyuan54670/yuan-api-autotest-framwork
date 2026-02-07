from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

PUBLIC_KEYS=os.getenv("PUBLIC_KEYS")
SERVER_URL=os.getenv("SERVER_URL")


