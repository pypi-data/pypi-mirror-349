
from setuptools import setup, find_packages

setup(
    name="mseep-keboola-mcp-server",
    version="0.18.0",
    description="MCP server for interacting with Keboola Connection",
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
    install_requires=['mcp[cli] == 1.6.0', 'kbcstorage ~= 0.9', 'httpx ~= 0.28', 'google-cloud-bigquery ~= 3.31'],
    keywords=["mseep"] + [],
)
