from setuptools import setup, find_packages

setup(
    name="pyspeak_command",
    version="3.1.1",
    author="Cícero Higor",
    author_email="higormc2015@gmail.com",
    description="Um utilitário para ler em voz alta e/ou traduzir comandos do terminal, scripts Python, e arquivos de texto",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/higormcarnauba/speak_command",
    packages=find_packages(),  # Encontra automaticamente todos os pacotes
    install_requires=[
        "pyttsx3",
        "pynput",
        "deep_translator",
        "ftfy"
    ],
    entry_points={
        "console_scripts": [
        "scmd=speak_command.main:main",
        "speak_command=speak_command.main:main",
    ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
