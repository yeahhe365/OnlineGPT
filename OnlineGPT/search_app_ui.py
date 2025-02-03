# search_app_ui.py
import os
import sys
import logging
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QTextEdit, QVBoxLayout,
    QHBoxLayout, QMessageBox, QFileDialog, QProgressBar, QTableWidget,
    QTableWidgetItem, QGroupBox, QHeaderView, QComboBox, QCheckBox,
    QGridLayout, QSplitter, QShortcut, QAction, QMenuBar,
    QStyle, QSizePolicy
)
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QFont, QIcon, QDesktopServices, QKeySequence

from gui_components import GuiLogHandler, MyLineEdit, MyTextEdit, CheckBoxHeader, CenteredCheckBoxDelegate
from language_manager import LanguageManager
from utils import save_results_to_txt, generate_txt_content


def init_ui(self):
    """
    初始化 UI 组件。
    """
    # 定义常用字体
    label_font = QFont("微软雅黑", 12)
    input_font = QFont("微软雅黑", 12)
    button_font = QFont("微软雅黑", 10)
    status_font = QFont("微软雅黑", 10)
    table_font = QFont("微软雅黑", 10)
    log_font = QFont("Consolas", 10)

    main_layout = QVBoxLayout()
    main_layout.setContentsMargins(20, 20, 20, 20)
    main_layout.setSpacing(15)

    # 创建菜单栏
    self.menu_bar = QMenuBar(self)
    language_menu_title = "Language" if self.language_manager.current_language == 'en' else "语言"
    self.language_menu = self.menu_bar.addMenu(language_menu_title)
    english_action = QAction("English", self)
    chinese_action = QAction("中文", self)
    self.language_menu.addAction(english_action)
    self.language_menu.addAction(chinese_action)
    english_action.triggered.connect(lambda: self.change_language('en'))
    chinese_action.triggered.connect(lambda: self.change_language('zh'))

    # 帮助菜单
    help_menu_title = self.language_manager.tr('help')
    self.help_menu = self.menu_bar.addMenu(help_menu_title)
    about_action = QAction(self.language_manager.tr('about'), self)
    self.help_menu.addAction(about_action)
    about_action.triggered.connect(self.show_about_dialog)

    main_layout.setMenuBar(self.menu_bar)

    # 搜索设置分组框
    search_group = QGroupBox(self.language_manager.tr('search_settings'))
    search_group.setObjectName("search_group")
    search_layout = QGridLayout()
    search_layout.setSpacing(10)
    search_group.setLayout(search_layout)

    # 进阶模式复选框
    self.advanced_mode_checkbox = QCheckBox(self.language_manager.tr('advanced_mode'))
    self.advanced_mode_checkbox.setFont(label_font)
    self.advanced_mode_checkbox.setToolTip(self.language_manager.tr('advanced_mode'))
    self.advanced_mode_checkbox.stateChanged.connect(self.on_advanced_mode_changed)

    # 搜索引擎选择
    self.engine_label = QLabel(self.language_manager.tr('search_engine'))
    self.engine_label.setFont(label_font)
    self.engine_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    self.engine_combo = QComboBox()
    self.engine_combo.setFont(input_font)
    self.engines = {
        "Google": "Google",
        "Bing": "Bing",
        "百度": "百度"
    }
    for engine in self.engines.keys():
        self.engine_combo.addItem(engine)
    # 修改处：默认搜索引擎设为 Bing
    self.engine_combo.setCurrentText("Bing")
    self.engine_combo.setToolTip(self.language_manager.tr('search_engine'))

    # 搜索结果数量
    self.result_num_label = QLabel(self.language_manager.tr('search_number'))
    self.result_num_label.setFont(label_font)
    self.result_num_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    self.decrement_button = QPushButton(self.language_manager.tr('decrement'))
    self.decrement_button.setFont(button_font)
    self.decrement_button.setFixedWidth(30)
    self.decrement_button.setStyleSheet("""
        QPushButton {
            background-color: #ff5722;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #e64a19;
        }
        QPushButton:pressed {
            background-color: #d84315;
        }
    """)
    self.decrement_button.setToolTip(self.language_manager.tr('decrement'))
    self.decrement_button.clicked.connect(self.on_decrement)

    self.result_num_value = 5  # 默认5
    self.result_num_display = QLabel(str(self.result_num_value))
    self.result_num_display.setFont(input_font)
    self.result_num_display.setAlignment(Qt.AlignCenter)
    self.result_num_display.setFixedWidth(30)
    self.result_num_display.setStyleSheet("""
        QLabel {
            border: 1px solid #ccc;
            border-radius: 4px;
            padding: 5px;
            background-color: #f0f0f0;
        }
    """)

    self.increment_button = QPushButton(self.language_manager.tr('increment'))
    self.increment_button.setFont(button_font)
    self.increment_button.setFixedWidth(30)
    self.increment_button.setStyleSheet("""
        QPushButton {
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #43a047;
        }
        QPushButton:pressed {
            background-color: #388e3c;
        }
    """)
    self.increment_button.setToolTip(self.language_manager.tr('increment'))
    self.increment_button.clicked.connect(self.on_increment)

    result_num_layout = QHBoxLayout()
    result_num_layout.addWidget(self.decrement_button)
    result_num_layout.addWidget(self.result_num_display)
    result_num_layout.addWidget(self.increment_button)
    result_num_layout.setSpacing(5)

    self.copy_button = QPushButton("")
    self.copy_button.setFont(button_font)
    self.copy_button.setFixedWidth(40)
    self.copy_button.setStyleSheet("""
        QPushButton {
            background-color: #ff9800;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #fb8c00;
        }
        QPushButton:pressed {
            background-color: #f57c00;
        }
    """)
    self.copy_button.setToolTip(self.language_manager.tr('copy'))
    self.copy_button.clicked.connect(self.on_copy_click)
    self.copy_button.setEnabled(False)
    self.copy_button.setIcon(self.style().standardIcon(QStyle.SP_FileDialogDetailedView))

    self.clear_button = QPushButton("")
    self.clear_button.setFont(button_font)
    self.clear_button.setFixedWidth(40)
    self.clear_button.setStyleSheet("""
        QPushButton {
            background-color: #9e9e9e;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px;
        }
        QPushButton:hover {
            background-color: #757575;
        }
        QPushButton:pressed {
            background-color: #616161;
        }
    """)
    self.clear_button.setToolTip(self.language_manager.tr('clear'))
    self.clear_button.clicked.connect(self.on_clear_click)
    self.clear_button.setIcon(self.style().standardIcon(QStyle.SP_TrashIcon))

    copy_and_clear_layout = QHBoxLayout()
    copy_and_clear_layout.addWidget(self.copy_button)
    copy_and_clear_layout.addWidget(self.clear_button)
    copy_and_clear_layout.setSpacing(10)

    search_num_layout = QHBoxLayout()
    search_num_layout.addWidget(self.result_num_label)
    search_num_layout.addLayout(result_num_layout)
    search_num_layout.addLayout(copy_and_clear_layout)
    search_num_layout.setSpacing(20)

    search_layout.addWidget(self.advanced_mode_checkbox, 0, 0)
    engine_layout = QHBoxLayout()
    engine_layout.addWidget(self.engine_label)
    engine_layout.addWidget(self.engine_combo)
    engine_layout.setSpacing(5)
    search_layout.addLayout(engine_layout, 0, 1)
    search_layout.addLayout(search_num_layout, 0, 2, 1, 2)

    self.search_label = QLabel(self.language_manager.tr('search_keywords'))
    self.search_label.setFont(label_font)
    self.search_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    
    # 非进阶模式下的搜索输入框（单行），按下Enter键触发搜索
    self.search_input = MyLineEdit()
    self.search_input.setFont(input_font)
    self.search_input.setPlaceholderText(self.language_manager.tr('search_placeholder'))
    self.search_input.setToolTip(self.language_manager.tr('search_keywords'))
    self.search_input.setMinimumWidth(360)
    self.search_input.returnPressed.connect(self.on_search_click)

    self.search_input_advanced = MyTextEdit()
    self.search_input_advanced.setFont(input_font)
    self.search_input_advanced.setPlaceholderText(self.language_manager.tr('search_placeholder_advanced'))
    self.search_input_advanced.setVisible(False)
    self.search_input_advanced.setToolTip(self.language_manager.tr('search_keywords'))
    self.search_input_advanced.setMinimumWidth(360)

    self.question_label = QLabel(self.language_manager.tr('custom_question'))
    self.question_label.setFont(label_font)
    self.question_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    self.question_input = QTextEdit()
    self.question_input.setFont(input_font)
    self.question_input.setPlaceholderText(self.language_manager.tr('question_placeholder'))
    self.question_label.setVisible(False)
    self.question_input.setVisible(False)
    self.question_input.setToolTip(self.language_manager.tr('custom_question'))

    # 主要操作按钮统一设置最小高度和统一样式（仅颜色不同）
    common_button_height = "min-height: 10px;"
    # 搜索按钮
    self.search_button = QPushButton(self.language_manager.tr('search'))
    self.search_button.setFont(button_font)
    self.search_button.setMinimumWidth(90)
    self.search_button.setStyleSheet(f"""
        QPushButton {{
            background-color: #4caf50;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            {common_button_height}
        }}
        QPushButton:hover {{
            background-color: #45a049;
        }}
        QPushButton:pressed {{
            background-color: #3e8e41;
        }}
    """)
    self.search_button.setToolTip(self.language_manager.tr('search'))
    self.search_button.clicked.connect(self.on_search_click)
    self.search_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    self.search_button.setIconSize(QSize(25, 25))

    # 中断按钮
    self.interrupt_button = QPushButton(self.language_manager.tr('interrupt'))
    self.interrupt_button.setFont(button_font)
    self.interrupt_button.setMinimumWidth(90)
    self.interrupt_button.setStyleSheet(f"""
        QPushButton {{
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px 8px 5px;
            {common_button_height}
        }}
        QPushButton:hover {{
            background-color: #da190b;
        }}
        QPushButton:pressed {{
            background-color: #b71c1c;
        }}
    """)
    self.interrupt_button.setToolTip(self.language_manager.tr('interrupt'))
    self.interrupt_button.clicked.connect(self.on_interrupt_click)
    self.interrupt_button.setEnabled(False)
    self.interrupt_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
    self.interrupt_button.setIconSize(QSize(32, 32))

    # 保存按钮
    self.save_button = QPushButton(self.language_manager.tr('save_results'))
    self.save_button.setFont(button_font)
    self.save_button.setMinimumWidth(90)
    self.save_button.setStyleSheet(f"""
        QPushButton {{
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            {common_button_height}
        }}
        QPushButton:hover {{
            background-color: #1E88E5;
        }}
        QPushButton:pressed {{
            background-color: #1976D2;
        }}
    """)
    self.save_button.setToolTip(self.language_manager.tr('save_results'))
    self.save_button.clicked.connect(self.on_save_click)
    self.save_button.setEnabled(False)
    self.save_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
    self.save_button.setIconSize(QSize(32, 32))

    # 打开按钮
    self.open_button = QPushButton(self.language_manager.tr('open_results'))
    self.open_button.setFont(button_font)
    self.open_button.setMinimumWidth(90)
    self.open_button.setStyleSheet(f"""
        QPushButton {{
            background-color: #9c27b0;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 20px;
            {common_button_height}
        }}
        QPushButton:hover {{
            background-color: #8E24AA;
        }}
        QPushButton:pressed {{
            background-color: #7B1FA2;
        }}
    """)
    self.open_button.setToolTip(self.language_manager.tr('open_results'))
    self.open_button.clicked.connect(self.on_open_click)
    self.open_button.setEnabled(False)
    self.open_button.setIcon(self.style().standardIcon(QStyle.SP_DialogOpenButton))
    self.open_button.setIconSize(QSize(32, 32))

    input_layout = QHBoxLayout()
    input_layout.addWidget(self.search_input)
    input_layout.addWidget(self.search_input_advanced)
    input_layout.addStretch(1)
    button_layout = QHBoxLayout()
    button_layout.addWidget(self.search_button)
    button_layout.addWidget(self.interrupt_button)
    button_layout.addStretch()
    button_layout.addWidget(self.save_button)
    button_layout.addWidget(self.open_button)
    input_layout.addLayout(button_layout)

    search_layout.addWidget(self.search_label, 1, 0)
    search_layout.addLayout(input_layout, 1, 1, 1, 3)
    search_layout.addWidget(self.question_label, 2, 0)
    search_layout.addWidget(self.question_input, 2, 1, 1, 3)

    search_layout.setColumnStretch(0, 0)
    search_layout.setColumnStretch(1, 1)
    search_layout.setColumnStretch(2, 1)
    search_layout.setColumnStretch(3, 1)

    self.status_label = QLabel(self.language_manager.tr('status_waiting'))
    self.status_label.setFont(status_font)
    self.status_label.setAlignment(Qt.AlignLeft)
    self.status_label.setStyleSheet("color: #555;")

    self.progress_bar = QProgressBar()
    self.progress_bar.setRange(0, 0)
    self.progress_bar.setVisible(False)
    self.progress_bar.setFixedHeight(15)
    self.progress_bar.setStyleSheet("""
        QProgressBar {
            border: 1px solid #bbb;
            background-color: #eee;
            height: 15px;
            border-radius: 7px;
        }
        QProgressBar::chunk {
            background-color: #4caf50;
            border-radius: 7px;
        }
    """)

    self.result_table = QTableWidget()
    self.result_table.setColumnCount(5)
    # 修改处：使用翻译后的文本设置表头
    self.result_table.setHorizontalHeaderLabels([
        self.language_manager.tr('copy'),
        self.language_manager.tr('url'),
        self.language_manager.tr('title'),
        self.language_manager.tr('snippet'),
        self.language_manager.tr('content')
    ])

    self.checkbox_header = CheckBoxHeader()
    self.result_table.setHorizontalHeader(self.checkbox_header)
    self.checkbox_header.checkBoxClicked.connect(self.on_header_checkbox_clicked)

    self.result_table.verticalHeader().setVisible(False)
    self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.result_table.setSelectionBehavior(QTableWidget.SelectRows)
    self.result_table.setSelectionMode(QTableWidget.SingleSelection)
    self.result_table.setAlternatingRowColors(True)
    self.result_table.setFont(table_font)
    self.result_table.setStyleSheet("""
        QTableWidget {
            background-color: #fff;
            alternate-background-color: #f9f9f9;
        }
        QHeaderView::section {
            background-color: #f0f0f0;
            padding: 6px;
            border: 1px solid #d6d6d6;
            font-weight: bold;
        }
        QTableWidget::item:selected {
            background-color: #cce5ff;
        }
    """)

    self.result_table.setColumnWidth(0, 40)
    self.result_table.setColumnWidth(1, 250)
    self.result_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
    self.result_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
    for i in range(2, 5):
        self.result_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    self.result_table.setItemDelegateForColumn(0, CenteredCheckBoxDelegate())
    self.result_table.cellClicked.connect(self.on_result_cell_clicked)

    log_group = QGroupBox("日志" if self.language_manager.current_language == 'zh' else "Logs")
    log_group.setObjectName("log_group")
    log_layout = QVBoxLayout()
    self.log_text = QTextEdit()
    self.log_text.setReadOnly(True)
    self.log_text.setFont(log_font)
    self.log_text.setStyleSheet("""
        QTextEdit {
            background-color: #1e1e1e;
            color: #dcdcdc;
            border: 1px solid #555;
            border-radius: 4px;
        }
    """)
    log_layout.addWidget(self.log_text)
    log_group.setLayout(log_layout)

    splitter = QSplitter(Qt.Vertical)
    splitter.addWidget(self.result_table)
    splitter.addWidget(log_group)
    splitter.setSizes([600, 300])

    main_layout.addWidget(search_group)
    main_layout.addWidget(self.status_label)
    main_layout.addWidget(self.progress_bar)
    main_layout.addWidget(splitter)

    self.setLayout(main_layout)

    self.setWindowTitle(self.language_manager.tr('window_title'))

    # —— 图标加载部分修改如下 —— 
    # 判断打包状态，获取资源所在目录
    if getattr(sys, 'frozen', False):
        script_dir = sys._MEIPASS
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    # 先尝试在 resources 子目录中寻找 icon.png
    icon_path = os.path.join(script_dir, 'resources', 'icon.png')
    if not os.path.exists(icon_path):
        # 若未找到，则直接在 script_dir 中寻找 icon.png
        icon_path = os.path.join(script_dir, 'icon.png')
    logging.info(f"尝试加载图标路径: {icon_path}")
    if not os.path.exists(icon_path):
        logging.error(f"图标文件不存在: {icon_path}")
        QMessageBox.critical(self, "错误", f"图标文件不存在: {icon_path}")
    else:
        try:
            self.setWindowIcon(QIcon(icon_path))
            logging.info(f"已设置窗口图标: {icon_path}")
        except Exception as e:
            logging.error(f"设置窗口图标时出错: {e}")
            QMessageBox.critical(self, "错误", f"设置窗口图标时出错: {e}")