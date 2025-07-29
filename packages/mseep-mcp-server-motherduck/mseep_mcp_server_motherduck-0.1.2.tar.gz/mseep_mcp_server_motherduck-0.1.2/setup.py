
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-motherduck",
    version="0.5",
    description="A MCP server for MotherDuck and local DuckDB",
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
    install_requires=['mcp>=1.3.0', 'duckdb==1.2.2', 'pandas>=2.0.0', 'tabulate>=0.9.0'],
    keywords=["mseep"] + [],
)
