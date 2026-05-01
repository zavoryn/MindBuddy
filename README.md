# MindBuddy

<p align="center">
  <strong>一个用 Python 实现的简化版 Claude Code</strong>
</p>

<p align="center">
  MindBuddy 是对 Claude Code（Anthropic 官方终端编程助手）核心架构的轻量级开源复刻。<br>
  它用 Python 重新实现了 Claude Code 的关键能力：Agent 循环、工具调用、上下文管理、会话持久化和记忆系统。
</p>

<p align="center">
  <a href="./README.zh-CN.md">English</a>
  |
  <a href="https://github.com/zavoryn/MindBuddy">GitHub</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue?style=flat-square">
</p>

---

## 这是什么？

如果你用过 Claude Code（`claude` 命令行工具），你会知道它能：

- 读取你的代码文件
- 编辑和修改代码
- 运行终端命令
- 搜索代码库
- 跨长对话记住上下文

**MindBuddy 就是这些能力的 Python 开源实现。** 它不是 API 封装，不是聊天壳子，而是一个完整的 Agent 运行时——从工具调用到上下文管理到会话持久化，全部自己实现。

## 跟 Claude Code 的对应关系

| Claude Code 功能 | MindBuddy 对应实现 | 说明 |
| --- | --- | --- |
| Agent Loop | `agent_loop.py` | 核心循环：接收用户输入 → 调用模型 → 解析工具调用 → 执行工具 → 返回结果 |
| Read/Edit/Write 工具 | `tools/read_file.py` `tools/edit_file.py` `tools/write_file.py` | 文件读写和精确字符串替换编辑 |
| Grep/Glob 工具 | `tools/grep_files.py` `tools/list_files.py` `tools/file_tree.py` | 代码搜索和文件发现 |
| Bash 工具 | `tools/run_command.py` | Shell 命令执行，带超时控制 |
| 上下文压缩 | `context_compactor.py` | 上下文溢出时自动压缩历史消息 |
| Memory 系统 | `memory.py` `working_memory.py` `memory_pipeline.py` | 三层记忆：工作记忆保护 + 项目知识注入 + 自动策展 |
| 会话持久化 | `session.py` | 会话可保存、恢复、回放、回滚 |
| MCP 工具扩展 | `mcp.py` `skills.py` | 支持 Model Context Protocol 加载外部工具 |
| TUI 终端界面 | `tui/` | 全屏终端 UI，实时渲染对话和工具输出 |
| 多模型支持 | `anthropic_adapter.py` `openai_adapter.py` `model_registry.py` | 不绑定单一模型，支持 Claude / GPT / 自定义端点 |

## 核心模块详解

### 1. Agent 循环 (`agent_loop.py`)

这是整个系统的心脏。工作流程：

```
用户输入 → 构造消息列表 → 发送到 LLM → 解析响应
    ↓
如果包含工具调用 → 执行工具 → 把结果追加到消息 → 重新发送到 LLM
    ↓
重复直到模型返回纯文本（不再调用工具）→ 输出给用户
```

### 2. 工具系统 (`tools/`)

每个工具都是一个标准化的异步函数，接收参数，返回结果：

- **文件操作**: 读文件、写文件、精确编辑（字符串替换）
- **代码搜索**: 正则搜索文件内容、列出文件、目录树
- **命令执行**: 运行 Shell 命令，捕获 stdout/stderr
- **Git 操作**: 封装常用 git 命令
- **Web**: 搜索、抓取网页内容
- **辅助**: JSON/CSV 处理、加密、编码、代码审查

### 3. 记忆系统

三层架构，解决"长对话丢失上下文"的问题：

```
┌─────────────────────────────┐
│  用户级记忆 (User Memory)    │  跨项目持久，存储偏好和通用知识
├─────────────────────────────┤
│  项目级记忆 (Project Memory) │  项目范围内持久，存储架构决策和约定
├─────────────────────────────┤
│  工作记忆 (Working Memory)   │  当前会话，受保护不会被上下文压缩丢弃
└─────────────────────────────┘
```

使用 TF-IDF 算法根据当前对话内容自动检索相关记忆注入上下文。

### 4. 上下文管理 (`context_cybernetics.py`)

