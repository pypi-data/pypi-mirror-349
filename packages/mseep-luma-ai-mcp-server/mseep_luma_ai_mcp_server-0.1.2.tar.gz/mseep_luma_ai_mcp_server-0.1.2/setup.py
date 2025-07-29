
from setuptools import setup, find_packages

setup(
    name="mseep-luma-ai-mcp-server",
    version="0.1.0",
    description="MCP server for Luma AI video generation",
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
    install_requires=['httpx>=0.24.0', 'pydantic>=2.0.0', 'python-dotenv>=1.0.0', 'click>=8.1.0', 'mcp>=0.2.0'],
    keywords=["mseep"] + [],
)
