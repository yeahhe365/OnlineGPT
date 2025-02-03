# search_engines.py
import logging
import urllib.parse
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from utils import get_page_content
import charset_normalizer

# 使用全局 session 复用 TCP 连接
session = requests.Session()
session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
})


def get_google_search_results(query, num_results=5, worker=None, retries=3):
    """
    获取 Google 搜索结果，并抓取每个结果页面的内容。
    遇到 HTTP 429 错误时，在重试等待期间不断检查中断标志，以便及时退出。
    """
    query_encoded = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={query_encoded}&num={num_results}"
    logging.info(f"发送请求到Google URL: {url}")
    
    attempt = 0
    while attempt < retries:
        # 检查中断标志，若已中断则直接返回空结果
        if worker and not worker.is_running:
            logging.info("任务中断，停止Google搜索重试。")
            return []
        try:
            response = session.get(url, timeout=10)
            if response.status_code == 429:
                wait_time = random.uniform(5, 10)
                logging.warning(f"收到429错误，等待 {wait_time:.2f} 秒后重试... (尝试 {attempt+1}/{retries})")
                # 分段等待，并在等待过程中检查中断
                slept = 0.0
                increment = 0.5
                while slept < wait_time:
                    if worker and not worker.is_running:
                        logging.info("任务中断，在等待429重试期间。")
                        return []
                    time.sleep(increment)
                    slept += increment
                attempt += 1
                continue
            response.raise_for_status()
            break  # 请求成功，退出重试循环
        except Exception as e:
            attempt += 1
            logging.error(f"请求或解码Google搜索结果失败（尝试 {attempt}/{retries}）：{e}")
            if attempt >= retries:
                raise Exception(f"请求或解码Google搜索结果失败：{e}")
    else:
        raise Exception("多次重试后仍然失败，可能被Google封禁。")
    
    # 再次检测中断状态
    if worker and not worker.is_running:
        logging.info("任务中断，停止处理Google搜索结果。")
        return []
    
    content_type = response.headers.get('Content-Type', '')
    if 'text/html' not in content_type:
        logging.error(f"搜索结果页面非HTML内容: {url}，Content-Type: {content_type}")
        raise Exception("搜索结果页面非HTML内容")
    
    detected = charset_normalizer.from_bytes(response.content).best()
    encoding = detected.encoding if detected and detected.encoding else 'utf-8'
    try:
        text = response.content.decode(encoding, errors='replace')
        logging.info(f"检测到编码: {encoding}，Google搜索结果页面URL: {url}")
    except Exception as e:
        logging.error(f"解码失败：{e}")
        raise Exception(f"解码失败：{e}")

    soup = BeautifulSoup(text, 'html.parser')
    results = []

    for g in soup.find_all('div', class_='tF2Cxc'):
        title_tag = g.find('h3')
        title = title_tag.get_text(separator=' ', strip=True) if title_tag else "No title"

        link_tag = g.find('a')
        link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "No link"

        snippet = ""
        for cls in ['VwiC3b', 'IsZvec', 'aCOpRe']:
            snippet_tag = g.find('div', class_=cls)
            if snippet_tag:
                snippet = snippet_tag.get_text(separator=' ', strip=True)
                break
        if not snippet:
            snippet_tag = g.find('span', class_='aCOpRe')
            if snippet_tag:
                snippet = snippet_tag.get_text(separator=' ', strip=True)
        if not snippet:
            snippet = "No content"

        if snippet == "No content":
            logging.debug("未能提取到Google摘要内容，尝试其他方法。")

        results.append({
            'title': title,
            'link': link,
            'snippet': snippet,
            'content': "正在获取内容...",
            'engine': 'Google'
        })

        if len(results) >= num_results:
            break

    logging.info(f"解析出 {len(results)} 个Google搜索结果。")

    # 使用 ThreadPoolExecutor 抓取各搜索结果页面内容，同时检测中断
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_result = {}
        for result in results:
            if worker and not worker.is_running:
                logging.info("抓取内容任务被中断。")
                break
            future = executor.submit(get_page_content, result['link'], worker)
            future_to_result[future] = result

        for future in as_completed(future_to_result):
            if worker and not worker.is_running:
                logging.info("抓取内容任务被中断，取消剩余任务。")
                for fut in future_to_result:
                    if not fut.done():
                        fut.cancel()
                break
            result = future_to_result[future]
            try:
                result['content'] = future.result()
            except Exception as e:
                logging.error(f"抓取内容时出错 ({result['link']}): {e}")
                result['content'] = "无法获取内容"

    return results


