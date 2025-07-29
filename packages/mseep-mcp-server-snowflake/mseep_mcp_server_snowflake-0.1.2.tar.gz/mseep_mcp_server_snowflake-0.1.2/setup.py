
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-snowflake",
    version="0.1.0",
    description="MCP server for interacting with Snowflake databases / 用于与 Snowflake 数据库交互的 MCP 服务器",
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
    install_requires=['mcp>=1.0.0', 'snowflake-connector-python', 'python-dotenv'],
    keywords=["mseep"] + [],
)
