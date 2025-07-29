
from setuptools import setup, find_packages

setup(
    name="mseep-elasticsearch-mcp-server",
    version="2.0.4",
    description="MCP Server for interacting with Elasticsearch and OpenSearch",
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
    install_requires=['elasticsearch==8.17.2', 'opensearch-py==2.8.0', 'mcp==1.6.0', 'python-dotenv==1.1.0', 'fastmcp==0.4.1', 'anthropic==0.49.0', 'tomli==2.2.1', 'tomli-w==1.2.0'],
    keywords=["mseep"] + [],
)
