# gui_components.py
import logging
from PyQt5.QtWidgets import QLineEdit, QTextEdit, QHeaderView, QStyleOptionButton, QStyledItemDelegate, QApplication
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QRect
from PyQt5.QtGui import QTextCursor, QPainter
from PyQt5.Qt import QStyle

class GuiLogHandler(logging.Handler, QObject):
    """
    自定义日志处理器，将日志写入GUI的QTextEdit控件。
    """
    log_signal = pyqtSignal(str, str)

    def __init__(self, text_edit):
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.text_edit = text_edit
        self.log_signal.connect(self.append_log)

    def emit(self, record):
        msg = self.format(record)
        # 根据日志级别设置不同的颜色
        if record.levelno == logging.ERROR:
            color = '#ff4c4c'  # 红色
        elif record.levelno == logging.WARNING:
            color = '#ffae42'  # 橙色
        elif record.levelno == logging.INFO:
            color = '#4caf50'  # 绿色
        else:
            color = '#dcdcdc'  # 默认颜色

        # 发射信号，将日志信息传递到主线程
        self.log_signal.emit(msg, color)

    def append_log(self, msg, color):
        """
        将日志消息以指定颜色添加到QTextEdit，并自动滚动到底部。
        """
        # 使用HTML格式插入带颜色的文本
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.insertHtml(f'<span style="color:{color};">{msg}</span><br>')
        self.text_edit.moveCursor(QTextCursor.End)
        self.text_edit.ensureCursorVisible()

class MyLineEdit(QLineEdit):
    """
    自定义的输入控件，增加特定的键盘事件处理。
    """
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.setCursorPosition(0)
        elif event.key() == Qt.Key_Down:
            self.setCursorPosition(len(self.text()))
        elif event.key() == Qt.Key_Delete:
            self.clear()
        else:
            super(MyLineEdit, self).keyPressEvent(event)

class MyTextEdit(QTextEdit):
    """
    自定义的文本编辑控件，增加特定的键盘事件处理。
    """
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Start)
            self.setTextCursor(cursor)
        elif event.key() == Qt.Key_Down:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
        elif event.key() == Qt.Key_Delete:
            self.clear()
        else:
            super(MyTextEdit, self).keyPressEvent(event)

class CheckBoxHeader(QHeaderView):
    """
    自定义QHeaderView，在第一列的表头添加一个复选框。
    """
    checkBoxClicked = pyqtSignal(bool)

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False
        self.setSectionsClickable(True)
        self.sectionClicked.connect(self.onSectionClicked)

    def paintSection(self, painter, rect, logicalIndex):
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        if logicalIndex == 0:
            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + 5, rect.y() + 5, 20, 20)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.isOn:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def onSectionClicked(self, logicalIndex):
        if logicalIndex == 0:
            self.isOn = not self.isOn
            self.checkBoxClicked.emit(self.isOn)
            self.updateSection(0)

class CenteredCheckBoxDelegate(QStyledItemDelegate):
    """
    自定义委托，用于在单元格中居中显示复选框。
    """
    def paint(self, painter, option, index):
        if index.column() == 0:
            # 获取复选框的状态
            checked = index.data(Qt.CheckStateRole) == Qt.Checked
            check_box_style_option = QStyleOptionButton()
            if checked:
                check_box_style_option.state |= QStyle.State_On
            else:
                check_box_style_option.state |= QStyle.State_Off
            check_box_style_option.state |= QStyle.State_Enabled

            # 计算复选框的位置，使其居中
            check_box_rect = self.getCheckBoxRect(option)
            check_box_style_option.rect = check_box_rect

            # 绘制复选框
            QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)
        else:
            super(CenteredCheckBoxDelegate, self).paint(painter, option, index)

    def getCheckBoxRect(self, option):
        # 获取复选框的尺寸
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        # 计算复选框的位置，使其居中
        x = option.rect.x() + (option.rect.width() - check_box_rect.width()) / 2
        y = option.rect.y() + (option.rect.height() - check_box_rect.height()) / 2
        return QRect(int(x), int(y), check_box_rect.width(), check_box_rect.height())
