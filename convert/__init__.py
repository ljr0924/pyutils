# -*- coding: utf-8 -*-

"""
@author: liangjr
@time: 2021/11/19 11:11
"""

from collections import defaultdict


def generate_tree(sources, keep_pid=False, pid_field_name="parent_id"):
    """
    无限级分类 平铺结构转状树结构
    [{"id": 1, "parent_id":0, **extra_data}, {"id": 2, "parent_id":1, **extra_data}]
     =>
    [{"id": 1, **extra_data, "list": [{"id": 2, **extra_data}]}]
    :param sources:   [{"id": 1, "parent_id":0, **extra_data}, {"id": 2, "parent_id":1, **extra_data}]
    :param keep_pid:  是否保留父id
    :param pid_field_name: 父id字段名称，默认为parent_id
    :return: [{"id": 1, **extra_data, "list": [{"id": 2, **extra_data}]}]
    """

    pid_2_source = defaultdict(list)
    for source in sources:
        pid_2_source[source[pid_field_name]].append(source)

    def _recursion(parent_id):
        tree = []
        for item in pid_2_source[parent_id]:
            data = dict(**item)
            child_list = _recursion(item["id"])
            if not keep_pid:
                del data[pid_field_name]
            if child_list:
                data["list"] = child_list
            tree.append(data)
        return tree

    return _recursion(0)


if __name__ == '__main__':
    s = [{"id": 1, "parent_id": 0, "name": "111"}, {"id": 2, "parent_id": 1, "name": "222"}]
    print(generate_tree(sources=s))
