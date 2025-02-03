# search_app.py
import sys
import logging
import os

from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox, QTableWidgetItem,
    QDialog, QScrollArea, QVBoxLayout, QLabel
)
from PyQt5.QtCore import Qt, QUrl, QThreadPool, QSettings
from PyQt5.QtGui import QIcon, QDesktopServices

from worker import Worker
from gui_components import GuiLogHandler
from utils import save_results_to_txt, generate_txt_content
from language_manager import LanguageManager  # 引入语言管理器

# 从新的 UI 文件中导入 init_ui 函数
from search_app_ui import init_ui


class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        # 初始化必要的属性
        self.language_manager = LanguageManager()
        self.worker = None
        self.saved_file = None
        self.all_results = []
        self.current_content = ""
        
        # 调用拆分到 search_app_ui.py 的界面初始化
        init_ui(self)
        # 设置日志处理器
        self.setup_logging()
        # 加载之前保存的设置
        self.load_settings()

    def setup_logging(self):
        """
        配置日志，将日志写入 GUI 文本控件。
        """
        gui_handler = GuiLogHandler(self.log_text)
        gui_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        gui_handler.setFormatter(formatter)
        logging.getLogger().addHandler(gui_handler)
        logging.getLogger().setLevel(logging.DEBUG)

    def load_settings(self):
        """
        加载之前保存的设置（窗口位置、大小、搜索引擎、搜索数量、进阶模式和语言）
        """
        settings = QSettings("MyCompany", "OnlineGPT")  # 修改处：去掉版本号
        geometry = settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        # 恢复搜索引擎设置，默认 Bing
        engine = settings.value("engine", "Bing")
        self.engine_combo.setCurrentText(engine)
        # 恢复搜索结果数量设置，默认 5
        result_num = settings.value("result_num", 5, type=int)
        self.result_num_value = result_num
        self.result_num_display.setText(str(result_num))
        # 恢复进阶模式状态
        advanced_mode = settings.value("advanced_mode", False, type=bool)
        self.advanced_mode_checkbox.setChecked(advanced_mode)
        # 恢复语言设置
        language = settings.value("language", "zh")
        self.language_manager.set_language(language)
        self.update_ui_texts()

    def save_settings(self):
        """
        保存当前设置（窗口位置、大小、搜索引擎、搜索数量、进阶模式和语言）
        """
        settings = QSettings("MyCompany", "OnlineGPT")  # 修改处：去掉版本号
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("engine", self.engine_combo.currentText())
        settings.setValue("result_num", self.result_num_value)
        settings.setValue("advanced_mode", self.advanced_mode_checkbox.isChecked())
        settings.setValue("language", self.language_manager.current_language)

    def show_about_dialog(self):
        """
        显示关于对话框（支持鼠标滚动查看长内容）。
        """
        about_title = self.language_manager.tr('about_title')
        about_message = self.language_manager.tr('about_message')

        dialog = QDialog(self)
        dialog.setWindowTitle(about_title)
        layout = QVBoxLayout(dialog)

        scroll_area = QScrollArea(dialog)
        scroll_area.setWidgetResizable(True)
        content = QLabel(about_message)
        content.setWordWrap(True)
        content.setTextFormat(Qt.RichText)
        scroll_area.setWidget(content)

        layout.addWidget(scroll_area)
        dialog.resize(600, 400)
        dialog.exec_()

    def change_language(self, language_code):
        if language_code in ['en', 'zh']:
            if language_code == self.language_manager.current_language:
                return
            self.language_manager.set_language(language_code)
            logging.info(f"语言更改为: {'English' if language_code == 'en' else '中文'}")
            self.update_ui_texts()
        else:
            logging.warning(f"尝试设置未知语言: {language_code}")

    def update_ui_texts(self):
        """
        更新界面所有文本以适应当前语言。
        """
        self.setWindowTitle(self.language_manager.tr('window_title'))
        if hasattr(self, 'language_menu'):
            self.language_menu.setTitle("Language" if self.language_manager.current_language == 'en' else "语言")
            self.language_menu.actions()[0].setText("English" if self.language_manager.current_language == 'en' else "英文")
            self.language_menu.actions()[1].setText("Chinese" if self.language_manager.current_language == 'en' else "中文")
        if hasattr(self, 'help_menu'):
            self.help_menu.setTitle(self.language_manager.tr('help'))
            self.help_menu.actions()[0].setText(self.language_manager.tr('about'))

        search_group = self.findChild(QWidget, "search_group")
        if search_group:
            search_group.setTitle(self.language_manager.tr('search_settings'))

        self.advanced_mode_checkbox.setText(self.language_manager.tr('advanced_mode'))
        self.advanced_mode_checkbox.setToolTip(self.language_manager.tr('advanced_mode'))

        self.engine_label.setText(self.language_manager.tr('search_engine'))
        self.engine_combo.setToolTip(self.language_manager.tr('search_engine'))

        self.result_num_label.setText(self.language_manager.tr('search_number'))

        self.decrement_button.setText(self.language_manager.tr('decrement'))
        self.decrement_button.setToolTip(self.language_manager.tr('decrement'))
        self.increment_button.setText(self.language_manager.tr('increment'))
        self.increment_button.setToolTip(self.language_manager.tr('increment'))
        self.copy_button.setToolTip(self.language_manager.tr('copy'))
        self.clear_button.setToolTip(self.language_manager.tr('clear'))
        self.search_button.setText(self.language_manager.tr('search'))
        self.search_button.setToolTip(self.language_manager.tr('search'))
        self.interrupt_button.setText(self.language_manager.tr('interrupt'))
        self.interrupt_button.setToolTip(self.language_manager.tr('interrupt'))
        self.save_button.setText(self.language_manager.tr('save_results'))
        self.save_button.setToolTip(self.language_manager.tr('save_results'))
        self.open_button.setText(self.language_manager.tr('open_results'))
        self.open_button.setToolTip(self.language_manager.tr('open_results'))

        self.search_label.setText(self.language_manager.tr('search_keywords'))
        if self.advanced_mode_checkbox.isChecked():
            self.search_input_advanced.setPlaceholderText(self.language_manager.tr('search_placeholder_advanced'))
            self.search_input_advanced.setToolTip(self.language_manager.tr('search_keywords'))
        else:
            self.search_input.setPlaceholderText(self.language_manager.tr('search_placeholder'))
            self.search_input.setToolTip(self.language_manager.tr('search_keywords'))

        self.question_label.setText(self.language_manager.tr('custom_question'))
        self.question_input.setPlaceholderText(self.language_manager.tr('question_placeholder'))
        self.question_input.setToolTip(self.language_manager.tr('custom_question'))

        self.status_label.setText(self.language_manager.tr('status_waiting'))

        self.result_table.setHorizontalHeaderLabels([
            self.language_manager.tr('copy'),
            self.language_manager.tr('url'),
            self.language_manager.tr('title'),
            self.language_manager.tr('snippet'),
            self.language_manager.tr('content')
        ])

        log_group = self.findChild(QWidget, "log_group")
        if log_group:
            log_group.setTitle("Logs" if self.language_manager.current_language == 'en' else "日志")

    def set_ui_enabled(self, enabled: bool):
        """
        统一启用或禁用界面控件，便于在搜索过程中统一设置状态。
        """
        self.search_input.setEnabled(enabled)
        self.search_input_advanced.setEnabled(enabled)
        self.question_input.setEnabled(enabled)
        self.increment_button.setEnabled(enabled)
        self.decrement_button.setEnabled(enabled)
        self.engine_combo.setEnabled(enabled)
        self.search_button.setEnabled(enabled)
        self.open_button.setEnabled(enabled and self.saved_file is not None)
        self.save_button.setEnabled(enabled and bool(self.all_results))
        self.copy_button.setEnabled(enabled and bool(self.all_results))
        self.interrupt_button.setEnabled(not enabled)

    def on_advanced_mode_changed(self, state):
        is_advanced = (state == Qt.Checked)
        logging.info(f"进阶模式 {'开启' if is_advanced else '关闭'}")
        if is_advanced:
            self.search_input.setVisible(False)
            self.search_input_advanced.setVisible(True)
            self.question_label.setVisible(True)
            self.question_input.setVisible(True)
            self.search_input_advanced.setFocus()
        else:
            self.search_input.setVisible(True)
            self.search_input_advanced.setVisible(False)
            self.question_label.setVisible(False)
            self.question_input.setVisible(False)
            self.search_input.setFocus()

    def on_increment(self):
        if self.result_num_value < 20:
            self.result_num_value += 1
            self.result_num_display.setText(str(self.result_num_value))
            logging.info(f"搜索数量增加到 {self.result_num_value}")

    def on_decrement(self):
        if self.result_num_value > 1:
            self.result_num_value -= 1
            self.result_num_display.setText(str(self.result_num_value))
            logging.info(f"搜索数量减少到 {self.result_num_value}")

    def on_clear_click(self):
        if self.advanced_mode_checkbox.isChecked():
            self.search_input_advanced.clear()
        else:
            self.search_input.clear()
        logging.info("已清空搜索关键词输入框。")

    def on_search_click(self):
        is_advanced = self.advanced_mode_checkbox.isChecked()
        if is_advanced:
            keywords_text = self.search_input_advanced.toPlainText().strip()
            if not keywords_text:
                QMessageBox.warning(self, self.language_manager.tr('input_error'),
                                    self.language_manager.tr('input_error_empty_keyword'))
                logging.warning("空关键词搜索（进阶模式）。")
                return
            queries = [line.strip() for line in keywords_text.splitlines() if line.strip()]
            if not queries:
                QMessageBox.warning(self, self.language_manager.tr('input_error'),
                                    self.language_manager.tr('input_error_empty_keyword'))
                logging.warning("空关键词搜索（进阶模式）。")
                return
            custom_question = self.question_input.toPlainText().strip()
            if not custom_question:
                QMessageBox.warning(self, self.language_manager.tr('input_error'),
                                    self.language_manager.tr('input_error_empty_question'))
                logging.warning("进阶模式下无自定义问题输入。")
                return
        else:
            query = self.search_input.text().strip()
            if not query:
                QMessageBox.warning(self, self.language_manager.tr('input_error'),
                                    self.language_manager.tr('input_error_empty_keyword'))
                logging.warning("空关键词搜索。")
                return
            queries = [query]
            custom_question = None

        num_results = self.result_num_value
        engine_display = self.engine_combo.currentText()
        engine = self.engines.get(engine_display, 'Bing')
        logging.info(f"开始搜索，关键词: {queries}, 数量: {num_results}, 引擎: {engine}")

        self.set_ui_enabled(False)
        self.status_label.setText(self.language_manager.tr('status_searching'))
        self.progress_bar.setVisible(True)
        self.result_table.setRowCount(0)

        self.worker = Worker(queries, num_results, engine, custom_question)
        self.worker.signals.finished.connect(self.on_search_complete)
        self.worker.signals.error.connect(self.on_search_error)
        QThreadPool.globalInstance().start(self.worker)

    def on_interrupt_click(self):
        if self.worker and self.worker.is_running:
            logging.info("用户中断搜索任务。")
            self.worker.stop()
            self.interrupt_button.setEnabled(False)
            self.status_label.setText(self.language_manager.tr('interrupt_info_task_interrupted'))
            self.set_ui_enabled(True)
        else:
            logging.warning("无正在运行的搜索任务可中断。")
            QMessageBox.information(self, self.language_manager.tr('input_error'),
                                    self.language_manager.tr('interrupt_info_no_task'))

    def on_search_complete(self, results, filename):
        self.progress_bar.setVisible(False)
        if results:
            try:
                self.saved_file = filename
                self.all_results = results
                logging.info("搜索结果已成功获取。")
            except Exception as e:
                logging.error(f"保存文件时出错：{e}")
                QMessageBox.critical(self, self.language_manager.tr('save_failure'),
                                     f"{self.language_manager.tr('save_failure').format(e)}")
                self.status_label.setText(self.language_manager.tr('status_search_failed'))
                self.set_ui_enabled(True)
                return

            self.result_table.setRowCount(0)
            for idx, result in enumerate(results):
                self.result_table.insertRow(idx)
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Checked)

                url_item = QTableWidgetItem(result['link'])
                title_item = QTableWidgetItem(result['title'])
                snippet_item = QTableWidgetItem(result['snippet'])
                content_item = QTableWidgetItem(result['content'])

                self.result_table.setItem(idx, 0, checkbox_item)
                self.result_table.setItem(idx, 1, url_item)
                self.result_table.setItem(idx, 2, title_item)
                self.result_table.setItem(idx, 3, snippet_item)
                self.result_table.setItem(idx, 4, content_item)

            self.result_table.itemChanged.connect(self.on_checkbox_state_changed)
            self.update_saved_content()

            self.status_label.setText(self.language_manager.tr('status_search_complete'))
            self.set_ui_enabled(True)

            if self.advanced_mode_checkbox.isChecked():
                self.search_input_advanced.setFocus()
            else:
                self.search_input.setFocus()

            logging.info("搜索完成，结果已展示。")
            self.copy_results_silently()

        else:
            self.result_table.setRowCount(0)
            self.status_label.setText(self.language_manager.tr('status_search_failed'))
            QMessageBox.information(self, self.language_manager.tr('input_error'),
                                    self.language_manager.tr('status_search_failed'))
            logging.info("搜索完成但无结果。")
            self.set_ui_enabled(True)

    def on_search_error(self, error_message):
        self.progress_bar.setVisible(False)
        self.result_table.setRowCount(0)
        self.status_label.setText(self.language_manager.tr('status_search_failed'))
        QMessageBox.critical(self, self.language_manager.tr('input_error'),
                             f"{self.language_manager.tr('status_search_failed')}\n{error_message}")
        logging.error(f"搜索错误：{error_message}")
        self.set_ui_enabled(True)

    def on_save_click(self):
        is_advanced = self.advanced_mode_checkbox.isChecked()
        if is_advanced:
            queries = [line.strip() for line in self.search_input_advanced.toPlainText().strip().splitlines() if line.strip()]
            custom_question = self.question_input.toPlainText().strip()
        else:
            query = self.search_input.text().strip()
            queries = [query]
            custom_question = None

        if not queries:
            QMessageBox.warning(self, self.language_manager.tr('input_error'),
                                self.language_manager.tr('save_error_no_keyword'))
            logging.warning("试图保存结果但无关键词。")
            return

        from PyQt5.QtWidgets import QFileDialog
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        default_filename = os.path.join(downloads_path, "search_results.txt")
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            self.language_manager.tr('save_results'),
            default_filename,
            "Text Files (*.txt);;All Files (*)",
            options=options
        )
        if filename:
            logging.info(f"用户选择保存文件路径：{filename}")
            try:
                selected_results = self.get_selected_results()
                save_results_to_txt(
                    selected_results,
                    ', '.join(queries),
                    filename=filename,
                    engine=self.engine_combo.currentText(),
                    custom_question=custom_question,
                    language=self.language_manager.current_language
                )

                QMessageBox.information(self, self.language_manager.tr('save_success').format(filename),
                                        self.language_manager.tr('save_success').format(filename))
                logging.info(f"结果成功保存到 {filename}")
                self.saved_file = filename
                self.open_button.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, self.language_manager.tr('save_failure'),
                                     f"{self.language_manager.tr('save_failure').format(e)}")
                logging.error(f"保存文件时出错：{e}")

    def on_open_click(self):
        if self.saved_file and os.path.exists(self.saved_file):
            logging.info(f"打开文件：{self.saved_file}")
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.saved_file))
        else:
            QMessageBox.warning(self, self.language_manager.tr('input_error'),
                                self.language_manager.tr('open_error_no_file'))
            logging.warning("尝试打开文件但不存在或未保存。")

    def on_copy_click(self):
        selected_results = self.get_selected_results()
        if selected_results:
            is_advanced = self.advanced_mode_checkbox.isChecked()
            if is_advanced:
                queries = [line.strip() for line in self.search_input_advanced.toPlainText().strip().splitlines() if line.strip()]
                custom_question = self.question_input.toPlainText().strip()
            else:
                query = self.search_input.text().strip()
                queries = [query]
                custom_question = None

            try:
                content = generate_txt_content(
                    selected_results,
                    ', '.join(queries),
                    engine=self.engine_combo.currentText(),
                    custom_question=custom_question,
                    language=self.language_manager.current_language
                )
                clipboard = QApplication.clipboard()
                clipboard.setText(content)
                logging.info("选中内容已复制到剪贴板。")
                QMessageBox.information(self, self.language_manager.tr('copy_success'),
                                        self.language_manager.tr('copy_success'))
            except Exception as e:
                QMessageBox.warning(self, self.language_manager.tr('copy_failure').format(e),
                                    self.language_manager.tr('copy_failure').format(e))
                logging.error(f"复制出错：{e}")
        else:
            QMessageBox.warning(self, self.language_manager.tr('copy_failure_no_selection'),
                                self.language_manager.tr('copy_failure_no_selection'))
            logging.warning("尝试复制但无选择内容。")

    def copy_results_silently(self):
        selected_results = self.get_selected_results()
        if selected_results:
            is_advanced = self.advanced_mode_checkbox.isChecked()
            if is_advanced:
                queries = [line.strip() for line in self.search_input_advanced.toPlainText().strip().splitlines() if line.strip()]
                custom_question = self.question_input.toPlainText().strip()
            else:
                query = self.search_input.text().strip()
                queries = [query]
                custom_question = None

            try:
                content = generate_txt_content(
                    selected_results,
                    ', '.join(queries),
                    engine=self.engine_combo.currentText(),
                    custom_question=custom_question,
                    language=self.language_manager.current_language
                )
                clipboard = QApplication.clipboard()
                clipboard.setText(content)
                logging.info("选中内容已自动复制到剪贴板。")
            except Exception as e:
                logging.error(f"自动复制出错：{e}")
        else:
            logging.warning("自动复制时无选择内容。")

    def on_result_cell_clicked(self, row, column):
        if column == 1:  # URL列
            item = self.result_table.item(row, column)
            if item:
                url = item.text()
                logging.info(f"点击URL：{url}")
                QDesktopServices.openUrl(QUrl(url))
            else:
                logging.warning("点击的URL单元格为空。")

    def on_checkbox_state_changed(self, item):
        if item.column() == 0:
            self.update_saved_content()
            all_checked = True
            for row in range(self.result_table.rowCount()):
                checkbox_item = self.result_table.item(row, 0)
                if checkbox_item is None or checkbox_item.checkState() != Qt.Checked:
                    all_checked = False
                    break
            self.checkbox_header.isOn = all_checked
            self.checkbox_header.updateSection(0)

    def on_header_checkbox_clicked(self, checked):
        for row in range(self.result_table.rowCount()):
            checkbox_item = self.result_table.item(row, 0)
            if checkbox_item is not None:
                checkbox_item.setCheckState(Qt.Checked if checked else Qt.Unchecked)

    def get_selected_results(self):
        selected_results = []
        for row in range(self.result_table.rowCount()):
            checkbox_item = self.result_table.item(row, 0)
            if checkbox_item is not None and checkbox_item.checkState() == Qt.Checked:
                title_item = self.result_table.item(row, 2)
                link_item = self.result_table.item(row, 1)
                snippet_item = self.result_table.item(row, 3)
                content_item = self.result_table.item(row, 4)
                if title_item and link_item and snippet_item and content_item:
                    result = {
                        'title': title_item.text(),
                        'link': link_item.text(),
                        'snippet': snippet_item.text(),
                        'content': content_item.text(),
                        'engine': self.engine_combo.currentText()
                    }
                    selected_results.append(result)
                else:
                    logging.warning(f"行 {row} 存在空数据项。")
        return selected_results

    def update_saved_content(self):
        selected_results = self.get_selected_results()
        is_advanced = self.advanced_mode_checkbox.isChecked()
        if is_advanced:
            queries = [line.strip() for line in self.search_input_advanced.toPlainText().strip().splitlines() if line.strip()]
            custom_question = self.question_input.toPlainText().strip()
        else:
            query = self.search_input.text().strip()
            queries = [query]
            custom_question = None

        try:
            content = generate_txt_content(
                selected_results,
                ', '.join(queries),
                engine=self.engine_combo.currentText(),
                custom_question=custom_question,
                language=self.language_manager.current_language
            )
            self.current_content = content
        except Exception as e:
            logging.error(f"更新内容时出错：{e}")

    def closeEvent(self, event):
        if self.worker and self.worker.is_running:
            self.worker.stop()
        self.save_settings()  # 保存当前设置
        event.accept()


if __name__ == "__main__":
    logging.basicConfig(
        filename='search_app.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    app = QApplication(sys.argv)
    window = SearchApp()
    window.show()
    sys.exit(app.exec_())