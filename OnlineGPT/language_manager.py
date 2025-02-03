# language_manager.py
import logging
from translations import translations

class LanguageManager:
    """
    语言管理器，负责管理当前语言和提供翻译功能。
    """
    def __init__(self):
        self.current_language = 'zh'  # 默认语言为中文

    def set_language(self, language_code):
        if language_code in translations:
            self.current_language = language_code
        else:
            logging.warning(f"尝试设置未知语言: {language_code}")

    def tr(self, key):
        return translations[self.current_language].get(key, key)