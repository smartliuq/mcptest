 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
甘特图应用程序主窗口
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableView, QMenuBar, QAction
)
from PyQt5.QtCore import Qt

from gantt_app.core.chart import GanttChart


class MainWindow(QMainWindow):
    """甘特图应用程序主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("甘特图生成器")
        self.resize(900, 600)
        self.chart = GanttChart()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI界面"""
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 顶部工具栏
        toolbar_layout = QHBoxLayout()
        new_btn = QPushButton("新建项目")
        save_btn = QPushButton("保存项目")
        export_btn = QPushButton("导出图表")
        
        toolbar_layout.addWidget(new_btn)
        toolbar_layout.addWidget(save_btn)
        toolbar_layout.addWidget(export_btn)
        toolbar_layout.addStretch(1)
        
        # 内容区域
        content_layout = QHBoxLayout()
        
        # 左侧任务面板
        task_panel = QWidget()
        task_layout = QVBoxLayout(task_panel)
        task_layout.addWidget(QLabel("项目任务"))
        task_table = QTableView()
        task_layout.addWidget(task_table)
        
        # 右侧图表区域
        chart_panel = QWidget()
        chart_layout = QVBoxLayout(chart_panel)
        chart_layout.addWidget(QLabel("甘特图"))
        chart_view = QWidget()
        chart_layout.addWidget(chart_view)
        
        # 设置内容比例
        content_layout.addWidget(task_panel, 1)
        content_layout.addWidget(chart_panel, 2)
        
        # 添加到主布局
        main_layout.addLayout(toolbar_layout)
        main_layout.addLayout(content_layout)
        
        # 创建菜单栏
        self._create_menu_bar()
        
        # 连接信号
        new_btn.clicked.connect(self.on_new_project)
        save_btn.clicked.connect(self.on_save_project)
        export_btn.clicked.connect(self.on_export_chart)
        
    def _create_menu_bar(self):
        """创建菜单栏"""
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        file_menu.addAction(QAction("新建", self))
        file_menu.addAction(QAction("打开", self))
        file_menu.addAction(QAction("保存", self))
        file_menu.addSeparator()
        file_menu.addAction(QAction("导出", self))
        file_menu.addSeparator()
        file_menu.addAction(QAction("退出", self))
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        edit_menu.addAction(QAction("添加任务", self))
        edit_menu.addAction(QAction("删除任务", self))
        edit_menu.addAction(QAction("编辑任务", self))
        
        # 视图菜单
        view_menu = menu_bar.addMenu("视图")
        view_menu.addAction(QAction("缩放适应", self))
        view_menu.addAction(QAction("放大", self))
        view_menu.addAction(QAction("缩小", self))
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        help_menu.addAction(QAction("使用帮助", self))
        help_menu.addAction(QAction("关于", self))
    
    def on_new_project(self):
        """创建新项目"""
        pass
    
    def on_save_project(self):
        """保存项目"""
        pass
    
    def on_export_chart(self):
        """导出图表"""
        pass