
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-duckdb",
    version="1.1.0",
    description="A DuckDB MCP server",
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
    install_requires=['duckdb>=1.1.3', 'mcp>=1.0.0'],
    keywords=["mseep"] + [],
)
