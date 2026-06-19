# MindBuddy

<p align="center">
  <strong>A Simplified Claude Code Implementation in Python</strong>
</p>

<p align="center">
  MindBuddy is a lightweight open-source reimplementation of Claude Code's core architecture.<br>
  It reimplements the key capabilities: Agent loop, tool calling, context management, session persistence, and memory system — all in Python.
</p>

<p align="center">
  <a href="./README.md">中文</a>
  |
  <a href="https://github.com/zavoryn/MindBuddy">GitHub</a>
</p>

<p align="center">
  <img alt="CI" src="https://github.com/zavoryn/MindBuddy/actions/workflows/ci.yml/badge.svg">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/license-MIT-blue?style=flat-square">
</p>

---

## What is this?

If you've used Claude Code (the `claude` CLI tool from Anthropic), you know it can:

- Read your code files
- Edit and modify code
- Run terminal commands
- Search your codebase
- Remember context across long conversations

**MindBuddy is a Python implementation of these capabilities.** It's not an API wrapper or a chat shell — it's a complete Agent runtime, from tool calling to context management to session persistence.

## Quick Start

```bash
git clone https://github.com/zavoryn/MindBuddy.git
cd MindBuddy
pip install -e .
```

Configure your API key:

```bash
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY or OPENAI_API_KEY
```

Run:

```bash
# Interactive mode (default)
mindbuddy

# Headless mode — great for CI/CD
mindbuddy-headless "Write a FastAPI hello world"

# HTTP gateway — for web integration
mindbuddy-gateway

# Scheduled tasks
mindbuddy-cron
```

## Claude Code Feature Mapping

| Claude Code Feature | MindBuddy Implementation | Description |
| --- | --- | --- |
| Agent Loop | `agent_loop.py` | Core loop: user input → LLM call → tool parsing → execution → repeat |
| Read/Edit/Write | `tools/read_file.py` `tools/edit_file.py` `tools/write_file.py` | File I/O and precise string replacement editing |
| Grep/Glob | `tools/grep_files.py` `tools/list_files.py` `tools/file_tree.py` | Code search and file discovery |
| Bash | `tools/run_command.py` | Shell command execution with timeout control |
| Context Compaction | `context_compactor.py` | Auto-compress history when context overflows |
| Memory System | `memory.py` `working_memory.py` `memory_pipeline.py` | 3-tier memory with TF-IDF retrieval |
| Session Persistence | `session.py` | Save, resume, replay, and rollback sessions |
| MCP Tools | `mcp.py` `skills.py` | Model Context Protocol for external tools |
| TUI | `tui/` | Full-screen terminal UI with real-time rendering |
| Multi-Model | `anthropic_adapter.py` `openai_adapter.py` | Claude / GPT / custom endpoints |

## Architecture

### Agent Loop (`agent_loop.py`)

```
User Input → Build Messages → Send to LLM → Parse Response
    ↓
Tool Calls? → Execute Tool → Append Result → Resend to LLM
    ↓
Pure Text Response → Output to User
```

### Memory System

Three-tier architecture to solve the "long conversation loses context" problem:

- **User Memory** — Persistent across projects, stores preferences
- **Project Memory** — Project-scoped, stores architecture decisions
- **Working Memory** — Current session, protected from context compaction

Uses TF-IDF to automatically retrieve relevant memories based on the current conversation.

### Context Management (`context_cybernetics.py`)

Context window is a finite resource. MindBuddy uses a PID controller to manage it:

- Monitor context usage in real-time
- Auto-trigger compaction when approaching overflow
- Protect working memory during compaction
- Predict future usage trends

## Project Structure

```
MindBuddy/
├── mindbuddy/                  # Main Python package
│   ├── agent_loop.py           # Agent main loop
│   ├── turn_kernel.py          # Per-turn step policy
│   ├── session.py              # Session persistence
│   ├── memory.py               # 3-tier memory system
│   ├── context_cybernetics.py  # PID context management
│   ├── anthropic_adapter.py    # Claude API adapter
│   ├── openai_adapter.py       # OpenAI API adapter
│   ├── mcp.py                  # MCP protocol integration
│   ├── tools/                  # 29 built-in tools
│   └── tui/                    # Terminal UI (19 modules)
├── tests/                      # Test suite
├── benchmarks/                 # Performance benchmarks
├── pyproject.toml
├── Dockerfile
└── docker-compose.yml
```

## Docker

```bash
docker build -t mindbuddy .
docker compose run --rm cli
docker compose up gateway
```

## Why?

Claude Code is a great closed-source product, but it's written in TypeScript and the code isn't available. I wanted a simplified Python version to:

1. **Learn Agent architecture** — Understand Agent Loop, tool calling, and context management by building it
2. **Customizable** — Add your own tools, modify behavior, swap models
3. **Local-first** — All data stays local, full control over sessions and memory
4. **Extensible** — MCP protocol for external tools, Hook system for custom behavior

## License

MIT License
