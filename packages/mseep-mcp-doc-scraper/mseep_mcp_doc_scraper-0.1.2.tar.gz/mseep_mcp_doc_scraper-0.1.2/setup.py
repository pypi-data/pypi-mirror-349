
from setuptools import setup, find_packages

setup(
    name="mseep-mcp_doc_scraper",
    version="0.1.0",
    description="MCP server for scraping documentation",
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
    install_requires=['aiohttp', 'mcp', 'pydantic'],
    keywords=["mseep"] + [],
)
