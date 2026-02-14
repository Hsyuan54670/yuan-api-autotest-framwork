import os
import yaml
import requests
from openai import OpenAI
from requests.exceptions import RequestException, JSONDecodeError
from urllib.parse import unquote

from common.config import API_KEY, AI_URL

# 配置
TEMPLATE_FILE = "template.yaml"
PROMPT_FILE = "prompt.md"
OUTPUT_DIR = "ai_testcases"
# Swagger配置
SWAGGER_URL = "http://localhost:8080/v3/api-docs"
REQUEST_TIMEOUT = 30
# 过滤配置：只生成指定请求方法的接口，空列表=不限制
ALLOW_METHODS = ["get", "post", "put", "delete", "patch"]
# 排除配置：跳过指定路径的接口（支持前缀匹配）
EXCLUDE_PATH_PREFIX = ["/actuator", "/error", "/favicon.ico"]

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 预加载系统提示词，只读取一次
with open(PROMPT_FILE, "r", encoding="utf-8") as f:
    system_prompt = f.read()

# 初始化AI客户端
client = OpenAI(api_key=API_KEY, base_url=AI_URL)


def fetch_swagger_doc(swagger_url: str) -> dict:
    """拉取Swagger/OpenAPI接口文档原始JSON数据"""
    print(f"正在拉取接口文档：{swagger_url}")
    try:
        response = requests.get(swagger_url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        swagger_json = response.json()
        print(f"✅ 接口文档拉取成功，文档版本：{swagger_json.get('openapi', swagger_json.get('swagger', '未知'))}")
        print(f"📌 总接口数量：{len(swagger_json.get('paths', {}))} 个")
        return swagger_json
    except RequestException as e:
        raise RuntimeError(f"接口文档拉取失败！请检查服务是否启动、URL是否正确：{str(e)}") from e
    except JSONDecodeError as e:
        raise RuntimeError(f"接口文档解析失败！URL返回的不是合法JSON格式：{str(e)}") from e


def parse_swagger_paths(swagger_doc: dict) -> list:
    """
    解析OpenAPI文档，拆分单个接口信息
    :return: 解析后的接口列表，每个元素包含单个接口的完整信息
    """
    paths = swagger_doc.get("paths", {})
    # 全局组件（请求/响应模型，用于AI理解字段含义）
    components = swagger_doc.get("components", {})
    api_list = []

    for path, path_info in paths.items():
        # 跳过排除的接口路径
        if any(path.startswith(prefix) for prefix in EXCLUDE_PATH_PREFIX):
            print(f"⏭️  跳过排除接口：{path}")
            continue

        # 遍历接口的请求方法（GET/POST/PUT等）
        for method, api_info in path_info.items():
            # 过滤不支持的请求方法
            if ALLOW_METHODS and method.lower() not in ALLOW_METHODS:
                continue

            # 解析接口基础信息
            api_name = api_info.get("summary", api_info.get("operationId", f"{method}_{path.replace('/', '_')}"))
            # 清理文件名非法字符
            file_name = f"test_{method.lower()}{unquote(path).replace('/', '_').replace('{', '').replace('}', '')}.yml"

            # 组装单个接口的完整文档，给AI用
            single_api_doc = {
                "接口名称": api_name,
                "接口地址": path,
                "请求方法": method.upper(),
                "接口描述": api_info.get("description", "无"),
                "请求参数": api_info.get("parameters", []),
                "请求体": api_info.get("requestBody", {}),
                "响应参数": api_info.get("responses", {}),
                "全局数据模型": components
            }

            api_list.append({
                "api_name": api_name,
                "file_name": file_name,
                "api_doc": single_api_doc
            })
            print(f"📦 解析接口：{method.upper()} {path} -> {api_name}")

    print(f"✅ 接口解析完成，共 {len(api_list)} 个有效接口待生成")
    return api_list


def generate_yaml(api_info):
    """单个接口生成YAML用例"""
    # 把接口文档转为YAML字符串，提升AI解析准确率
    api_doc_str = yaml.dump(api_info, allow_unicode=True, sort_keys=False)

    response = client.chat.completions.create(
        model="qwen-plus-latest",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"接口文档：{api_doc_str}\n请直接返回可用的YAML用例"}
        ],
        stream=True,
        top_p=0.8,
        temperature=0.7,
        extra_body={
            "enable_thinking": True,
            "thinking_budget": 6000
        }
    )
    reasoning_content = ""
    answer_content = ""
    is_answering = False
    print("\n" + "=" * 20 + f"生成用例：{api_info.get('接口名称', '未知接口')}" + "=" * 20)

    for chunk in response:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
            if not is_answering:
                print(delta.reasoning_content, end="", flush=True)
            reasoning_content += delta.reasoning_content

        if hasattr(delta, "content") and delta.content:
            if not is_answering:
                print("\n" + "=" * 20 + "用例内容" + "=" * 20)
                is_answering = True
            print(delta.content, end="", flush=True)
            answer_content += delta.content

    return answer_content.strip()


def save_yaml(content, filename):
    """保存单个接口的YAML用例文件"""
    path = os.path.join(OUTPUT_DIR, filename)
    # 简单校验YAML格式合法性
    try:
        yaml.safe_load(content)
    except yaml.YAMLError as e:
        print(f"\n❌ 生成的YAML格式非法，文件：{filename}，错误：{e}")
        # 即使格式异常也保存文件，方便人工修正
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n✅ 用例生成成功：{path}")


if __name__ == "__main__":
    try:
        # 1. 拉取Swagger接口文档
        swagger_doc = fetch_swagger_doc(SWAGGER_URL)
        # 2. 解析拆分单个接口
        api_list = parse_swagger_paths(swagger_doc)
        if not api_list:
            print("❌ 未解析到有效接口，程序退出")
            exit(0)
        # 3. 批量生成用例
        success_count = 0
        for index, api in enumerate(api_list, 1):
            print(f"\n==================== 进度：{index}/{len(api_list)} ====================")
            try:
                yaml_content = generate_yaml(api["api_doc"])
                if yaml_content:
                    save_yaml(yaml_content, api["file_name"])
                    success_count += 1
                else:
                    print(f"\n❌ 接口 {api['api_name']} 生成内容为空，跳过")
            except Exception as e:
                print(f"\n❌ 接口 {api['api_name']} 生成失败：{str(e)}")
                continue

        print(f"\n🎉 全部执行完成！成功生成 {success_count}/{len(api_list)} 个接口用例")
        print(f"📂 用例保存目录：{os.path.abspath(OUTPUT_DIR)}")

    except Exception as e:
        print(f"\n❌ 程序执行失败：{str(e)}")