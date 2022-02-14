# -*- coding: utf-8 -*-

"""
@author: liangjr
@time: 2022/1/25 15:12
"""
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required=False, help="json文件路径")
parser.add_argument("-j", "--json", required=False, help="json格式数据")
parser.add_argument("-o", "--output", required=False, default="cmd", help="内容输出位置, 控制台输出或文件输出")
parser.add_argument("-t", "--type", required=False, default="pydantic", choices=["pydantic", "dataclass"],
                    help="model类型，pydantic或datacclass")
args = parser.parse_args()

if not args.path and not args.json:
    raise ValueError("缺失json数据")

if args.type == "pydantic":
    class_type = "class {}(BaseModel):"
    content = "from typing import *\n\nfrom pydantic import BaseModel\n\n\n"
elif args.type == "dataclass":
    class_type = "@dataclass\nclass {}:"
    content = "from typing import *\n\nfrom dataclasses import dataclass\n\n\n"
else:
    raise ValueError(f"无效model类型，<{args.type}>，pydantic或datacclass")


def separator_2_camel(s, separator="_"):
    return "".join([i.capitalize() for i in s.split(separator)])


def json_2_model(name, data: dict):
    global content
    class_text = [class_type.format(separator_2_camel(name))]
    for k, v in data.items():
        if isinstance(v, dict):
            json_2_model(k, v)
            t = separator_2_camel(k)
        elif isinstance(v, int):
            t = "int"
        elif isinstance(v, float):
            t = "float"
        elif isinstance(v, str):
            t = "str"
        elif isinstance(v, list):
            node_name = k + "_node"
            if v and isinstance(v[0], dict):
                json_2_model(node_name, v[0])
                t = f"List[{separator_2_camel(node_name)}]"
            else:
                t = "list"
        else:
            t = "Any"
        class_text.append(f"    {k}: {t}")
    content += "\n".join(class_text) + "\n\n\n"
    return


if __name__ == '__main__':
    if args.path:
        with open(args.path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = json.loads(args.json)

    json_2_model("root", json_data)

    if args.output == "cmd":
        print(content)
    else:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)

    print("完成")
