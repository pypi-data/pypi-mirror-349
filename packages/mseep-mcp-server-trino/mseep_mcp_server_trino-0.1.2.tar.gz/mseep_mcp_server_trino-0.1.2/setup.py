
from setuptools import setup, find_packages

setup(
    name="mseep-mcp_server_trino",
    version="0.1.1",
    description="A Model Context Protocol (MCP) server that enables secure interaction with Trino. This server allows AI assistants to list tables, read data, and execute SQL queries through a controlled interface, making data exploration and analysis safer and more structured.",
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
    install_requires=['mcp>=1.0.0', 'trino==0.333.0'],
    keywords=["mseep"] + [],
)
