
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-qdrant",
    version="0.7.1",
    description="MCP server for retrieving context from a Qdrant vector database",
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
    install_requires=['mcp[cli]>=1.3.0', 'fastembed>=0.6.0', 'qdrant-client>=1.12.0', 'pydantic>=2.10.6'],
    keywords=["mseep"] + [],
)
