#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
控制台版 JSON 转 YAML 工具
功能：从控制台输入 JSON 内容，直接输出转换后的 YAML 内容
"""

import json
import yaml
import sys


def json_to_yaml_console():
    """控制台交互：输入JSON，输出YAML"""
    print("=" * 50)
    print("📝 请输入 JSON 内容（输入完成后按 Ctrl+D 确认，Windows 按 Ctrl+Z+回车）")
    print("💡 提示：可以直接粘贴多行 JSON 内容")
    print("=" * 50)

    # 读取控制台输入的所有内容（支持多行JSON）
    try:
        # 读取stdin所有输入（兼容单行/多行JSON）
        json_input = sys.stdin.read()
        if not json_input.strip():
            raise ValueError("未输入任何JSON内容")

        # 解析JSON为Python数据结构
        json_data = json.loads(json_input)

        # 转换为YAML并输出
        print("\n✅ JSON 转换为 YAML 结果：")
        print("-" * 50)
        yaml_output = yaml.dump(
            json_data,
            default_flow_style=False,  # 块格式，更易读
            sort_keys=False,  # 保留JSON原有的键顺序
            allow_unicode=True,  # 支持中文等Unicode字符
            indent=2  # 缩进2个空格
        )
        print(yaml_output)

    except json.JSONDecodeError as e:
        print(f"\n❌ JSON 格式错误：{e}")
        print("💡 请检查JSON语法是否正确（比如引号、逗号、花括号/方括号是否配对）")
    except Exception as e:
        print(f"\n❌ 转换失败：{str(e)}")


if __name__ == "__main__":
    # 直接执行控制台交互逻辑
    json_to_yaml_console()