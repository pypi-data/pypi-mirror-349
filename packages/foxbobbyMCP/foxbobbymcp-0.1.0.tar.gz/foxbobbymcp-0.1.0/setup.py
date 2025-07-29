from setuptools import setup, find_packages
import os

# 读取 README 文件作为长描述
readme_path = os.path.join(os.path.dirname(__file__), "README.md")
try:
    with open(readme_path, encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "foxbobbyMCP - 多模态大模型MCP服务器。"

setup(
    name="foxbobbyMCP",
    version="0.1.0",
    packages=find_packages(),
    author="foxbobby",
    author_email="your.email@example.com",
    description="支持多种大模型对话/生图/音频的MCP服务器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/foxbobbyMCP",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.7",
    install_requires=[
        "mcp>=1.6.0",
        "requests",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "foxbobbyMCP=foxbobbyMCP.__main__:main",
        ],
    },
) 