上下文窗口是有限资源。MindBuddy 用 PID 控制器（比例-积分-微分）来管理：

- 实时监控上下文使用率
- 接近溢出时自动触发压缩
- 压缩时保护工作记忆不被丢弃
- 预测未来使用趋势，提前做准备

### 5. 会话系统 (`session.py`)

- **持久化**: 会话自动保存，进程退出后可恢复
- **回放**: 重看完整的对话历史和工具调用链
- **检查点**: 每次文件编辑前自动创建检查点
- **回滚**: 撤销错误的编辑，不需要手动 `git checkout`

## 快速开始

```bash
git clone https://github.com/zavoryn/MindBuddy.git
cd MindBuddy
pip install -e .
```

配置 API Key：

```bash
cp .env.example .env
# 编辑 .env，设置 ANTHROPIC_API_KEY 或 OPENAI_API_KEY
```

运行：

```bash
# 交互模式（默认）
mindbuddy

# 无头模式——适合 CI/CD
mindbuddy-headless "帮我写一个 FastAPI 的 hello world"

# HTTP 网关——适合 Web 集成
mindbuddy-gateway

# 定时任务
mindbuddy-cron
```

## 使用示例

启动后直接输入自然语言：

```
你> 帮我看一下 main.py 的入口函数做了什么
（MindBuddy 会读取文件并分析）

你> 把日志级别改成 DEBUG
（MindBuddy 会精确编辑配置文件）

你> 运行测试看看有没有挂的
（MindBuddy 会执行 pytest 并报告结果）

你> /memory
（查看记忆系统的当前状态）

你> /session
（查看当前会话的详细信息）
```

## 项目结构

```
MindBuddy/
├── mindbuddy/                  # 主 Python 包
│   ├── agent_loop.py           # Agent 主循环
│   ├── turn_kernel.py          # 每轮执行的步骤策略
│   ├── main.py                 # CLI 入口
│   ├── session.py              # 会话持久化
│   ├── memory.py               # 三层记忆系统
│   ├── working_memory.py       # 工作记忆（压缩保护）
│   ├── memory_pipeline.py      # 记忆检索和注入
│   ├── context_cybernetics.py  # PID 上下文管理
│   ├── context_compactor.py    # 上下文压缩
│   ├── anthropic_adapter.py    # Claude API 适配器
│   ├── openai_adapter.py       # OpenAI API 适配器
│   ├── model_registry.py       # 模型路由注册
│   ├── mcp.py                  # MCP 协议集成
│   ├── hooks.py                # Hook 事件系统
│   ├── skills.py               # 技能加载
│   ├── permissions.py          # 文件权限管理
│   ├── gateway.py              # HTTP 网关
│   ├── headless.py             # 无头模式
│   ├── cron_runner.py          # 定时任务
│   ├── tools/                  # 工具集（29 个工具）
│   └── tui/                    # 终端 UI（19 个模块）
├── tests/                      # 测试套件
├── benchmarks/                 # 性能基准
├── docs/                       # 文档
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

## Docker

```bash
docker build -t mindbuddy .

# 交互
docker compose run --rm cli

# 网关
docker compose up gateway

# 无头
docker compose run --rm headless "分析这个项目"
```

## 技术栈

- **语言**: Python 3.11+
- **LLM 接入**: Anthropic Messages API / OpenAI Chat Completions API
- **记忆检索**: TF-IDF 向量相似度
- **上下文控制**: PID 控制器 + 预测性溢出保护
- **工具扩展**: Model Context Protocol (MCP)
- **终端 UI**: 全屏 TUI（纯 Python 实现）
- **部署**: Docker 多阶段构建，四种运行模式

## 为什么做这个？

Claude Code 是一个很棒的闭源产品，但它是 TypeScript 实现的，代码不可用。我想用 Python 做一个简化版，让我能：

1. **学习 Agent 架构** — 通过自己实现来理解 Agent Loop、工具调用、上下文管理的原理
2. **可定制** — 随时添加自己的工具、修改行为、接入不同的模型
3. **本地优先** — 所有数据都在本地，会话、记忆、配置完全可控
4. **可扩展** — 通过 MCP 协议接入外部工具，通过 Hook 系统自定义行为

## 许可证

MIT License
