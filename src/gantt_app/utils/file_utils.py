 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件操作工具函数
"""

import os
import json
import pickle
from datetime import datetime


def ensure_dir(directory):
    """确保目录存在，如果不存在则创建"""
    if not os.path.exists(directory):
        os.makedirs(directory)


def save_project(project_data, filepath):
    """
    保存项目数据到文件
    
    参数:
        project_data (dict): 项目数据字典
        filepath (str): 文件保存路径
    """
    ensure_dir(os.path.dirname(filepath))
    
    # 转换日期为字符串
    serializable_data = {}
    for key, value in project_data.items():
        if isinstance(value, dict):
            serializable_data[key] = {k: v.isoformat() if isinstance(v, datetime) else v 
                                     for k, v in value.items()}
        else:
            serializable_data[key] = value.isoformat() if isinstance(value, datetime) else value
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(serializable_data, f, ensure_ascii=False, indent=2)


def load_project(filepath):
    """
    从文件加载项目数据
    
    参数:
        filepath (str): 文件路径
    
    返回:
        dict: 项目数据字典
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 转换日期字符串为datetime对象
    for key, value in data.items():
        if isinstance(value, dict):
            for k, v in value.items():
                try:
                    if isinstance(v, str) and 'T' in v:
                        data[key][k] = datetime.fromisoformat(v)
                except ValueError:
                    pass
    
    return data


def get_recent_files(directory, max_count=5):
    """
    获取目录中最近修改的文件
    
    参数:
        directory (str): 目录路径
        max_count (int): 最大文件数量
    
    返回:
        list: 最近文件路径列表
    """
    if not os.path.exists(directory):
        return []
    
    files = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            files.append((filepath, os.path.getmtime(filepath)))
    
    # 按修改时间排序
    sorted_files = sorted(files, key=lambda x: x[1], reverse=True)
    return [f[0] for f in sorted_files[:max_count]]