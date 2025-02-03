# worker.py
import logging
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot
from search_engines import (
    get_google_search_results,
    get_bing_search_results,
    get_baidu_search_results
)
from utils import save_results_to_txt

class WorkerSignals(QObject):
    """
    定义 Worker 的信号，finished 信号返回搜索结果和保存的文件路径，
    error 信号返回错误信息。
    """
    finished = pyqtSignal(list, str)  # 参数：结果列表、文件路径
    error = pyqtSignal(str)

class Worker(QRunnable):
    """
    使用 QRunnable 实现的工作任务，将搜索任务提交给 QThreadPool 处理。
    """
    def __init__(self, queries, num_results=5, engine='Google', custom_question=None):
        super(Worker, self).__init__()
        self.queries = queries              # 搜索关键词列表
        self.num_results = num_results      # 每个关键词的搜索结果数量
        self.engine = engine                # 搜索引擎（Google/Bing/百度）
        self.custom_question = custom_question  # 自定义问题（可选）
        self._is_running = True             # 任务运行状态标志
        self.signals = WorkerSignals()      # 创建信号对象

    @property
    def is_running(self):
        return self._is_running

    def stop(self):
        """
        停止工作任务，将运行标志设为 False。
        """
        self._is_running = False

    @pyqtSlot()
    def run(self):
        """
        执行搜索任务，遍历所有关键词调用对应搜索引擎的搜索函数，
        并利用 ThreadPoolExecutor 抓取各搜索结果页面的内容。
        最后保存结果到文本文件，并发射 finished 信号；如果出现异常则发射 error 信号。
        """
        try:
            all_results = []
            logging.info(
                f"Worker started: queries: {self.queries}, num_results: {self.num_results}, engine: {self.engine}"
            )
            for query in self.queries:
                if not self.is_running:
                    logging.info("Search task interrupted.")
                    break
                if self.engine == 'Google':
                    results = get_google_search_results(query, self.num_results, self)
                elif self.engine == 'Bing':
                    results = get_bing_search_results(query, self.num_results, self)
                elif self.engine == '百度':
                    results = get_baidu_search_results(query, self.num_results, self)
                else:
                    raise Exception("Unsupported search engine.")
                for result in results:
                    result['query'] = query
                all_results.append(results)

            if not self.is_running:
                logging.info("Search task was stopped; emitting empty results.")
                self.signals.finished.emit([], "")
                return

            # 将二维列表扁平化
            flat_results = [item for sublist in all_results for item in sublist]
            filename = save_results_to_txt(
                flat_results,
                ', '.join(self.queries),
                engine=self.engine,
                custom_question=self.custom_question
            )
            self.signals.finished.emit(flat_results, filename)
            logging.info("Worker task completed successfully.")
        except Exception as e:
            self.signals.error.emit(str(e))
            logging.error(f"Worker encountered an error: {e}")