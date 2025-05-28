#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
甘特图核心实现 - 改进版
"""

import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import matplotlib.font_manager as fm
import platform
import os
from typing import List, Optional, Union, Dict, Any

# 配置中文字体
def configure_chinese_font() -> None:
    """根据不同的操作系统配置合适的中文字体"""
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
    """任务类，表示甘特图中的单个任务"""
    
    def __init__(self, 
                assignTo: str,
                artfid: str,
                description: str, 
                start_date: datetime.datetime, 
                end_date: datetime.datetime, 
                progress: float = 0, 
                color: Optional[str] = None,
                dependencies: Optional[List[str]] = None):
        """
        初始化任务
        
        参数:
            assignTo (str): 任务负责人
            artfid (str): 任务ID
            description (str): 任务描述
            start_date (datetime): 开始日期
            end_date (datetime): 结束日期
            progress (float): 完成百分比 (0-100)
            color (str): 任务颜色
            dependencies (List[str]): 依赖的任务ID列表
        
        异常:
            ValueError: 如果结束日期早于开始日期
        """
        # 验证日期
        if end_date < start_date:
            raise ValueError("结束日期不能早于开始日期")
            
        # 验证进度
        if progress < 0 or progress > 100:
            raise ValueError("进度必须在0-100之间")
            
        self.assignTo = assignTo
        self.artfId = artfid
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.progress = progress
        self.color = color or '#4287f5'
        self.subtasks = []
        self.dependencies = dependencies or []
    
    def add_subtask(self, task: 'Task') -> None:
        """
        添加子任务
        
        参数:
            task (Task): 要添加的子任务对象
        """
        self.subtasks.append(task)
        
    def duration(self) -> int:
        """
        获取任务持续时间（天）
        
        返回:
            int: 任务持续的天数，如果同一天完成则返回1
        """
        days = (self.end_date - self.start_date).days
        # 至少持续1天，即使同一天开始和结束
        return max(1, days)
    
    def __repr__(self) -> str:
        """任务的字符串表示"""
        return f"Task({self.description}, {self.start_date.strftime('%Y-%m-%d')}, {self.end_date.strftime('%Y-%m-%d')}, {self.progress}%)"


class GanttChart:
    """甘特图类，用于管理任务并生成甘特图"""
    
    def __init__(self):
        """初始化甘特图对象"""
        self.tasks: List[Task] = []
        self.title: str = "项目甘特图"
    
    def add_task(self, task: Task) -> None:
        """
        添加任务到甘特图
        
        参数:
            task (Task): 要添加的任务对象
        """
        self.tasks.append(task)
    
    def set_title(self, title: str) -> None:
        """
        设置甘特图标题
        
        参数:
            title (str): 甘特图标题
        """
        self.title = title
    
    def render(self, figsize: tuple = (12, 8), save_path: Optional[str] = None) -> Optional[plt.Figure]:
        """
        渲染甘特图
        
        参数:
            figsize (tuple): 图表尺寸
            save_path (str): 保存路径，如果为None则显示图表
            
        返回:
            Optional[plt.Figure]: 如果渲染成功则返回Figure对象，否则返回None
        """
        if not self.tasks:
            print("没有任务可以渲染")
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
                             datetime.timedelta(days=duration_days),
                             0.8,
                             edgecolor='black',
                             facecolor=task.color,
                             alpha=0.8)
            ax.add_patch(task_bar)
            
            # 绘制进度
            if task.progress > 0:
                progress_width = datetime.timedelta(days=duration_days * (task.progress / 100))
                progress_bar = Rectangle((task.start_date, y_pos - 0.4),
                                     progress_width,
                                     0.8,
                                     facecolor='#50C878',
                                     alpha=0.6)
                ax.add_patch(progress_bar)
            
            # 添加任务标签
            y_ticks.append(y_pos)
            y_labels.append(f"{task.assignTo}-{task.artfId}")
            
            # 添加日期标签
            ax.text(task.start_date, y_pos + 0.2,
                   task.start_date.strftime('%Y-%m-%d'),
                   ha='left', va='bottom',
                   fontsize=8)
            ax.text(task.end_date, y_pos + 0.2,
                   task.end_date.strftime('%Y-%m-%d'),
                   ha='right', va='bottom',
                   fontsize=8)
            
            # 添加描述文本
            ax.text(task.start_date + datetime.timedelta(days=0.5), y_pos,
                  task.description,
                  ha='left', va='center',
                  fontsize=8)
        
        # 设置y轴
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        
        # 格式化x轴日期
        plt.gcf().autofmt_xdate()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"甘特图已保存到 {save_path}")
        else:
            plt.tight_layout()
            plt.show()
        
        return fig
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        将甘特图数据转换为Pandas DataFrame
        
        返回:
            pd.DataFrame: 包含所有任务信息的数据框
        """
        data = []
        for task in self.tasks:
            data.append({
                'AssignTo': task.assignTo,
                'ArtifactID': task.artfId,
                'Description': task.description,
                'Start': task.start_date,
                'End': task.end_date,
                'Duration': task.duration(),
                'Progress': task.progress,
                'Dependencies': ','.join(task.dependencies) if task.dependencies else ''
            })
        return pd.DataFrame(data)
    
    def export_csv(self, filepath: str) -> None:
        """
        导出为CSV文件
        
        参数:
            filepath (str): 导出的文件路径
        """
        df = self.to_dataframe()
        df.to_csv(filepath, index=False)
        print(f"数据已导出到 {filepath}")
        
    def export_excel(self, filepath: str) -> None:
        """
        导出为Excel文件
        
        参数:
            filepath (str): 导出的文件路径
        """
        df = self.to_dataframe()
        df.to_excel(filepath, index=False)
        print(f"数据已导出到 {filepath}")
    
    def load_from_csv(self, filepath: str) -> 'GanttChart':
        """
        从CSV文件加载任务
        
        参数:
            filepath (str): CSV文件路径
            
        返回:
            GanttChart: 返回自身实例以支持链式调用
            
        异常:
            FileNotFoundError: 如果文件不存在
            ValueError: 如果文件格式不正确
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
            
        try:
            df = pd.read_csv(filepath)
            self.tasks = []
            
            for _, row in df.iterrows():
                start_date = pd.to_datetime(row['Start']).to_pydatetime()
                end_date = pd.to_datetime(row['End']).to_pydatetime()
                
                # 处理依赖关系
                dependencies = []
                if 'Dependencies' in row and pd.notna(row['Dependencies']) and row['Dependencies']:
                    dependencies = row['Dependencies'].split(',')
                
                task = Task(
                    assignTo=row.get('AssignTo', '未分配'),
                    artfid=row.get('ArtifactID', 'ID-0000'),
                    description=row.get('Description', '无描述'),
                    start_date=start_date,
                    end_date=end_date,
                    progress=row.get('Progress', 0),
                    dependencies=dependencies
                )
                self.add_task(task)
            
            return self
            
        except Exception as e:
            raise ValueError(f"加载CSV文件时出错: {str(e)}")
    
    def load_from_excel(self, filepath: str, sheet_name: str = 0) -> 'GanttChart':
        """
        从Excel文件加载任务
        
        参数:
            filepath (str): Excel文件路径
            sheet_name (str): 工作表名称或索引
            
        返回:
            GanttChart: 返回自身实例以支持链式调用
            
        异常:
            FileNotFoundError: 如果文件不存在
            ValueError: 如果文件格式不正确
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"文件不存在: {filepath}")
            
        try:
            df = pd.read_excel(filepath, sheet_name=sheet_name)
            self.tasks = []
            
            # 尝试识别列名
            column_mapping = self._identify_columns(df)
            
            for _, row in df.iterrows():
                # 跳过审核状态的任务
                if 'Status' in column_mapping and pd.notna(row[column_mapping['Status']]):
                    status = row[column_mapping['Status']]
                    if status == "Reviewed":
                        continue
                
                # 获取必要的字段
                try:
                    description = row[column_mapping.get('Description', df.columns[0])]
                    
                    if 'StartDate' in column_mapping and pd.notna(row[column_mapping['StartDate']]):
                        start_date = pd.to_datetime(row[column_mapping['StartDate']]).to_pydatetime()
                    else:
                        start_date = datetime.datetime.now()
                    
                    if 'EndDate' in column_mapping and pd.notna(row[column_mapping['EndDate']]):
                        end_date = pd.to_datetime(row[column_mapping['EndDate']]).to_pydatetime()
                    else:
                        end_date = start_date + datetime.timedelta(days=7)
                    
                    assignTo = row[column_mapping.get('AssignTo', '未分配')] if 'AssignTo' in column_mapping else '未分配'
                    artfid = row[column_mapping.get('ArtifactID', 'ID-0000')] if 'ArtifactID' in column_mapping else f"ID-{len(self.tasks)+1:04d}"
                    
                    task = Task(
                        assignTo=str(assignTo) if pd.notna(assignTo) else '未分配',
                        artfid=str(artfid) if pd.notna(artfid) else f"ID-{len(self.tasks)+1:04d}",
                        description=str(description) if pd.notna(description) else f"任务 {len(self.tasks)+1}",
                        start_date=start_date,
                        end_date=end_date,
                        progress=0
                    )
                    self.add_task(task)
                    
                except Exception as e:
                    print(f"处理任务时出错: {str(e)}")
                    continue
            
            return self
            
        except Exception as e:
            raise ValueError(f"加载Excel文件时出错: {str(e)}")
    
    def _identify_columns(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        智能识别DataFrame中的列名
        
        参数:
            df (pd.DataFrame): 数据框
            
        返回:
            Dict[str, str]: 标准列名到实际列名的映射
        """
        column_mapping = {}
        
        for col in df.columns:
            col_lower = str(col).lower()
            
            # 任务名称/描述
            if any(keyword in col_lower for keyword in ['任务', '标题', 'title', 'task', 'name', 'description']):
                column_mapping['Description'] = col
            
            # 负责人
            elif any(keyword in col_lower for keyword in ['负责', '分配', 'owner', 'assign', 'person']):
                column_mapping['AssignTo'] = col
            
            # 开始日期
            elif ('开始' in col_lower or 'start' in col_lower) and not 'actual' in col_lower:
                column_mapping['StartDate'] = col
            
            # 结束日期
            elif ('结束' in col_lower or 'end' in col_lower or 'due' in col_lower) and not 'actual' in col_lower:
                column_mapping['EndDate'] = col
            
            # 任务ID
            elif any(keyword in col_lower for keyword in ['id', '工件', 'artifact', 'artfid']):
                column_mapping['ArtifactID'] = col
            
            # 状态
            elif any(keyword in col_lower for keyword in ['状态', 'status', 'state']):
                column_mapping['Status'] = col
            
            # 进度
            elif any(keyword in col_lower for keyword in ['进度', 'progress', 'complete']):
                column_mapping['Progress'] = col
        
        return column_mapping