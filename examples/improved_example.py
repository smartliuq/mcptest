#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
甘特图改进版使用示例
"""

from datetime import datetime, timedelta
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 使用改进版的Task和GanttChart
from src.gantt_app.core.chart_improved import Task, GanttChart


def main():
    """示例主函数"""
    print("创建甘特图示例(改进版)")
    
    # 创建甘特图
    chart = GanttChart()
    chart.set_title("项目任务甘特图(改进版)")
    
    # Excel文件路径
    excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "data sample.xlsx")
    
    try:
        # 使用新的load_from_excel方法直接加载Excel数据
        chart.load_from_excel(excel_path)
        
        if not chart.tasks:
            print("没有从Excel读取到任务，无法创建甘特图")
            return
        
        # 打印任务信息
        print(f"成功加载了 {len(chart.tasks)} 个任务:")
        for i, task in enumerate(chart.tasks, 1):
            print(f"{i}. {task.description} ({task.start_date.strftime('%Y-%m-%d')} 至 {task.end_date.strftime('%Y-%m-%d')}), 负责人: {task.assignTo}")
        
        # 渲柔甘特图
        chart.render(figsize=(16, 8))
        
        # 导出数据
        print("\n任务数据:")
        print(chart.to_dataframe())
        
        # 导出到CSV
        output_csv = "improved_project_gantt.csv"
        chart.export_csv(output_csv)
        print(f"甘特图数据已导出到 {output_csv}")
        
        # 导出到Excel
        output_excel = "improved_project_gantt.xlsx"
        chart.export_excel(output_excel)
        print(f"甘特图数据已导出到 {output_excel}")
        
    except Exception as e:
        print(f"创建甘特图时出错: {str(e)}")


if __name__ == "__main__":
    main()