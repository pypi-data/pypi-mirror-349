# 项目模板结构

本文档展示了使用 `create-uv-project` 生成的不同类型项目的典型目录结构。所有项目均设计为使用 `uv` 作为包管理和工作流工具。

## 1. Basic 模板

一个基础的 Python 项目结构，包含一个简单的可执行入口点。适合小型应用或作为更复杂项目的起点。

```
project_name/
├── .gitignore
├── pyproject.toml
├── README.md
├── src/
│   └── project_slug/      # 例如: my_app/
│       ├── __init__.py
│       └── main.py        # 包含一个简单的 main() 函数
└── tests/
    ├── __init__.py
    └── test_main.py
```

## 2. CLI 模板

专为命令行界面 (CLI) 工具设计的项目结构。可能预置了参数解析库的集成。

```
project_name/
├── .gitignore
├── pyproject.toml       # 包含 [project.scripts] 指向 CLI 入口
├── README.md
├── src/
│   └── project_slug/      # 例如: my_cli_app/
│       ├── __init__.py
│       ├── cli.py         # 主要 CLI逻辑 (例如使用 Typer, Click)
│       └── commands/      # (可选) 存放子命令模块
│           ├── __init__.py
│           └── example_command.py
└── tests/
    ├── __init__.py
    └── test_cli.py
```

## 3. FastAPI 模板

用于构建 FastAPI Web 应用程序的项目结构。

```
project_name/
├── .env.example           # 示例环境变量配置
├── .gitignore
├── pyproject.toml       # 依赖: fastapi, uvicorn
├── README.md
├── src/
│   └── project_slug/      # 例如: my_fastapi_app/
│       ├── __init__.py
│       ├── main.py        # FastAPI 应用实例和主要启动逻辑
│       ├── core/
│       │   ├── __init__.py
│       │   └── config.py  # 应用配置
│       ├── models/
│       │   ├── __init__.py
│       │   └── item.py    # Pydantic 模型示例
│       ├── routers/
│       │   ├── __init__.py
│       │   └── items.py   # API 路由示例
│       └── schemas/       # (可选) 或者直接在 models/ 中定义请求/响应体
│           ├── __init__.py
│           └── item.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_items_api.py
```

## 4. Library 模板

用于开发 Python 库的项目结构。通常不包含直接的可执行入口点。

```
project_name/
├── .gitignore
├── pyproject.toml       # 主要配置库的元数据和依赖
├── README.md
├── src/
│   └── project_slug/      # 例如: my_library/
│       ├── __init__.py    # 暴露库的公共 API
│       └── core_module.py # 库的核心功能模块
└── tests/
    ├── __init__.py
    └── test_core_module.py
```

## 5. Flask 模板

用于构建 Flask Web 应用程序的项目结构。

```
project_name/
├── .env.example           # 示例环境变量配置
├── .gitignore
├── pyproject.toml       # 依赖: flask
├── README.md
├── instance/              # Flask 实例文件夹 (例如, SQLite DB, 配置文件)
│   └── config.py
├── src/
│   └── project_slug/      # 例如: my_flask_app/
│       ├── __init__.py    # 应用工厂 (create_app)
│       ├── routes.py      # (或 views.py) 定义应用路由
│       ├── models.py      # (可选) 数据库模型 (例如使用 SQLAlchemy)
│       ├── forms.py       # (可选) WTForms 表单定义
│       ├── static/        # 静态文件 (CSS, JavaScript, 图片)
│       │   └── css/
│       │       └── style.css
│       └── templates/     # Jinja2 模板
│           ├── base.html
│           └── index.html
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_app.py
``` 