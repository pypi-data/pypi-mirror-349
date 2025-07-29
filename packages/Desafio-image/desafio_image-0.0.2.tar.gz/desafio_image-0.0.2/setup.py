import os
from pathlib import Path
from setuptools import setup, find_packages

# Obtém o diretório base do projeto
BASE_DIR = Path(__file__).parent.resolve()

try:
    # Tenta ler o README.md
    readme_path = BASE_DIR / "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    print("Arquivo README.md não encontrado!")
    long_description = ""

try:
    # Tenta ler o requirements.txt
    requirements_path = BASE_DIR / "requirements.txt"
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    print("Arquivo requirements.txt não encontrado!")
    requirements = []

setup(
    name="Desafio_image",
    version="0.0.2",
    author="Jacqueline",
    description="Desafio de processamento de imagem usando Skimage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tiemi/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)