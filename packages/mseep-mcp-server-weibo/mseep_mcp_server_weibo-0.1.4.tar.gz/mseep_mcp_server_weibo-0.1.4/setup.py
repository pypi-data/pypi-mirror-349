
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-weibo",
    version="0.1.2",
    description="A MCP Server for Weibo",
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
    install_requires=['httpx', 'mcp[cli]'],
    keywords=["mseep"] + ['MCP', 'Model Context Protocol', 'Weibo', 'Python', 'Social Networks'],
)