def get_bing_search_results(query, num_results=5, worker=None):
    """
    获取 Bing 搜索结果，并抓取每个结果页面的内容。
    """
    query_encoded = urllib.parse.quote_plus(query)
    url = f"https://www.bing.com/search?q={query_encoded}&count={num_results}"

    logging.info(f"发送请求到Bing URL: {url}")
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            logging.error(f"搜索结果页面非HTML内容: {url}，Content-Type: {content_type}")
            raise Exception("搜索结果页面非HTML内容")

        detected = charset_normalizer.from_bytes(response.content).best()
        encoding = detected.encoding if detected and detected.encoding else 'utf-8'

        text = response.content.decode(encoding, errors='replace')
        logging.info(f"检测到编码: {encoding}，Bing搜索结果页面URL: {url}")
    except Exception as e:
        logging.error(f"请求或解码Bing搜索结果失败：{e}")
        raise Exception(f"请求或解码Bing搜索结果失败：{e}")

    soup = BeautifulSoup(text, 'html.parser')
    results = []

    for li in soup.find_all('li', class_='b_algo'):
        h2 = li.find('h2')
        if h2 and h2.find('a'):
            a_tag = h2.find('a')
            title = a_tag.get_text(separator=' ', strip=True)
            link = a_tag['href']
        else:
            title = "No title"
            link = "No link"

        snippet_tag = li.find('p')
        snippet = snippet_tag.get_text(separator=' ', strip=True) if snippet_tag else "No content"

        results.append({
            'title': title,
            'link': link,
            'snippet': snippet,
            'content': "正在获取内容...",
            'engine': 'Bing'
        })

        if len(results) >= num_results:
            break

    logging.info(f"解析出 {len(results)} 个Bing搜索结果。")

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_result = {}
        for result in results:
            if worker and not worker.is_running:
                logging.info("抓取内容任务被中断。")
                break
            future = executor.submit(get_page_content, result['link'], worker)
            future_to_result[future] = result

        for future in as_completed(future_to_result):
            if worker and not worker.is_running:
                logging.info("抓取内容任务被中断，取消剩余任务。")
                for fut in future_to_result:
                    if not fut.done():
                        fut.cancel()
                break
            result = future_to_result[future]
            try:
                result['content'] = future.result()
            except Exception as e:
                logging.error(f"抓取内容时出错 ({result['link']}): {e}")
                result['content'] = "无法获取内容"

    return results


def get_baidu_search_results(query, num_results=5, worker=None):
    """
    获取 百度 搜索结果，并抓取每个结果页面的内容。
    """
    query_encoded = urllib.parse.quote_plus(query)
    url = f"https://www.baidu.com/s?wd={query_encoded}&rn={num_results}&ie=utf-8"

    logging.info(f"发送请求到百度 URL: {url}")
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if 'text/html' not in content_type:
            logging.error(f"搜索结果页面非HTML内容: {url}，Content-Type: {content_type}")
            raise Exception("搜索结果页面非HTML内容")

        detected = charset_normalizer.from_bytes(response.content).best()
        encoding = detected.encoding if detected and detected.encoding else 'utf-8'

        text = response.content.decode(encoding, errors='replace')
        logging.info(f"检测到编码: {encoding}，百度搜索结果页面URL: {url}")
    except Exception as e:
        logging.error(f"请求或解码百度搜索结果失败：{e}")
        raise Exception(f"请求或解码百度搜索结果失败：{e}")

    soup = BeautifulSoup(text, 'html.parser')
    results = []

    for div in soup.find_all('div', class_='result'):
        h3 = div.find('h3')
        if h3 and h3.find('a'):
            a_tag = h3.find('a')
            title = a_tag.get_text(separator=' ', strip=True)
            link = a_tag['href']
        else:
            title = "No title"
            link = "No link"

        snippet_tag = div.find('div', class_='c-abstract')
        if not snippet_tag:
            snippet_tag = div.find('div', class_='c-span18 c-span-last')
        snippet = snippet_tag.get_text(separator=' ', strip=True) if snippet_tag else "No content"

        results.append({
            'title': title,
            'link': link,
            'snippet': snippet,
            'content': "正在获取内容...",
            'engine': '百度'
        })

        if len(results) >= num_results:
            break

    logging.info(f"解析出 {len(results)} 个百度搜索结果。")

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_result = {}
        for result in results:
            if worker and not worker.is_running:
                logging.info("抓取内容任务被中断。")
                break
            future = executor.submit(get_page_content, result['link'], worker)
            future_to_result[future] = result

        for future in as_completed(future_to_result):
            if worker and not worker.is_running:
                logging.info("抓取内容任务被中断，取消剩余任务。")
                for fut in future_to_result:
                    if not fut.done():
                        fut.cancel()
                break
            result = future_to_result[future]
            try:
                result['content'] = future.result()
            except Exception as e:
                logging.error(f"抓取内容时出错 ({result['link']}): {e}")
                result['content'] = "无法获取内容"

    return results