# README.es.md

---

# AI Git Assistant 🤖📦

[![PyPI version](https://img.shields.io/pypi/v/ai-git-assistant)](https://pypi.org/project/ai-git-assistant/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Asistente inteligente para Git que automatiza la creación de commits semánticos y genera plantillas para Pull Requests, con soporte para análisis de cambios y sugerencias basadas en IA.

## ✨ Características principales

- 🧠 **Sugerencias de commits inteligentes** usando ML (Naive Bayes + TF-IDF)
- 📝 **Generación automática de mensajes** con múltiples enfoques:
  - Basado en tipo de archivo
  - Basado en cambios realizados
  - Basado en temática del código
- 🔍 **Detección automática** de archivos modificados (staged/unstaged/untracked)
- 📊 **Análisis de cambios** por tipo de archivo (código, docs, tests, etc.)
- 📑 **Plantilla de PR** con:
  - Listado organizado de archivos modificados
  - Sección para consideraciones de testing
  - Tabla de aplicaciones compatibles
- 🛠️ **Soporte para SQL** con detección especial de archivos .sql
- 🌍 **Interfaz en español** (fácil de internacionalizar)

---

## 📦 Instalación

```bash
pip install ai-git-assistant
```

O instala desde el código fuente:

```bash
https://github.com/LuisGH28/git_assitant.git
cd git_assitant
pip install .
```

---

## 🏗️ Estructura del proyecto

```
ai-git-assistant/
├── __init__.py
├── __main__.py            # Lógica principal
├── requirements.txt       # Dependencias
tests/
├── tests_cli.py           # Tests de interfaz
└── tests_git_utils.py     # Tests de funcionalidad Git
```

## 🛠 Instalación

Clona el repositorio y agrega el archivo git_assistant a tu repositorio en el que estas trabajando

```
https://github.com/LuisGH28/git_assitant.git
cd git_assitant
pip install .
```

---

## 🎥 Demo

Demo animado

![demo](assets/ai-git-assistan.git)

Resultado de la sugerencia del PR

![result](assets/pr_suggest1.png)

![result](assets/pr_suggest2.png)

**Nota:** debes estar en la raiz del proyecto, como se muestra en el gif, si todo tu proyecto esta en la carpeta ejemplo en la terminal debes ubicarte en el ejemplo y ahi puedes ejecutar con el comando ai-git-assistant

---

## 📁 Estructura del Proyecto

```
ai-git-assistant/
├── __init__.py
├── __main__.py            # Lógica principal
├── requirements.txt       # Dependencias
tests/
├── tests_cli.py           # Tests de interfaz
└── tests_git_utils.py     # Tests de funcionalidad Git

```

---

## 📌 Requisitos

* Python 3.8+
* Git instalado y configurado
* Dependencias:
  * scikit-learn
  * joblib

---

## 🛠️ Desarrollo

1. Clona el repositorio
2. Crea un entorno virtual:

```
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

4. Instala dependencias:

```
pip install -e ".[dev]"
```

4. Ejecuta tests:

```
pytest
```

---

## 🤖 Roadmap

* Soporte para más lenguajes (i18n)
* Integración con APIs de GitHub/GitLab
* Modo no-interactivo para CI/CD
* Plugin para editores (VSCode, PyCharm)

---

## 🎉 ¡Disponible en PyPI!

```
pip install ai-git-assistant
```
