# Six-Figure AI Engineer API Server

Backend API server for the Six-Figure AI Engineer application.

## Setup

### 1. 安装 Supabase CLI

**使用 Homebrew（推荐）：**

```bash
brew install supabase/tap/supabase
```

**或使用 npm：**

```bash
npm install -g supabase
```

**或使用 npx（无需全局安装）：**

```bash
npx supabase
```

### 2. 安装 Python 依赖

使用 Poetry 安装依赖：

```bash
poetry install
```

## Running

**重要：** 必须使用 Poetry 环境运行，以确保所有依赖都已正确安装。

启动服务器（推荐方式）：

```bash
poetry run python main.py
```

或者先激活 Poetry 虚拟环境，然后运行：

```bash
poetry shell
python main.py
```

服务器将在 `http://localhost:8000` 上运行

## Environment Variables

Create a `.env` file with the following variables:

```
SUPABASE_API_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
```
