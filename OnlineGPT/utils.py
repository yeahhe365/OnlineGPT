# utils.py
import re
import logging
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import charset_normalizer

def clean_text(text):
    """
    清洗文本，移除控制字符和非打印字符。
    """
    return re.sub(r'[\x00-\x1F\x7F]', '', text)

def get_page_content(url, worker=None):
    """
    获取指定URL页面的所有文本内容，处理编码并过滤非HTML内容，同时尽量保留原网页的文本格式。
    支持中断功能：使用流式下载数据，并在每个块读取时检测 worker 的中断标志。
    """
    if worker and not worker.is_running:
        logging.info(f"中断获取页面内容：{url}")
        return "任务已中断，无法获取内容"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/113.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    try:
        # 使用 stream=True 以便分块读取数据
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            logging.warning(f"非HTML内容，跳过: {url}，Content-Type: {content_type}")
            return "非HTML内容，无法提取"

        chunks = []
        # 以 1KB 为单位读取响应数据，并在每个块时检查中断标志
        for chunk in response.iter_content(chunk_size=1024):
            if worker and not worker.is_running:
                logging.info(f"中断获取页面内容：{url}")
                response.close()
                return "任务已中断，无法获取内容"
            chunks.append(chunk)
        content_bytes = b''.join(chunks)

        detected = charset_normalizer.from_bytes(content_bytes).best()
        encoding = detected.encoding if detected and detected.encoding else 'utf-8'
        text = content_bytes.decode(encoding, errors='replace')
        logging.info(f"检测到编码: {encoding}，URL: {url}")
    except requests.RequestException as e:
        logging.error(f"获取页面内容失败 ({url}): {e}")
        return "无法获取内容"
    except Exception as e:
        logging.error(f"解码页面内容失败 ({url}): {e}")
        return "无法提取内容"

    soup = BeautifulSoup(text, 'html.parser')

    # 尝试优先提取 <article> 标签内的内容
    article = soup.find('article')
    if article:
        extracted_text = '\n\n'.join([
            p.get_text(separator='\n', strip=True)
            for p in article.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
        ])
    else:
        paragraphs = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
        extracted_text = '\n\n'.join([
            p.get_text(separator='\n', strip=True) for p in paragraphs
        ])

    extracted_text = clean_text(extracted_text)
    if len(extracted_text) < 200:
        logging.debug(f"提取内容过短 ({len(extracted_text)} 字符), 使用备用方法。")
        extracted_text = '\n\n'.join([
            p.get_text(separator='\n', strip=True)
            for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'])
        ])
        extracted_text = clean_text(extracted_text)

    return extracted_text if extracted_text else "无法提取内容"

def generate_txt_content(all_results, query, engine='Google', custom_question=None, language='zh'):
    """
    生成要保存或复制的文本内容，仅包含选中的结果。
    根据语言生成不同的指令内容。
    """
    try:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if language == 'en':
            content = (
                "Ignore all previous instructions. You are a knowledgeable and helpful person that can answer any questions. Your task is to answer the following question delimited by triple backticks. Please answer in English.\n\n"
                "Question:\n"
                "```\n"
            )
            if custom_question:
                content += f"{custom_question}\n"
            else:
                content += f"{query}\n"
            content += "```\n\n"
            content += "It's possible that the question, or just a portion of it, requires relevant information from the internet to give a satisfactory answer. The relevant search results provided below, delimited by triple quotes, are the necessary information already obtained from the internet. The search results set the context for addressing the question, so you don't need to access the internet to answer the question.\n\n"
            content += "Write a comprehensive answer to the question in the best way you can. If necessary, use the provided search results.\n\n"
            content += f"For your reference, today's date is {current_datetime}.\n\n"
            content += "---\n\n"
            content += "If you use any of the search results in your answer, always cite the sources at the end of the corresponding line, similar to how Wikipedia.org cites information. Use the citation format [NUMBER], where both the NUMBER and URL correspond to the provided search results below, delimited by triple quotes.\n\n"
            content += "Present the answer in a clear format.\n"
            content += "Use a numbered list if it clarifies things\n"
            content += "---\n\n"
            content += "If you can't find enough information in the search results and you're not sure about the answer, try your best to give a helpful response by using all the information you have from the search results.\n\n"
        else:
            content = (
                "忽略之前的所有指示。你是一个知识渊博且乐于助人的人，可以回答任何问题。你的任务是回答以下被三个反引号分隔的问题。请用中文回答。\n\n"
                "问题：\n"
                "```\n"
            )
            if custom_question:
                content += f"{custom_question}\n"
            else:
                content += f"{query}\n"
            content += "```\n\n"
            content += "问题可能需要互联网相关的信息来给出满意的答案。下面提供的被三个引号分隔的相关搜索结果是已经从互联网获取的必要信息。这些搜索结果为回答问题提供了上下文，因此你不需要访问互联网来回答问题。\n\n"
            content += "请用你能做到的最佳方式写出对问题的全面回答。如果有必要，使用提供的搜索结果。\n\n"
            content += f"供参考，今天的日期是 {current_datetime}。\n\n"
            content += "---\n\n"
            content += "如果你在回答中使用了任何搜索结果，请始终在相应行的末尾引用来源，类似于Wikipedia.org引用信息的方式。使用引用格式[编号]，其中编号和URL对应于下面被三个引号分隔的提供的搜索结果。\n\n"
            content += "以清晰的格式呈现答案。\n"
            content += "如果有助于澄清，请使用编号列表。\n"
            content += "---\n\n"
            content += "如果你在搜索结果中找不到足够的信息，并且不确定答案，请尽力利用所有来自搜索结果的信息提供有帮助的回答。\n\n"

        content += "Search results:\n"
        content += '"""\n'
        idx = 1
        for result in all_results:
            content += f"NUMBER:{idx}\n"
            content += f"URL: {result['link']}\n"
            content += f"TITLE: {result['title']}\n"
            content += f"SNIPPET: {result['snippet']}\n"
            content += f"CONTENT: {result['content']}\n\n"
            idx += 1
        content += '"""\n'
        return content
    except Exception as e:
        logging.error(f"生成内容时出错：{e}")
        raise Exception(f"生成内容时出错：{e}")

def save_results_to_txt(all_results, query, filename=None, engine='Google', custom_question=None, language='zh'):
    """
    将搜索结果保存到文本文件中，按照指定的格式。
    默认保存到系统的“下载”文件夹。
    """
    if not filename:
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        filename = os.path.join(downloads_path, "search_results.txt")

    logging.info(f"尝试将搜索结果保存到文件: {filename}")
    try:
        content = generate_txt_content(all_results, query, engine, custom_question, language)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"搜索结果成功保存到 {filename}")
        return filename  # 返回保存的文件路径
    except Exception as e:
        logging.error(f"保存文件时出错：{e}")
        raise e