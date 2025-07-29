
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-appwrite",
    version="0.1.4",
    description="MCP (Model Context Protocol) server for Appwrite",
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
    install_requires=['appwrite>=9.0.3', 'docstring-parser>=0.16', 'mcp[cli]>=1.3.0'],
    keywords=["mseep"] + [],
)
