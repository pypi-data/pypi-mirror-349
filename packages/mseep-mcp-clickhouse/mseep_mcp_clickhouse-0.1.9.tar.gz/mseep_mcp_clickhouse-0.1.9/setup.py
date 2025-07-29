
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-clickhouse",
    version="0.1.7",
    description="An MCP server for ClickHouse.",
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
    install_requires=['mcp[cli]>=1.3.0', 'python-dotenv>=1.0.1', 'uvicorn>=0.34.0', 'clickhouse-connect>=0.8.16', 'pip-system-certs>=4.0'],
    keywords=["mseep"] + [],
)
