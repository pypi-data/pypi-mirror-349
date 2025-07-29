from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ai-git-assistant",
    version="1.0.0",
    author="Luis Gonzalez",
    author_email="luisgnzhdz@gmail.com",
    description="Asistente inteligente para automatizar tareas de Git y GitHub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LuisGH28/git_assistant",  # Corregido
    packages=find_packages(),
    include_package_data=True,  # Importante para incluir model.pkl
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
    install_requires=[
        "scikit-learn",
        "numpy",
        "joblib",
    ],
    entry_points={
        "console_scripts": [
            "ai-git-assistant=ai_git_assistant.__main__:main",  # Coherente con nombre de paquete
        ],
    },
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=3.0",
            "pytest-mock>=3.0",
            "black>=22.0",
        ]
    }
)