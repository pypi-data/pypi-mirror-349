
from setuptools import setup, find_packages

setup(
    name="mseep-memory-mcp-server",
    version="0.2.0",
    description="MCP server for managing Claude's memory and knowledge graph",
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
    install_requires=['aiofiles', 'loguru>=0.7.3', 'mcp[cli]>=1.2.0', 'memory-mcp-server', 'ruff>=0.9.4', 'thefuzz[speedup]>=0.20.0'],
    keywords=["mseep"] + [],
)
