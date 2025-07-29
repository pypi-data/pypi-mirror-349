import json
import pandas as pd
import itertools
from typing import List, Dict

def json_to_class(json_str, cls):
    data = json.loads(json_str)
    return cls(**data)

def df_to_markdown(df: pd.DataFrame, columns=None) -> str:
    """
    将 pandas.DataFrame 导出为 Markdown 表格字符串，可以指定导出的列名。

    参数:
    df (pd.DataFrame): 要导出的 DataFrame。
    columns (list, optional): 要导出的列名。如果为 None，则导出所有列。

    返回:
    str: Markdown 表格字符串。
    """
    if columns is not None:
        df = df[columns]

    # 构建表头
    header = '| ' + ' | '.join(df.columns) + ' |'
    separator = '| ' + ' | '.join(['---'] * len(df.columns)) + ' |'

    # 构建表格内容
    rows = []
    for index, row in df.iterrows():
        rows.append('| ' + ' | '.join(map(str, row)) + ' |')

    # 合并所有部分
    markdown_table = '\n'.join([header, separator] + rows)
    return markdown_table

def df_to_json(df: pd.DataFrame, columns=None) -> str:
    if columns is not None:
        df = df[columns]
    # 将 DataFrame 转换为 JSON 数组
    json_array = df.to_dict(orient='records')
    return json.dumps(json_array, ensure_ascii=False)

def is_empty_metrics(metrics):
    if metrics is None:
        return True
    if metrics['sharpe'] is None and metrics['fitness'] is None:
        return True
    return False

def build_alphas(template: str, params: Dict) -> List[str]:
    """
    所有可能的表达式
    :param template: 表达式模板
    :param params: 参数说明，key为对应要替换的变量，value为列表
    :return:
    """
    keys = list(params.keys())
    values = list(params.values())
    # 生成笛卡尔积
    combinations = list(itertools.product(*values))
    # 替换模板中的变量
    result = []
    for combination in combinations:
        result_dict = dict(zip(keys, combination))
        result.append(template.format(**result_dict))
    return result