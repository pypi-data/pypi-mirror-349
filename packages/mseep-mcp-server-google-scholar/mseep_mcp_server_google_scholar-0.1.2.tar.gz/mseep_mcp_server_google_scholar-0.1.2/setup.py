
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-google-scholar",
    version="0.1.0",
    description="An MCP server for searching and retrieving articles from Google Scholar",
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
    install_requires=['mcp[cli]>=1.4.1', 'scholarly>=1.7.0', 'asyncio>=3.4.3'],
    keywords=["mseep"] + [],
)
