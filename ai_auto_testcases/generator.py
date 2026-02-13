import os
import yaml
from openai import OpenAI

from common.config import API_KEY, AI_URL

# 配置
TEMPLATE_FILE = "template.yaml"
PROMPT_FILE = "prompt.md"
OUTPUT_DIR = "ai_testcases"


# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    system_prompt = f.read()

# 初始化AI客户端
client = OpenAI(api_key=API_KEY, base_url=AI_URL)


def generate_yaml(api_info):
    # 调用AI
    response = client.chat.completions.create(
        model="qwen-plus-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"接口文档：{api_info}\n请直接返回可用的YAML用例"}
        ],
        stream=True,
        top_p=0.8,  # 核采样参数，控制生成内容的多样性，0.8 为适中值，兼顾生成内容的稳定性和灵活性
        temperature=0.7,  # 温度系数，控制模型创造力，0.7 为平衡值，既保证用例符合接口规范，又能覆盖不同的测试场景
        extra_body={
            "enable_thinking": True,
            "thinking_budget": 6000
        }
    )
    reasoning_content = ""  # Complete reasoning process
    answer_content = ""  # Complete response
    is_answering = False  # Whether entering the response phase
    print("=" * 20 + "Thinking Process" + "=" * 20)

    for chunk in response:
        if not chunk.choices:
            print("Usage:")
            print(chunk.usage)
            continue

        delta = chunk.choices[0].delta

        # Only collect reasoning content
        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
            if not is_answering:
                print(delta.reasoning_content, end="", flush=True)
            reasoning_content += delta.reasoning_content

        # Received content, starting to respond
        if hasattr(delta, "content") and delta.content:
            if not is_answering:
                print("=" * 20 + "Complete Response" + "=" * 20)
                is_answering = True
            print(delta.content, end="", flush=True)
            answer_content += delta.content

    return answer_content.strip()


def save_yaml(content, filename):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ 生成成功：{path}")


if __name__ == "__main__":
    # 在这里粘贴你的接口文档 | 可自定义文档形式，并且自定义相应的处理方式让ai更好地理解接口信息
    api_doc = """
    接口名称：用户登录接口
    接口地址：/login
    请求方法：POST
    请求头：Content-Type: application/json
    请求参数：
        username: 字符串，必填，用户名
        password: 字符串，必填，密码
    响应参数：
        code: 整数，200表示成功，401表示账号密码错误
        msg: 字符串，响应消息
        data: 对象，包含token字段，登录成功返回
    """

    # 生成
    yaml_content = generate_yaml(api_doc)
    save_yaml(yaml_content, "test_login.yml")