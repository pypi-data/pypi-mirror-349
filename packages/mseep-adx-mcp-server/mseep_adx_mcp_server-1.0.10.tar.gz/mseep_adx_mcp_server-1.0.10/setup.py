
from setuptools import setup, find_packages

setup(
    name="mseep-adx_mcp_server",
    version="1.0.9",
    description="MCP server for Azure Data Explorer integration",
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
    install_requires=['mcp[cli]', 'azure-kusto-data', 'azure-identity', 'python-dotenv', 'pyproject-toml>=0.1.0'],
    keywords=["mseep"] + [],
)
