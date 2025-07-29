
from setuptools import setup, find_packages

setup(
    name="mseep-baidu-mcp-server",
    version="0.1.6",
    description="MCP Server for searching via Baidu",
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
    install_requires=['beautifulsoup4>=4.13.3', 'httpx>=0.28.1', 'mcp[cli]>=1.3.0', 'readabilipy>=0.3.0', 'markdownify>=1.1.0'],
    keywords=["mseep"] + [],
)
