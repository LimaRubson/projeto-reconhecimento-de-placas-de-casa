from setuptools import setup, find_packages

setup(
    name="reconhecimento_placas",
    version="1.0",
    description="Projeto de Reconhecimento de Placas de Casas utilizando processamento de imagens e OCR",
    author="Seu Nome",
    author_email="seuemail@exemplo.com",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "pytesseract",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "reconhecimento_placas=src.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
