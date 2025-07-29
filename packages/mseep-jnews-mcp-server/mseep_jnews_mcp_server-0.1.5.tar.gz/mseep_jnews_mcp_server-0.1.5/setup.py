
from setuptools import setup, find_packages

setup(
    name="mseep-jnews-mcp-server",
    version="0.1.3",
    description="一个提供热点新闻头条信息功能的模型上下文协议（Model Context Protocol）服务器。",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp[cli]>=1.4.1'],
    keywords=["mseep"] + [],
)
