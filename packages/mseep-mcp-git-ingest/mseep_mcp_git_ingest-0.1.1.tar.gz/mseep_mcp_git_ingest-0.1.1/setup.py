
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-git-ingest",
    version="0.1.0",
    description="MCP Git Ingest: GitHub repository analysis tools",
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
    install_requires=['fastmcp', 'gitpython', 'uvicorn'],
    keywords=["mseep"] + [],
)
