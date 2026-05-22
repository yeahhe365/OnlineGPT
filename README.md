<p align="center">
  <a href="./README.md">中文</a> | <a href="./README.en.md">English</a>
</p>

---

# OnlineGPT 7.0

![icon](https://github.com/user-attachments/assets/bac65bed-11e0-413f-9cc8-2ab1c78ba8ec)


**OnlineGPT 7.0** 是一个强大的在线信息搜索和管理工具，基于 Python 和 PyQt5 构建。它支持多种搜索引擎，提供高级搜索选项，并允许用户轻松复制、保存和管理搜索结果。该项目支持中英文界面，旨在为全球用户提供便捷的搜索体验。

## 目录

- [功能特点](#功能特点)
- [截图](#截图)
- [安装](#安装)
- [使用指南](#使用指南)
- [许可证](#许可证)
- [贡献](#贡献)
- [联系方式](#联系方式)
- [附加资源](#附加资源)

## 功能特点

- **多语言支持**：支持中英文界面，满足不同语言用户的需求。
- **多搜索引擎**：集成 Google、Bing 和百度，提供多样化的搜索选择。
- **高级搜索模式**：允许用户输入多行关键词和自定义问题，实现更精细的搜索。
- **结果管理**：轻松复制、保存或打开搜索结果，提升工作效率。
- **实时日志**：内置日志记录，帮助用户跟踪搜索活动和调试。
- **快捷键支持**：支持快捷键（如 Ctrl+C）快速中断搜索任务。
- **用户友好的界面**：简洁直观的用户界面设计，易于上手。

## 截图

![PixPin_2024-12-13_00-23-01](https://github.com/user-attachments/assets/648df9b9-8512-453d-899d-87e486265cb9)


![PixPin_2024-12-13_00-23-36](https://github.com/user-attachments/assets/ab9bb89e-5463-4965-9ebd-7c50e687b491)


## 安装

### 前提条件

- **Python 3.7+**：确保已安装 Python 3.7 或更高版本。可以从 [Python 官方网站](https://www.python.org/downloads/) 下载并安装。
- **Git**：用于克隆仓库。可以从 [Git 官方网站](https://git-scm.com/downloads) 下载并安装。

### 步骤

1. **克隆仓库**

   打开终端或命令提示符，执行以下命令将项目克隆到本地：

   ```bash
   git clone https://github.com/yeahhe365/OnlineGPT.git
   ```

2. **进入项目目录**

   ```bash
   cd OnlineGPT
   ```

3. **创建虚拟环境（可选但推荐）**

   创建并激活一个虚拟环境，以隔离项目依赖：

   ```bash
   python -m venv venv
   ```

   - **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

4. **安装依赖**

   使用 `pip` 安装项目所需的依赖包：

   ```bash
   pip install -r requirements.txt
   ```

   *如果没有 `requirements.txt` 文件，请创建并添加以下内容：*

   ```text
   PyQt5>=5.15.4
   requests
   ```

5. **运行应用程序**

   在项目根目录下，运行以下命令启动应用：

   ```bash
   python search_app.py
   ```

## 使用指南

### 启动应用

运行应用程序后，将看到如下主界面：
![PixPin_2024-12-13_00-16-18](https://github.com/user-attachments/assets/639c5367-3d2b-4a9e-a408-cd5a3eb6685a)

![PixPin_2024-12-13_00-19-01](https://github.com/user-attachments/assets/3ad2590e-c747-437d-9db9-82c83a1604ca)

![PixPin_2024-12-13_00-25-34](https://github.com/user-attachments/assets/57755631-e83d-42c2-9e3c-6b5816a99f29)

### 主要功能

1. **输入搜索关键词**
   - **普通模式**：在“搜索关键词”输入框中输入单个关键词或短语。
   - **进阶模式**：勾选“进阶模式”，可以在高级输入框中输入多行关键词，并附加自定义问题。

2. **选择搜索引擎**
   - 从下拉菜单中选择您偏好的搜索引擎（Google、Bing、百度）。

3. **设置搜索数量**
   - 使用加号和减号按钮调整每个关键词的搜索结果数量。

4. **开始搜索**
   - 点击“搜索”按钮，应用将开始执行搜索任务。搜索进度会在状态栏和进度条中显示。

5. **查看和管理结果**
   - 搜索完成后，结果将显示在下方的表格中。您可以：
     - **复制**：点击“复制”按钮将选中的内容复制到剪贴板。
     - **保存结果**：点击“保存结果”按钮将结果保存为文本文件。
     - **打开结果**：点击“打开结果”按钮直接打开保存的结果文件。

6. **中断搜索**
   - 在搜索过程中，如果需要中断任务，可以点击“中断”按钮或使用快捷键 `Ctrl+C`。

### 高级设置

- **日志记录**：底部的日志窗口显示应用的实时日志，有助于调试和了解搜索过程。
- **快捷键支持**：支持多种快捷键操作，提升使用效率。

### 多语言切换

- 在菜单栏中选择“Language”或“语言”，切换应用界面的语言（英文或中文）。

### 示例操作

1. **普通搜索**：

   - 输入关键词：`Python 教程`
   - 选择搜索引擎：`Google`
   - 设置结果数量：10
   - 点击“搜索”，等待结果显示。

2. **进阶搜索**：

   - 勾选“进阶模式”
   - 在高级输入框中输入多行关键词：
     ```
     天气预报
     股票行情
     ```
   - 输入自定义问题：`如何在 Python 中实现爬虫？`
   - 选择搜索引擎：`Bing`
   - 设置结果数量：5
   - 点击“搜索”，等待结果显示。

## 许可证

本项目采用 [MIT 许可证](LICENSE) 进行许可。您可以根据许可证的条款自由使用、修改和分发该软件。

## 贡献

欢迎任何形式的贡献！无论是报告问题、提出建议还是提交代码改进，您的参与都将使 **OnlineGPT 7.0** 变得更好。

### 如何贡献

1. **Fork 仓库**

   点击右上角的 “Fork” 按钮，将项目仓库克隆到您的 GitHub 账户中。

2. **创建新分支**

   在本地仓库中，创建一个新的分支来进行您的修改：

   ```bash
   git checkout -b feature/您的分支名称
   ```

3. **进行修改**

   进行您想要的修改和改进。

4. **提交更改**

   添加并提交您的更改：

   ```bash
   git add .
   git commit -m "描述您的更改"
   ```

5. **推送到远程分支**

   ```bash
   git push origin feature/您的分支名称
   ```

6. **创建 Pull Request**

   回到 GitHub 仓库页面，点击 “Compare & pull request” 按钮，填写相关信息并提交 Pull Request。

### 代码规范

- 请确保代码符合 PEP 8 规范。
- 添加必要的注释和文档，便于他人理解您的代码。
- 在进行重大更改前，请先开一个 issue，与维护者讨论您的想法。

## 联系方式

如果您有任何问题、建议或反馈，请通过以下方式与我们联系：

- **邮箱**：yeahhe@example.com
- **GitHub Issues**：[Issues 页面](https://github.com/yeahhe365/OnlineGPT/issues)
- **论坛**：[LINUXDO 论坛](https://linux.do/t/topic/211975)

## 附加资源

- **开源地址**：[https://github.com/yeahhe365/OnlineGPT](https://github.com/yeahhe365/OnlineGPT)
- **LINUXDO 论坛**：[https://linux.do/t/topic/211975](https://linux.do/t/topic/211975)

---

## 更新日志

### [v7.0](https://github.com/yeahhe365/OnlineGPT/releases/tag/v7.0) - 2024-04-27

- 引入多语言支持（中英文）
- 集成 Google、Bing 和百度搜索引擎
- 添加高级搜索模式
- 优化用户界面，提升用户体验
- 增加日志记录功能
- 实现快捷键支持（如 Ctrl+C 中断搜索）

---

感谢您使用 **OnlineGPT 7.0**！我们致力于不断改进和提升，如果您有任何建议或反馈，欢迎随时与我们联系。

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
