# translations.py
translations = {
    'en': {
        'window_title': "OnlineGPT",  # 去掉版本号
        'search_settings': "Search Settings",
        'advanced_mode': "Advanced Mode",
        'search_engine': "Search Engine:",
        'search_number': "Number of Results:",
        'decrement': "-",
        'increment': "+",
        'copy': "Copy",
        'clear': "Clear",
        'search_keywords': "Search Keywords:",
        'search_placeholder': "e.g., What's the weather like tomorrow",
        'search_placeholder_advanced': "Enter one keyword per line, e.g.,\nWhat's the weather like tomorrow\nShanghai travel guide",
        'custom_question': "Please enter your question:",
        'question_placeholder': "Enter your question here",
        'search': "Search",
        'interrupt': "Interrupt",
        'save_results': "Save",
        'open_results': "Open",
        'status_waiting': "Waiting for input...",
        'status_searching': "Searching, please wait...",
        'status_search_complete': "Search complete, results saved and copied.",
        'status_search_failed': "Search failed.",
        'input_error': "Input Error",
        'input_error_empty_keyword': "Please enter at least one search keyword!",
        'input_error_empty_question': "Please enter a custom question!",
        'save_error_no_keyword': "No search keywords, cannot save results.",
        'save_success': "Search results have been saved to {}",
        'save_failure': "Error saving file: {}",
        'open_error_no_file': "No result file to open.",
        'copy_success': "Selected content has been copied to the clipboard.",
        'copy_failure': "Failed to copy content: {}",
        'copy_failure_no_selection': "No content selected.",
        'interrupt_info_no_task': "There is no ongoing search task to interrupt.",
        'interrupt_info_task_interrupted': "Search has been interrupted.",
        'help': "Help",
        'about': "About",
        'about_title': "About OnlineGPT",  # 去掉版本号
        'about_message': (
            "<h2>About OnlineGPT</h2>"  # 去掉版本号
            "<p>OnlineGPT is a powerful tool for searching and managing online information.</p>"
            "<h3>Usage Instructions:</h3>"
            "<ol>"
            "<li><strong>Enter Search Keywords:</strong> Input your search terms in the designated field. For advanced searches, enable Advanced Mode.</li>"
            "<li><strong>Select Search Engine:</strong> Choose your preferred search engine from the dropdown menu (Google, Bing, 百度).</li>"
            "<li><strong>Set Number of Results:</strong> Adjust the number of search results you wish to retrieve.</li>"
            "<li><strong>Start Search:</strong> Click the 'Search' button to begin the search process.</li>"
            "<li><strong>View Results:</strong> Once the search is complete, results will be displayed in the table below.</li>"
            "<li><strong>Manage Results:</strong> You can copy, save, or open the search results as needed.</li>"
            "<li><strong>Interrupt Search:</strong> If needed, you can interrupt an ongoing search by clicking the 'Interrupt' button or pressing Ctrl+C.</li>"
            "</ol>"
            "<h3>Features:</h3>"
            "<ul>"
            "<li><strong>Advanced Mode:</strong> Provides additional options for more refined searches, including custom questions.</li>"
            "<li><strong>Multiple Search Engines:</strong> Supports Google, Bing, and 百度 for diverse search needs.</li>"
            "<li><strong>Result Management:</strong> Easily copy, save, or open search results directly from the application.</li>"
            "<li><strong>Logging:</strong> View detailed logs of your search activities within the application.</li>"
            "</ul>"
            "<h3>License:</h3>"
            "<p>This project is licensed under the <a href='https://opensource.org/licenses/MIT'>MIT License</a>. "
            "You are free to use, modify, and distribute this software in accordance with the terms of the license.</p>"
            "<h3>Additional Resources:</h3>"
            "<p><strong>Open Source:</strong> "
            "<a href='https://github.com/yeahhe365/OnlineGPT'>https://github.com/yeahhe365/OnlineGPT</a></p>"
            "<p><strong>LINUXDO Forum:</strong> "
            "<a href='https://linux.do/t/topic/211975'>https://linux.do/t/topic/211975</a></p>"
        ),
        'url': "URL",
        'title': "Title",
        'snippet': "Snippet",
        'content': "Content"
    },
    'zh': {
        'window_title': "OnlineGPT",  # 去掉版本号
        'search_settings': "搜索设置",
        'advanced_mode': "进阶模式",
        'search_engine': "搜索引擎：",
        'search_number': "搜索数量：",
        'decrement': "-",
        'increment': "+",
        'copy': "复制",
        'clear': "清空",
        'search_keywords': "搜索关键词：",
        'search_placeholder': "例如：明天天气怎么样",
        'search_placeholder_advanced': "每行一个关键词，如：\n明天天气怎么样\n上海旅游攻略",
        'custom_question': "请输入问题：",
        'question_placeholder': "在此输入您的问题",
        'search': "搜索",
        'interrupt': "中断",
        'save_results': "保存",
        'open_results': "打开",
        'status_waiting': "等待输入...",
        'status_searching': "正在搜索，请稍候...",
        'status_search_complete': "搜索完成，结果已保存并已自动复制。",
        'status_search_failed': "搜索失败。",
        'input_error': "输入错误",
        'input_error_empty_keyword': "请输入至少一个搜索关键词！",
        'input_error_empty_question': "请输入自定义问题！",
        'save_error_no_keyword': "没有搜索关键词，无法保存结果。",
        'save_success': "搜索结果已保存到 {}",
        'save_failure': "保存文件时出错：{}",
        'open_error_no_file': "没有可打开的结果文件。",
        'copy_success': "已复制选中的内容到剪贴板。",
        'copy_failure': "复制内容时出错：{}",
        'copy_failure_no_selection': "未选择任何内容。",
        'interrupt_info_no_task': "当前没有正在运行的搜索任务。",
        'interrupt_info_task_interrupted': "搜索已被中断。",
        'help': "帮助",
        'about': "关于",
        'about_title': "关于 OnlineGPT",  # 去掉版本号
        'about_message': (
            "<h2>关于 OnlineGPT</h2>"  # 去掉版本号
            "<p>OnlineGPT 是一个强大的在线信息搜索和管理工具。</p>"
            "<h3>使用说明：</h3>"
            "<ol>"
            "<li><strong>输入搜索关键词：</strong> 在指定的输入框中输入您的搜索词。对于高级搜索，请启用进阶模式。</li>"
            "<li><strong>选择搜索引擎：</strong> 从下拉菜单中选择您偏好的搜索引擎（Google、Bing、百度）。</li>"
            "<li><strong>设置搜索数量：</strong> 调整您希望获取的搜索结果数量。</li>"
            "<li><strong>开始搜索：</strong> 点击“搜索”按钮开始搜索过程。</li>"
            "<li><strong>查看结果：</strong> 搜索完成后，结果将显示在下方的表格中。</li>"
            "<li><strong>管理结果：</strong> 您可以根据需要复制、保存或打开搜索结果。</li>"
            "<li><strong>中断搜索：</strong> 如有需要，您可以通过点击“中断”按钮或按下Ctrl+C来中断正在进行的搜索。</li>"
            "</ol>"
            "<h3>功能特点：</h3>"
            "<ul>"
            "<li><strong>进阶模式：</strong> 提供额外的选项以进行更精细的搜索，包括自定义问题。</li>"
            "<li><strong>多搜索引擎支持：</strong> 支持Google、Bing和百度，满足多样化的搜索需求。</li>"
            "<li><strong>结果管理：</strong> 轻松复制、保存或直接从应用程序中打开搜索结果。</li>"
            "<li><strong>日志记录：</strong> 在应用程序内查看详细的搜索活动日志。</li>"
            "</ul>"
            "<h3>License:</h3>"
            "<p>本项目采用 <a href='https://opensource.org/licenses/MIT'>MIT 许可证</a> 进行许可。您可以根据许可证的条款自由使用、修改和分发该软件。</p>"
            "<h3>额外资源：</h3>"
            "<p><strong>开源地址：</strong> "
            "<a href='https://github.com/yeahhe365/OnlineGPT'>https://github.com/yeahhe365/OnlineGPT</a></p>"
            "<p><strong>LINUXDO 论坛：</strong> "
            "<a href='https://linux.do/t/topic/211975'>https://linux.do/t/topic/211975</a></p>"
        ),
        'url': "链接",
        'title': "标题",
        'snippet': "摘要",
        'content': "内容"
    }
}