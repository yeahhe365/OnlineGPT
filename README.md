# OnlineGPT

![Clip_2024-09-29_23-47-27](https://github.com/user-attachments/assets/02794f4f-f552-45ff-a6bc-54fd18f2d006)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

## 简介

**OnlineGPT** 是一个基于 Python 和 PyQt5 的桌面应用程序，为用户提供了一个功能强大的图形用户界面，支持使用多个搜索引擎（Google、Bing、百度）进行网络搜索。它的主要目的是让**语言模型能够连接到互联网**，获取实时的网络信息，以提供更准确和丰富的回答。

**GitHub 主页**：[https://github.com/yeahhe365/OnlineGPT.git](https://github.com/yeahhe365/OnlineGPT.git)

## 功能特点

- **连接语言模型与互联网**：通过搜索引擎获取最新的网络信息，增强语言模型的知识库。

- **多搜索引擎支持**：轻松切换 Google、Bing、百度等主流搜索引擎，获取最全面的搜索结果。

- **进阶模式**：支持批量关键词输入和自定义问题，满足高级用户的需求。

- **结果预览**：以表格形式展示搜索结果，包括标题、链接、摘要和内容，直观明了。

- **内容获取**：自动抓取搜索结果页面的详细内容，采用多线程技术，加速内容获取。

- **结果管理**：支持选择、保存、打开和复制搜索结果，方便数据的存储和共享。

- **日志记录**：实时显示应用程序的运行日志，方便调试和监控运行状态。

- **中断操作**：在搜索过程中可随时中断任务，增强用户对程序的控制。

- **快捷键支持**：提供多种快捷键，提升操作效率。

## 快捷键列表

| 快捷键     | 功能             |
|------------|------------------|
| ↑ 方向键   | 光标移动到开头   |
| ↓ 方向键   | 光标移动到末尾   |
| Delete 键  | 清空关键词       |
| Enter 键   | 开始搜索         |
| Ctrl + C   | 中断             |

## 安装指南

### 系统要求

- **操作系统**：Windows、macOS、Linux
- **Python 版本**：Python 3.7 或以上

### 依赖库

在运行本程序之前，需要安装以下 Python 库：

- [PyQt5](https://pypi.org/project/PyQt5/)
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [charset-normalizer](https://pypi.org/project/charset-normalizer/)

### 安装步骤

1. **克隆仓库**

   ```bash
   git clone https://github.com/yeahhe365/OnlineGPT.git
   cd OnlineGPT
   ```

2. **创建虚拟环境（可选）**

   ```bash
   python -m venv venv
   ```

   - **激活虚拟环境**

     - Windows:

       ```bash
       venv\Scripts\activate
       ```

     - macOS/Linux:

       ```bash
       source venv/bin/activate
       ```

3. **安装依赖库**

   ```bash
   pip install -r requirements.txt
   ```

   **注意**：如果没有 `requirements.txt` 文件，可以手动安装：

   ```bash
   pip install PyQt5 requests beautifulsoup4 charset-normalizer
   ```

## 使用说明

### 运行程序

在命令行中，进入项目目录，运行以下命令：

```bash
python main.py
```

### 用户界面说明

#### 主窗口

（在此处添加程序的 UI 图片，例如主窗口的截图）

![Clip_2024-09-29_23-44-25](https://github.com/user-attachments/assets/60cd2f8e-7b07-4dc9-ab1f-a138e4e53f2b)
![Clip_2024-09-29_23-45-41](https://github.com/user-attachments/assets/456fcac1-54c6-43aa-9c87-67acc7a421f3)


- **搜索设置**

  - **进阶模式**：勾选后，可以输入多个关键词和自定义问题，适用于批量搜索和复杂查询。

  - **搜索引擎**：从下拉菜单中选择要使用的搜索引擎（Google、Bing、百度）。

  - **搜索结果数量**：设置要获取的搜索结果数量，范围为 1 到 20。

- **关键词输入**

  - **普通模式**：在“请输入搜索关键词”输入框中输入单个关键词。

  - **进阶模式**：在多行输入框中输入多个关键词（每行一个），并在“请输入问题”输入框中输入自定义问题。

- **按钮操作**

  - **搜索**：开始搜索任务，根据输入的关键词和设置获取搜索结果。

  - **中断**：中断当前的搜索任务，立即停止搜索和内容抓取。

  - **保存结果**：将选中的搜索结果保存到文本文件，支持自定义保存路径。

  - **打开结果**：打开已保存的结果文件，方便查看和编辑。

  - **复制**：将选中的搜索结果复制到剪贴板，便于粘贴和分享。

- **状态和进度**

  - **状态标签**：显示当前的运行状态，如“等待输入...”、“正在搜索，请稍候...”等。

  - **进度条**：显示搜索任务的进度，支持无限模式和百分比进度。

- **结果显示区**

  - 以表格形式展示搜索结果，包括 **选择**、**URL**、**标题**、**摘要** 和 **内容**。

  - **复选框表头**：可一键全选或取消全选所有搜索结果。

  - 点击 **URL** 列，可在默认浏览器中打开对应的链接。

- **日志区**

  - 实时显示应用程序的运行日志，包括 **INFO**、**WARNING**、**ERROR** 等级别的日志信息。

  - 日志信息包括时间戳、日志级别和消息内容。

### 操作步骤

1. **选择模式**

   - **普通模式**：适用于单个关键词的快速搜索。

   - **进阶模式**：适用于批量关键词搜索和需要自定义问题的场景。

2. **输入关键词**

   - **普通模式**：在“请输入搜索关键词”输入框中输入关键词，如“明天天气怎么样”。

   - **进阶模式**：在多行输入框中输入多个关键词（每行一个），如：

     ```
     明天天气怎么样
     上海旅游攻略
     ```

     并在“请输入问题”输入框中输入自定义问题。

3. **设置搜索参数**

   - 从下拉菜单中选择搜索引擎（默认：Google）。

   - 设置搜索结果数量（默认：5）。

4. **开始搜索**

   - 点击 **搜索** 按钮，程序将开始搜索任务。

   - 搜索过程中，**搜索** 按钮将被禁用，**中断** 按钮启用。

5. **查看结果**

   - 搜索完成后，结果将显示在下方的表格中。

   - 可通过勾选左侧的复选框选择需要的结果。

6. **保存或复制结果**

   - 点击 **保存结果** 按钮，选择保存路径，将选中的结果保存为文本文件。

   - 点击 **复制** 按钮，将选中的结果复制到剪贴板。

7. **打开结果**

   - 点击 **打开结果** 按钮，打开已保存的结果文件。

### 注意事项

- **中断操作**

  - 在搜索过程中，可随时点击 **中断** 按钮或使用快捷键 **Ctrl + C** 停止任务。

  - 中断后，已获取的结果将保留，未完成的任务将被终止。

- **日志查看**

  - 在程序运行过程中，可在日志区查看详细的运行信息。

  - 日志信息包括时间戳、日志级别和消息内容。

- **快捷键**

  | 快捷键     | 功能             |
  |------------|------------------|
  | ↑ 方向键   | 光标移动到开头   |
  | ↓ 方向键   | 光标移动到末尾   |
  | Delete 键  | 清空关键词       |
  | Enter 键   | 开始搜索         |
  | Ctrl + C   | 中断             |

## 文件结构

```
OnlineGPT
├── main.py
├── search_app.py
├── worker.py
├── search_engines.py
├── utils.py
├── gui_components.py
├── resources
│   ├── icon.ico
│   ├── logo.png
│   └── main_window.png  # UI 截图
├── controllers
│   ├── event_handlers.py
│   └── __init__.py
├── models
│   ├── data_models.py
│   └── __init__.py
├── search
│   ├── search_engines
│   │   ├── google_search.py
│   │   ├── bing_search.py
│   │   ├── baidu_search.py
│   │   └── __init__.py
│   ├── utils
│   │   ├── network_utils.py
│   │   ├── text_utils.py
│   │   ├── file_utils.py
│   │   └── __init__.py
│   ├── worker.py
│   └── __init__.py
├── ui
│   ├── ui_search_app.py
│   ├── gui_components.py
│   └── __init__.py
├── constants.py
├── logging_config.py
├── icon.ico
├── logo.png
└── __pycache__
```

### 主要文件和目录说明

- **main.py**：程序入口，初始化应用程序并启动主窗口。

- **search_app.py**：定义了 `SearchApp` 类，构建了应用程序的主界面和主要逻辑。

- **worker.py**：定义了 `Worker` 类，处理搜索任务的后台线程，支持中断操作。

- **search_engines.py**：包含对不同搜索引擎的支持，定义了获取搜索结果的函数。

- **utils.py**：工具函数，包括清洗文本、获取页面内容、生成和保存结果等。

- **gui_components.py**：自定义的 GUI 组件，包括日志处理器、自定义输入框、复选框表头等。

- **resources**：存放应用程序的资源文件，如图标和图片。

- **controllers**：包含事件处理器，负责处理用户交互和界面事件。

- **models**：包含数据模型，定义了应用程序中使用的数据结构。

- **search**：搜索相关的模块，包含搜索引擎接口和工具函数。

- **ui**：界面组件，包含 UI 界面的定义和自定义组件。

- **__pycache__**：Python 编译文件缓存目录，可忽略。

## 备用下载

如果您无法通过 GitHub 获取本项目，您可以通过以下备用下载链接获取：

- **备用下载站**：[https://www.yeahhe.online/OneDriveShare/小虎会享/⌨️Code/🐍Python/🕷爬虫/OnlineGPT](https://www.yeahhe.online/OneDriveShare/%E5%B0%8F%E8%99%8E%E4%BC%9A%E4%BA%AB/%E2%8C%A8%EF%B8%8FCode/%F0%9F%90%8DPython/%F0%9F%95%B7%E7%88%AC%E8%99%AB/OnlineGPT)

## 讨论与交流

欢迎加入以下讨论，分享您的使用体验和建议：

- **LINUXDO 论坛讨论**：[https://linux.do/t/topic/211975?u=yeahhe](https://linux.do/t/topic/211975?u=yeahhe)

## 贡献指南

欢迎对本项目提出意见、建议和改进。您可以通过以下方式参与：

- **提交问题**：如果发现任何问题或有改进建议，请在 GitHub 的 Issues 中提交，我们会尽快处理。

- **拉取请求**：欢迎提交拉取请求以修复问题或添加新功能。在提交之前，请确保您的代码符合项目的代码规范，并进行了充分的测试。

- **代码规范**：请遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码规范，保持代码的一致性和可读性。

## 许可证

本项目采用 [Apache License 2.0](LICENSE) 进行许可。您可以自由地使用、修改和分发本软件。

## 致谢

感谢所有为本项目做出贡献的开发者和社区成员。特别感谢开源社区提供的优秀工具和资源。

---

**注意**：在使用本软件时，请遵守各搜索引擎的使用条款和相关法律法规。未经授权，不要进行过于频繁的自动化请求，以免对目标网站造成负担。
