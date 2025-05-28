#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
甘特图基本使用示例
"""

from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import os
import random

from gantt_app.core.chart import Task, GanttChart



def read_excel_data():
    """从Excel文件读取任务数据"""
    # Excel文件路径
    excel_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "data sample.xlsx")
    
    if not os.path.exists(excel_path):
        print(f"文件不存在: {excel_path}")
        return []
    
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_path)
        print(f"成功读取Excel文件，共 {len(df)} 条记录")
        print(f"列名: {list(df.columns)}")
        
        # 定义颜色列表用于随机分配颜色
        colors = ["#FF7F50", "#6495ED", "#8A2BE2", "#3CB371", "#FFD700", "#DC143C", 
                 "#9370DB", "#20B2AA", "#FF6347", "#4682B4"]
        
        tasks = []
        
        # 遍历Excel数据，创建任务
        for _, row in df.iterrows():
            try:
                # 确定列名
                title_col = None
                assigned_to_col = None
                start_date_col = None
                end_date_col = None
                status_col = None
                
                # 尝试查找相应的列
                for col in df.columns:
                    col_lower = col.lower()
                    if '标题' in col_lower or 'title' in col_lower or 'task' in col_lower:
                        title_col = col
                    elif 'owner' in col_lower or 'owner' in col_lower:
                        assigned_to_col = col
                    elif ('开始' in col_lower or 'start' in col_lower) and 'expect' in col_lower:
                        start_date_col = col
                    elif ('结束' in col_lower or 'end' in col_lower) and 'expect' in col_lower:
                        end_date_col = col
                    elif '状态' in col_lower or 'status' in col_lower:
                        status_col = col
                
                # 如果找不到必要的列，跳过
                if not all([title_col, start_date_col, end_date_col]):
                    print("找不到必要的列，使用以下默认列名:")
                    print("- 任务名称列: Task Name")
                    print("- 分配到列: Assigned To")
                    print("- 开始日期列: Expected Start Date")
                    print("- 结束日期列: Expected End Date")
                    print("- 状态列: Status")
                    
                    title_col = "Task Name" if "Task Name" in df.columns else df.columns[0]
                    assigned_to_col = "Owner" if "Owner" in df.columns else None
                    start_date_col = "Expected Start Date" if "Expected Start Date" in df.columns else None
                    end_date_col = "Expected End Date" if "Expected End Date" in df.columns else None
                    status_col = "Status" if "Status" in df.columns else None
                
                # 忽略"Reviewed"状态的任务
                if status_col and row[status_col] == "Reviewed":
                    continue
                
                # 获取任务名称
                task_name = str(row[title_col]) if title_col else f"任务 {len(tasks) + 1}"
                
                # 获取分配人员
                if assigned_to_col and pd.notna(row[assigned_to_col]):
                    assignee = str(row[assigned_to_col])
                else:
                    assignee = "未分配"
                
                # 获取日期
                if start_date_col and pd.notna(row[start_date_col]):
                    start = pd.to_datetime(row[start_date_col]).to_pydatetime()
                else:
                    start = datetime.now() - timedelta(days=30)
                
                if end_date_col and pd.notna(row[end_date_col]):
                    end = pd.to_datetime(row[end_date_col]).to_pydatetime()
                else:
                    end = start + timedelta(days=10)
                
                # 随机生成完成百分比和颜色
                progress = 0
                color = random.choice(colors)
                
                # 创建任务
                artfid = str(row['工件 ID']) if '工件 ID' in df.columns and pd.notna(row['工件 ID']) else "ID-" + str(random.randint(1000, 9999))
                task = Task(assignTo=assignee, artfid=artfid, description=task_name, 
                           start_date=start, end_date=end, progress=progress, color=color)
                
                tasks.append(task)
                print(f"创建任务: {task_name}, 分配给: {assignee}, 开始: {start}, 结束: {end}")
                
            except Exception as e:
                print(f"处理任务时出错: {str(e)}")
                continue
        
        # 按照assignTo属性对任务列表进行排序
        tasks.sort(key=lambda task: task.assingto)
        print(f"已按照负责人(assignTo)对任务进行排序，共{len(tasks)}个任务")
        
        return tasks
    
    except Exception as e:
        print(f"读取Excel文件时出错: {str(e)}")
        return []


def main():
    """示例主函数"""
    print("创建甘特图示例")
    
    # 创建甘特图
    chart = GanttChart()
    chart.set_title("项目任务甘特图")
    
    # 从Excel读取任务数据
    tasks = read_excel_data()
    
    if not tasks:
        print("没有从Excel读取到任务，无法创建甘特图")
        return
    
    # 添加任务到甘特图
    for task in tasks:
        chart.add_task(task)
    
    # 渲染甘特图
    chart.render(figsize=(16, 8))
    
    # 导出数据
    print(chart.to_dataframe())
    
    # 导出到CSV
    chart.export_csv("project_gantt.csv")
    print("甘特图数据已导出到 project_gantt.csv")


### for Alice to learn


if __name__ == "__main__":
    main()