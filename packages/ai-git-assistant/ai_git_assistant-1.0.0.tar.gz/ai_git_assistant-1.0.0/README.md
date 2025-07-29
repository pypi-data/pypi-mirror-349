# AI Git Assistant 🤖📦

[![PyPI version](https://img.shields.io/pypi/v/ai-git-assistant)](https://pypi.org/project/ai-git-assistant/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://file+.vscode-resource.vscode-cdn.net/Users/macbook/Documents/gitAssistant/LICENSE)

📄 This README is also available in: [Español](README.es.md)

Intelligent Git assistant that automates semantic commit creation and generates Pull Request templates, with support for change analysis and AI-based suggestions.

## ✨ Key Features

- 🧠 **Smart commit suggestions** using ML (Naive Bayes + TF-IDF)
- 📝 **Automatic message generation** with multiple approaches:
  - File type-based
  - Change-based
  - Code theme-based
- 🔍 **Automatic detection** of modified files (staged/unstaged/untracked)
- 📊 **Change analysis** by file type (code, docs, tests, etc.)
- 📑 **PR template** with:
  - Organized list of modified files
  - Testing considerations section
  - Compatible applications table
- 🛠️ **SQL support** with special .sql file detection
- 🌍 **Spanish interface** (easy to internationalize)

---

## 📦 Installation

```bash
pip install ai-git-assistant
```

Or install from source:

```bash
https://github.com/LuisGH28/git_assitant.git
cd git_assitant
pip install .
```

---

## 🏗️ Project Structure

```
ai-git-assistant/
├── __init__.py
├── __main__.py            # Main logic
├── requirements.txt       # Dependencies
tests/
├── tests_cli.py           # Interface tests
└── tests_git_utils.py     # Git functionality tests

```

---

## 📌 Requirements

* Python 3.8+
* Git installed and configured
* Dependencies:
  * scikit-learn
  * joblib

---

## 🛠️ Development

1. Clone the repository
2. Create a virtual environment:

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```
pip install -e ".[dev]"
```

4. Run tests:

```
pytest
```

---

## 🤖 Roadmap

* Support for more languages (i18n)
* Integration with GitHub/GitLab APIs
* Non-interactive mode for CI/CD
* Editor plugins (VSCode, PyCharm)

---

## 🎉 Available on PyPI!

```
pip install ai-git-assistant
```
