#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
甘特图核心实现
"""

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.font_manager as fm
import platform

# 配置中文字体
def configure_chinese_font():
    system = platform.system()
    if system == 'Windows':
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文黑体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    elif system == 'Linux':
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'SimHei']
        plt.rcParams['axes.unicode_minus'] = False
    elif system == 'Darwin':  # macOS
        plt.rcParams['font.family'] = ['sans-serif']
        plt.rcParams['font.sans-serif'] = ['PingFang SC', 'STHeiti']
        plt.rcParams['axes.unicode_minus'] = False
    
# 应用字体配置
configure_chinese_font()


class Task:
    """任务类"""
    
    def __init__(self, assignTo,artfid,description, start_date, end_date, progress=0, color=None):
        """
        初始化任务
        
        参数:
            assignTo (str): 任务owern
            artfid:TFID
            description:任务描述
            start_date (datetime): 开始日期
            end_date (datetime): 结束日期
            progress (float): 完成百分比 (0-100)
            color (str): 任务颜色
        """
        self.assingto = assignTo
        self.artfId = artfid
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.progress = progress
        self.color = color or '#4287f5'
        self.subtasks = []
    
    def add_subtask(self, task):
        """添加子任务"""
        self.subtasks.append(task)
        
    def duration(self):
        """获取任务持续时间（天）"""
        return (self.end_date - self.start_date).days
    
    def __repr__(self):
        return f"Task({self.description}, {self.start_date}, {self.end_date}, {self.progress}%)"


class GanttChart:
    """甘特图类"""
    
    def __init__(self):
        self.tasks = []
        self.title = "项目甘特图"
    
    def add_task(self, task):
        """添加任务到甘特图"""
        self.tasks.append(task)
    
    def set_title(self, title):
        """设置甘特图标题"""
        self.title = title
    
    def render(self, figsize=(12, 8), save_path=None):
        """
        渲染甘特图
        
        参数:
            figsize (tuple): 图表尺寸
            save_path (str): 保存路径，如果为None则显示图表
        """
        if not self.tasks:
            return None
        
        fig, ax = plt.subplots(figsize=figsize)
        
        # 设置图表样式
        ax.set_title(self.title)
        ax.set_xlabel('日期')
        ax.set_ylabel('任务')
        ax.grid(True, alpha=0.3)
        
        # 获取日期范围
        start_dates = [task.start_date for task in self.tasks]
        end_dates = [task.end_date for task in self.tasks]
        min_date = min(start_dates)
        max_date = max(end_dates)
        
        # 设置x轴
        ax.set_xlim(min_date, max_date)
        
        # 使用日期格式化
        date_format = mdates.DateFormatter('%Y-%m-%d')
        ax.xaxis.set_major_formatter(date_format)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        
        # 绘制每个任务
        y_ticks = []
        y_labels = []
        for i, task in enumerate(self.tasks):
            y_pos = len(self.tasks) - i
            
            # 转换日期为数值
            start_num = mdates.date2num(task.start_date)
            duration_days = task.duration()
            
            # 绘制任务条
            task_bar = Rectangle((task.start_date, y_pos - 0.4),
                             datetime.timedelta(days=duration_days + 1),
                             0.8,
                             edgecolor='black',
                             facecolor=task.color,
                             alpha=0.8)
            ax.add_patch(task_bar)
            
            # 绘制进度
            if task.progress > 0:
                progress_width = datetime.timedelta(days=(duration_days + 1) * (task.progress / 100))
                progress_bar = Rectangle((task.start_date, y_pos - 0.4),
                                     progress_width,
                                     0.8,
                                     facecolor='#50C878',
                                     alpha=0.6)
                ax.add_patch(progress_bar)
            
            # 添加任务标签
            y_ticks.append(y_pos)
            y_labels.append(task.assingto+"-"+task.artfId)
            
            # 添加日期标签
            ax.text(task.start_date, y_pos + 0.2,
                   task.start_date.strftime('%Y-%m-%d'),
                   ha='left', va='bottom',
                   fontsize=8)
            ax.text(task.end_date, y_pos + 0.2,
                   task.end_date.strftime('%Y-%m-%d'),
                   ha='right', va='bottom',
                   fontsize=8)
        
        # 设置y轴
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        
        # 格式化x轴日期
        plt.gcf().autofmt_xdate()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.tight_layout()
            plt.show()
        
        return fig
    
    def to_dataframe(self):
        """将甘特图数据转换为Pandas DataFrame"""
        data = []
        for task in self.tasks:
            data.append({
                'AssignTo': task.assingto,
                'ArtifactID': task.artfId,
                'Description': task.description,
                'Start': task.start_date,
                'End': task.end_date,
                'Duration': task.duration(),
                'Progress': task.progress
            })
        return pd.DataFrame(data)
    
    def export_csv(self, filepath):
        """导出为CSV文件"""
        df = self.to_dataframe()
        df.to_csv(filepath, index=False)
        
    def export_excel(self, filepath):
        """导出为Excel文件"""
        df = self.to_dataframe()
        df.to_excel(filepath, index=False)
    
    def load_from_csv(self, filepath):
        """从CSV文件加载任务"""
        df = pd.read_csv(filepath)
        self.tasks = []
        
        for _, row in df.iterrows():
            start_date = pd.to_datetime(row['Start']).to_pydatetime()
            end_date = pd.to_datetime(row['End']).to_pydatetime()
            
            task = Task(
                assignTo=row.get('AssignTo', '未分配'),
                artfid=row.get('ArtifactID', 'ID-0000'),
                description=row.get('Description', '无描述'),
                start_date=start_date,
                end_date=end_date,
                progress=row.get('Progress', 0)
            )
            self.add_task(task)
        
        return self