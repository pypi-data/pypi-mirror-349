
from setuptools import setup, find_packages

setup(
    name="mseep-steampipe-mcp-server",
    version="0.2.1",
    description="A Python MCP server interacting with PostgreSQL, intended for use with Steampipe.",
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
    install_requires=['mcp[cli]>=1.6.0', 'psycopg[binary,pool]>=3.1.0', 'pydantic>=2.0.0', 'click>=8.1.8'],
    keywords=["mseep"] + ['mcp', 'llm', 'postgres', 'postgresql', 'steampipe'],
)
