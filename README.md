# ZenBook

ZenBook 是一个基于 Go 语言开发的智能搜索和总结工具。它利用 OpenAI 的 GPT 模型来处理和总结从特定来源(如小红书)抓取的信息。

## 功能特点

- 从小红书抓取指定主题的帖子和评论
- 使用 GPT 模型对抓取的内容进行智能总结
- 将总结结果保存为 Markdown 文件

## 安装

1. 确保您已安装 Go 1.20 或更高版本。
2. 克隆此仓库:
   ```
   git clone https://github.com/ClayCheung/zenbook.git
   ```
3. 进入项目目录:
   ```
   cd zenbook
   ```
4. 安装依赖:
   ```
   go mod download
   ```

## 配置

1. 在项目根目录创建 `.env` 文件。
2. 在 `.env` 文件中添加以下内容:
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_BASE_URL=your_openai_base_url
   ```

## 使用方法

有两种方式运行程序:

1. 直接使用 `go run` 命令:
   ```
   go run cmd/main.go -query "您的搜索查询"
   ```

2. 先编译为二进制文件,然后运行:
   ```
   go build -o zenbook cmd/main.go
   ./zenbook -query "您的搜索查询"
   ```

运行后,程序将从小红书抓取相关内容,使用 GPT 模型进行总结,并将结果保存在 `output/answer.md` 文件中。
