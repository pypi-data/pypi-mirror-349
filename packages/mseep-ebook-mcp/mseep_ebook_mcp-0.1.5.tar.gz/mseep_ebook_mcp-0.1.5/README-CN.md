# Ebook-MCP
<img src="logo.png" alt="ebook-mcp logo" width="132" height="132">

[English](https://github.com/onebirdrocks/ebook-mcp/blob/main/README.md) | 中文


Ebook-MCP 是一个功能强大的电子书处理 Model Context Protocol (MCP) 服务器。基于 [Model Context Protocol](https://github.com/modelcontextprotocol) 构建，它提供了一套标准化的 API，可以无缝集成 LLM 应用程序和电子书处理功能。目前支持 EPUB 和 PDF 格式。

## 使用场景和价值

Ebook-MCP 通过启用与阅读材料的自然语言对话，彻底改变了您与电子书的交互方式。它可以无缝集成到现代 AI 驱动的 IDE（如 Cursor 和 Claude）中，让您能够：

- **智能图书馆管理**：只需简单询问"显示我下载文件夹中的所有 EPUB 文件"或"在我的图书馆中查找关于 GenAI 的书籍"
- **交互式阅读体验**：与您的书籍进行自然对话：
  - "给我简单介绍一下'LLM Engineer Handbook'这本书"
  - "第三章讲了什么内容？"
  - "总结一下这本书中关于 RAG 的要点"
- **主动学习支持**：通过 AI 驱动的交互增强学习效果：
  - "基于第五章中的 RAG 概念创建一个测验"
  - "解释一下本章讨论的各种架构之间的差异"
  - "根据本节的概念给我一些实践练习"
- **内容导航**：使用自然语言查询轻松浏览您的书籍：
  - "查找所有讨论提示工程的章节"
  - "显示关于微调的章节"
  - "带我到讨论向量数据库的部分"

通过架起传统电子书和 AI 功能之间的桥梁，Ebook-MCP 帮助读者通过直观的对话式交互从数字图书馆中获取更多价值。

快速演示 — 使用 DeepSeek 运行（更多 Claude 和 OpenAI 的示例代码，请查看 mcp-client-example 文件夹）
```
问：你能帮我查询我的下载目录中的epub电子书吗？
问答省略:各种总结归纳都可...........


## 查询：
用户：你能考察我几个问题，看我对这本书的掌握程度吗？


AI：好的！以下是关于《埃隆·马斯克传》（Walter Isaacson 著）的5个问题，测试你对这本书的掌握程度。请根据你的理解回答，我会根据你的答案进行反馈和补充。

---

### 问题1：
马斯克的童年和家庭背景，如何影响了他后来的性格和事业？
（提示：与父亲的关系、南非的成长经历等）

---

### 问题2：
Zip2 和 X.com（后来的 PayPal）是马斯克早期的创业项目。它们分别解决了什么问题？马斯克最终是如何退出这些公司的？
（提示：Zip2的商业模式，X.com与Confinity的合并等）

---

### 问题3：
2008年，SpaceX 和特斯拉同时濒临破产。马斯克是如何拯救这两家公司的？
（提示：猎鹰1号的第四次发射，NASA合同，特斯拉的“最后一搏”等）

---

### 问题4：
马斯克的管理风格有哪些争议？书中有哪些具体事件体现了他的“硬核”或“极端”工作文化？
（提示：弗里蒙特工厂的“生产地狱”、推特的大裁员等）

---

### 问题5：
马斯克对人工智能（AI）的态度是什么？他为什么同时支持OpenAI和Neuralink这两个看似矛盾的项目？
（提示：AI的生存威胁论，脑机接口的愿景等）

---

请依次回答这些问题，我会根据你的答案进行补充和纠正。
（如果某个问题不清楚，也可以直接问我）

---

## 用户回答：

- 问题1：他父亲对他粗暴的态度，让他对他人缺乏共情。
- 问题2：Zip2 解决了电子地图和在线黄页的问题。X.com 解决了电子支付。
- 问题3：他拿到了NASA的订单。特斯拉通过在中国建厂解决了产能问题。
- 问题4：我不知道，请帮我解答。
- 问题5：他认为开源技术是确保AI安全和开放的必要方式。

---

## AI回答：你的回答已经抓住了书中的一些关键点，我来补充细节和纠正一些偏差，同时为问题4和5提供更多背景：

---

### 问题1 —— 修正与补充

#### 父亲的影响：
马斯克的父亲埃罗尔确实非常严苛，比如曾经强迫小马斯克跪在地上数大米几个小时。书中强调，这种情感钝化的经历，反而让他形成了极端的目标导向性格 —— 对别人的痛苦不敏感，但对目标极度执着。

#### 反向影响：
马斯克并不是完全没有共情能力，而是选择性共情。例如他对员工冷酷，但会亲自研究医疗设备来帮助生病的儿子X。

---

### 问题2 —— 修正与补充

#### Zip2：
本质上是企业在线黄页 + 地图导航服务（帮助报纸实现数字化转型）。马斯克早期亲自编写大量代码，甚至睡在办公室。最终被康柏（Compaq）以3.07亿美元收购，马斯克个人获得2200万美元。

#### X.com：
不仅仅是电子支付，更是马斯克试图打造的一个金融全平台（取代银行）。后来与Confinity（PayPal前身）合并，但因为内部斗争被踢出管理层。eBay收购PayPal时，马斯克获得了1.8亿美元。
> 注：X.com 后来被马斯克买回，成为推特母公司的名称。

---

### 问题3 —— 修正与补充

#### SpaceX：
2008年，猎鹰1号在经历三次失败后，第四次发射终于成功。紧接着，SpaceX 拿到了NASA价值16亿美元的货运合同，成为公司的救命稻草。

#### 特斯拉：
2008年，特斯拉靠戴姆勒投资的5000万美元，以及美国能源部的贷款才得以生存下来。
> 中国建厂（2019年）是后期的事情。早期的生存关键是Model S（2012年）的成功发布，以及马斯克卖掉自己所有房产，全力押注特斯拉。

---

### 问题4 —— 解答：管理风格的争议

#### “硬核”文化：

- 在SpaceX和特斯拉：马斯克要求员工每周工作80小时以上，甚至要在工厂里过夜。他曾说：“如果你不在这里，就会有人取代你的位置。”
  
- 收购推特后：他立即裁员75%，并要求剩余员工签署“极端硬核”承诺书，承诺长时间、高强度工作。

#### 极端案例：

- 弗里蒙特工厂：Model 3产能地狱时期，马斯克直接睡在生产线上，甚至骂员工“连狗都不如”（事后道歉）。

- 开除高管：曾因为PPT字体不够大，当场开除特斯拉高管。

---

### 问题5 —— 修正与补充

#### AI威胁论：
马斯克认为AI可能会毁灭人类（“比核弹更危险”）。因此：

- OpenAI：最初支持OpenAI，推动安全、开源的AI（但后来因控制权分歧离开）。

- Neuralink：希望通过脑机接口让人类与AI共生，避免人类被AI淘汰。

#### 矛盾之处：
尽管警告AI的风险，但马斯克同时在特斯拉大力推动自动驾驶（FSD），并成立xAI研究AGI（通用人工智能）。


### **综合评分**：
✅ 核心事件抓得准，但细节需强化（如时间线、具体金额）。
🔍 建议再关注：马斯克的**多线程管理**（同时操盘5家公司）、**舆论操控术**（推特治国）。
```

## 功能特性

### EPUB 支持
- 提取元数据（标题、作者、出版日期等）
- 提取目录
- 提取章节内容（支持 Markdown 输出）
- 批量处理 EPUB 文件

### PDF 支持
- 提取元数据（标题、作者、创建日期等）
- 提取目录
- 按页码提取内容
- 按章节标题提取内容
- 支持 Markdown 输出
- 批量处理 PDF 文件

## 安装

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/ebook-mcp.git
cd ebook-mcp
```

2. 使用 `uv` 安装依赖：
```bash
uv pip install -r requirements.txt
```

## 使用方法

### 在开发模式下启动 MCP 服务器

运行开发模式服务器：
```bash
uv run mcp dev src/ebook_mcp/main.py
```
您可以访问 http://localhost:5173/ 进行测试和调试

### 在生产模式下启动 MCP 服务器

运行生产模式服务器：
```bash
uv run main.py
```

#### 在 Cursor 中配置 MCP

在 Cursor 中添加以下配置：
```bash
"ebook-mcp":{
            "command": "uv",
            "args": [
                "--directory",
                "/Users/onebird/github/ebook-mcp/src/ebook_mcp/",
                "run",
                "main.py"
            ]
        }
```



### EPUB 处理示例

```python
# 获取目录中的所有 EPUB 文件
epub_files = get_all_epub_files("/path/to/books")

# 获取 EPUB 元数据
metadata = get_metadata("/path/to/book.epub")

# 获取目录
toc = get_toc("/path/to/book.epub")

# 获取特定章节内容（Markdown 格式）
chapter_content = get_chapter_markdown("/path/to/book.epub", "chapter_id")
```

### PDF 处理示例

```python
# 获取目录中的所有 PDF 文件
pdf_files = get_all_pdf_files("/path/to/books")

# 获取 PDF 元数据
metadata = get_pdf_metadata("/path/to/book.pdf")

# 获取目录
toc = get_pdf_toc("/path/to/book.pdf")

# 获取特定页面内容
page_text = get_pdf_page_text("/path/to/book.pdf", 1)
page_markdown = get_pdf_page_markdown("/path/to/book.pdf", 1)

# 获取特定章节内容
chapter_content, page_numbers = get_pdf_chapter_content("/path/to/book.pdf", "Chapter 1")
```

## API 参考

### EPUB APIs

#### `get_all_epub_files(path: str) -> List[str]`
获取指定目录中的所有 EPUB 文件。

#### `get_metadata(epub_path: str) -> Dict[str, Union[str, List[str]]]`
获取 EPUB 文件的元数据。

#### `get_toc(epub_path: str) -> List[Tuple[str, str]]`
获取 EPUB 文件的目录。

#### `get_chapter_markdown(epub_path: str, chapter_id: str) -> str`
获取章节内容的 Markdown 格式。

### PDF APIs

#### `get_all_pdf_files(path: str) -> List[str]`
获取指定目录中的所有 PDF 文件。

#### `get_pdf_metadata(pdf_path: str) -> Dict[str, Union[str, List[str]]]`
获取 PDF 文件的元数据。

#### `get_pdf_toc(pdf_path: str) -> List[Tuple[str, int]]`
获取 PDF 文件的目录。

#### `get_pdf_page_text(pdf_path: str, page_number: int) -> str`
获取特定页面的纯文本内容。

#### `get_pdf_page_markdown(pdf_path: str, page_number: int) -> str`
获取特定页面的 Markdown 格式内容。

#### `get_pdf_chapter_content(pdf_path: str, chapter_title: str) -> Tuple[str, List[int]]`
通过章节标题获取章节内容和对应的页码。

## 依赖项

主要依赖包括：
- ebooklib：EPUB 文件处理
- PyPDF2：基础 PDF 处理
- PyMuPDF：高级 PDF 处理
- beautifulsoup4：HTML 解析
- html2text：HTML 转 Markdown
- pydantic：数据验证
- fastmcp：MCP 服务器框架

## 重要说明

1. PDF 处理依赖于文档的目录。如果目录不可用，某些功能可能无法工作。
2. 对于大型 PDF 文件，建议按页面范围处理，避免一次性加载整个文件。
3. EPUB 章节 ID 必须从目录结构中获取。

## 架构

```
           ┌────────────────────────────┐
           │         代理层             │
           │  - 翻译策略               │
           │  - 风格一致性检查         │
           │  - LLM 调用与交互         │
           └────────────▲─────────────┘
                        │ 工具调用
           ┌────────────┴─────────────┐
           │        MCP 工具层        │
           │  - 提取章节              │
           │  - 写入翻译后的章节      │
           │  - 生成 EPUB             │
           └────────────▲─────────────┘
                        │ 系统/IO 调用
           ┌────────────┴─────────────┐
           │        系统基础层        │
           │  - 文件读取             │
           │  - ebooklib 解析        │
           │  - 文件路径存储/检查    │
           └────────────────────────────┘
```

## 贡献

我们欢迎 Issues 和 Pull Requests！

## 更新日志

### v1.0.5
- 初始发布
- 支持 EPUB 和 PDF 格式
- 基础文件处理 API
- MCP Client的例子（Claude，DeepSeek，OpenAI）
- 支持从PyPI下载运行
