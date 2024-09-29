# main.py
import sys
import logging
from PyQt5.QtWidgets import QApplication
from search_app import SearchApp

def main():
    """
    程序主入口。
    """
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(
        filename='search_app.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()
