#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
从Excel文件创建甘特图的简单示例
"""

from datetime import datetime, timedelta
import os
import sys

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gantt_app.core.chart import Task, GanttChart


def create_sample_gantt():
    """创建示例甘特图"""
    chart = GanttChart()
    chart.set_title("示例项目甘特图")
    
    # 创建示例任务
    base_date = datetime(2025, 5, 1)
    
    tasks = [
        Task("张三", "TASK-001", "需求分析", base_date, base_date + timedelta(days=7), 100, "#FF6B6B"),
        Task("李四", "TASK-002", "系统设计", base_date + timedelta(days=5), base_date + timedelta(days=12), 80, "#4ECDC4"),
        Task("王五", "TASK-003", "编码实现", base_date + timedelta(days=10), base_date + timedelta(days=25), 60, "#45B7D1"),
        Task("赵六", "TASK-004", "功能测试", base_date + timedelta(days=20), base_date + timedelta(days=30), 30, "#96CEB4"),
        Task("孙七", "TASK-005", "系统部署", base_date + timedelta(days=28), base_date + timedelta(days=35), 0, "#FFEAA7"),
    ]
    
    for task in tasks:
        chart.add_task(task)
    
    # 渲染甘特图
    chart.render(figsize=(14, 8))
    
    # 导出数据
    chart.export_csv("sample_gantt.csv")
    print("示例甘特图数据已导出到 sample_gantt.csv")
    
    return chart


if __name__ == "__main__":
    create_sample_gantt()