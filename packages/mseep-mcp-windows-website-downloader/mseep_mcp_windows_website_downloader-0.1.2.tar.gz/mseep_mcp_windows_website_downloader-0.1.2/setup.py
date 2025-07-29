
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-windows-website-downloader",
    version="0.1.0",
    description="Simple MCP server for downloading documentation websites",
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
    install_requires=['aiohttp>=3.8.0', 'beautifulsoup4>=4.9.0', 'mcp-python>=0.1.0', 'lxml>=4.9.0'],
    keywords=["mseep"] + [],
)
