# create-uv-project

<div align="center">

![UV Project Creator](https://raw.githubusercontent.com/yourusername/create-uv-project/main/assets/logo.png)

[![PyPI version](https://badge.fury.io/py/create-uv-project.svg)](https://badge.fury.io/py/create-uv-project)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/pypi/pyversions/create-uv-project)](https://pypi.org/project/create-uv-project/)

</div>

---

🚀 `create-uv-project` 是一个革命性的 Python 项目脚手架工具，专为现代 Python 开发者打造。它利用 [UV](https://github.com/astral-sh/uv) 包管理器的强大功能，帮助您在几秒钟内创建一个完全配置好的 Python 项目。

## ✨ 特性

- 🎯 **零配置**: 一键创建标准化的 Python 项目结构
- 🔋 **电池已包含**: 预配置了最佳实践和常用工具
- 🚄 **极速依赖安装**: 采用 UV 超快的包管理能力
- 📦 **现代化工具链**: 集成 Poetry/PDM 风格的依赖管理
- 🛡️ **类型检查**: 默认支持 type hints 和 mypy
- 🧪 **测试就绪**: 预置 pytest 配置
- 📝 **文档模板**: 自动生成项目文档框架

## 🚀 快速开始

### 安装

```bash
pip install create-uv-project
```

或者使用 UV（推荐）：

```bash
uv pip install create-uv-project
```

### 使用方法

创建新项目：

```bash
create-uv-project my-awesome-project
```

使用模板创建：

```bash
create-uv-project my-awesome-project --template fastapi
```

## 📖 可用模板

- `basic`: 基础 Python 项目结构
- `cli`: 命令行工具项目
- `fastapi`: FastAPI Web 应用
- `library`: Python 库项目
- `flask`: Flask Web 应用

## 🎨 项目结构

```
my-awesome-project/
├── src/
│   └── my_awesome_project/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── test_main.py
├── docs/
│   └── index.md
├── README.md
├── pyproject.toml
├── .gitignore
```

## 🛠️ 开发者指南

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/create-uv-project.git
cd create-uv-project
```

2. 安装依赖：
```bash
uv pip install -e ".[dev]"
```

3. 运行测试：
```bash
pytest
```

## 🤝 贡献指南

我们欢迎所有形式的贡献，无论是新功能、文档改进还是错误报告。请查看我们的 [贡献指南](CONTRIBUTING.md) 了解更多信息。

## 📜 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🌟 致谢

- [UV](https://github.com/astral-sh/uv) - 超快的 Python 包管理器
- [所有贡献者](https://github.com/yourusername/create-uv-project/graphs/contributors)

---

<div align="center">
如果这个项目对您有帮助，请考虑给它一个星标 ⭐️
</div>
