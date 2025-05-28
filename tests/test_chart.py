#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
甘特图核心模块单元测试
"""

import unittest
from datetime import datetime, timedelta
import os
import pandas as pd
import tempfile

from gantt_app.core.chart import Task, GanttChart


class TestTask(unittest.TestCase):
    """任务类测试"""
    
    def setUp(self):
        """测试前准备"""
        self.start_date = datetime.now()
        self.end_date = self.start_date + timedelta(days=5)
        self.task = Task(
            assignTo="开发者", 
            artfid="TASK-123", 
            description="测试任务",
            start_date=self.start_date,
            end_date=self.end_date,
            progress=50,
            color="#FF0000"
        )
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.task.assingto, "开发者")
        self.assertEqual(self.task.artfId, "TASK-123")
        self.assertEqual(self.task.description, "测试任务")
        self.assertEqual(self.task.start_date, self.start_date)
        self.assertEqual(self.task.end_date, self.end_date)
        self.assertEqual(self.task.progress, 50)
        self.assertEqual(self.task.color, "#FF0000")
        self.assertEqual(self.task.subtasks, [])
    
    def test_add_subtask(self):
        """测试添加子任务"""
        subtask = Task(
            assignTo="子任务负责人",
            artfid="SUB-456",
            description="子任务",
            start_date=self.start_date,
            end_date=self.end_date,
            progress=20
        )
        self.task.add_subtask(subtask)
        self.assertEqual(len(self.task.subtasks), 1)
        self.assertEqual(self.task.subtasks[0], subtask)
    
    def test_duration(self):
        """测试任务持续时间计算"""
        self.assertEqual(self.task.duration(), 5)
        
        # 测试同一天开始和结束的任务
        same_day_task = Task(
            assignTo="开发者",
            artfid="SAME-789",
            description="同一天完成的任务",
            start_date=self.start_date,
            end_date=self.start_date,
            progress=100
        )
        self.assertEqual(same_day_task.duration(), 0)
        
    def test_repr(self):
        """测试对象表示方法"""
        # 注意：当前实现存在问题，应该修复Task.__repr__方法
        # 该测试可能会失败，因为__repr__使用了self.name而不是self.description
        try:
            repr_str = repr(self.task)
            self.assertIn("测试任务", repr_str)
        except AttributeError:
            self.fail("Task.__repr__方法引用了不存在的属性")


class TestGanttChart(unittest.TestCase):
    """甘特图类测试"""
    
    def setUp(self):
        """测试前准备"""
        self.chart = GanttChart()
        self.start_date = datetime.now()
        
        # 创建测试任务
        self.task1 = Task(
            assignTo="开发者1",
            artfid="TASK-1",
            description="任务1",
            start_date=self.start_date,
            end_date=self.start_date + timedelta(days=3),
            progress=30,
            color="#FF0000"
        )
        
        self.task2 = Task(
            assignTo="开发者2",
            artfid="TASK-2", 
            description="任务2",
            start_date=self.start_date + timedelta(days=1),
            end_date=self.start_date + timedelta(days=6),
            progress=10,
            color="#00FF00"
        )
    
    def test_init(self):
        """测试初始化"""
        self.assertEqual(self.chart.tasks, [])
        self.assertEqual(self.chart.title, "项目甘特图")
    
    def test_add_task(self):
        """测试添加任务"""
        self.chart.add_task(self.task1)
        self.assertEqual(len(self.chart.tasks), 1)
        self.assertEqual(self.chart.tasks[0], self.task1)
        
        self.chart.add_task(self.task2)
        self.assertEqual(len(self.chart.tasks), 2)
    
    def test_set_title(self):
        """测试设置标题"""
        self.chart.set_title("测试甘特图")
        self.assertEqual(self.chart.title, "测试甘特图")
    
    def test_to_dataframe(self):
        """测试转换为DataFrame"""
        self.chart.add_task(self.task1)
        self.chart.add_task(self.task2)
        
        df = self.chart.to_dataframe()
        
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['AssignTo', 'ArtifactID', 'Description', 'Start', 'End', 'Duration', 'Progress'])
        self.assertEqual(df.iloc[0]['AssignTo'], "开发者1")
        self.assertEqual(df.iloc[1]['AssignTo'], "开发者2")
    
    def test_export_csv(self):
        """测试导出CSV"""
        self.chart.add_task(self.task1)
        self.chart.add_task(self.task2)
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # 导出CSV
            self.chart.export_csv(temp_path)
            
            # 验证文件存在
            self.assertTrue(os.path.exists(temp_path))
            
            # 读取并验证内容
            df = pd.read_csv(temp_path)
            self.assertEqual(len(df), 2)
            self.assertEqual(df.iloc[0]['AssignTo'], "开发者1")
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_load_from_csv(self):
        """测试从CSV加载"""
        self.chart.add_task(self.task1)
        self.chart.add_task(self.task2)
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp_file:
            temp_path = temp_file.name
        
        try:
            # 导出CSV
            self.chart.export_csv(temp_path)
            
            # 创建新图表并加载
            new_chart = GanttChart()
            new_chart.load_from_csv(temp_path)
            
            # 验证任务数量
            self.assertEqual(len(new_chart.tasks), 2)
            
            # 验证任务属性
            self.assertEqual(new_chart.tasks[0].assingto, "开发者1")
            self.assertEqual(new_chart.tasks[0].artfId, "TASK-1")
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()