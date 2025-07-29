
from setuptools import setup, find_packages

setup(
    name="mseep-lancedb-mcp",
    version="0.1.0",
    description="LanceDB MCP Server for vector database operations",
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
    install_requires=['lancedb>=0.12.0', 'pydantic>=2.0', 'mcp>=1.1.2', 'numpy>=1.24.0', 'fastapi>=0.100.0', 'uvicorn>=0.22.0', 'tomlkit>=0.12.0'],
    keywords=["mseep"] + [],
)
