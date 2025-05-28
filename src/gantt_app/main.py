 #!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
甘特图应用程序主入口
"""

import sys
from PyQt5.QtWidgets import QApplication
from gantt_app.ui.main_window import MainWindow


def main():
    """应用程序主函数"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()