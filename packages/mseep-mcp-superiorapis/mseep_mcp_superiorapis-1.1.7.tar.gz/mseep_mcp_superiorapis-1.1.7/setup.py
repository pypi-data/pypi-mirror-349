
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-superiorapis",
    version="1.1.5",
    description="This project is a Python-based **MCP Server** that dynamically fetches plugin definitions from **SuperiorAPIs** and auto-generates MCP tool functions based on OpenAPI schemas.",
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
    install_requires=['mcp>=1.5.0', 'aiohttp>=3.11.0'],
    keywords=["mseep"] + [],
)
