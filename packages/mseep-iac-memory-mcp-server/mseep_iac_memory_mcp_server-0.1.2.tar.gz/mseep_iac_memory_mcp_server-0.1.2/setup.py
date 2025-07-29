
from setuptools import setup, find_packages

setup(
    name="mseep-iac-memory-mcp-server",
    version="0.1.0",
    description="Custom Memory MCP Server intended to act as a cache between me and the AI about Infrastructure-as-Code information.",
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
    install_requires=['mcp>=1.2.0', 'pydantic>=2.6.1', 'pydantic-core>=2.14.6', 'anyio>=4.8.0', 'jsonschema>=4.21.1', 'pytest-asyncio>=0.23.8'],
    keywords=["mseep"] + [],
)
