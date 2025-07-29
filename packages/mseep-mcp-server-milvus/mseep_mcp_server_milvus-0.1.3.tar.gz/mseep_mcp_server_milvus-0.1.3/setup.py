
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-milvus",
    version="0.1.1",
    description="MCP server for Milvus",
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
    install_requires=['mcp[cli]>=1.1.2', 'pymilvus>=2.5.1', 'click>=8.0.0', 'ruff>=0.11.0', 'dotenv>=0.9.9'],
    keywords=["mseep"] + [],
)
