
from setuptools import setup, find_packages

setup(
    name="mseep-mcpo",
    version="0.0.14",
    description="A simple, secure MCP-to-OpenAPI proxy server",
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
    install_requires=['click>=8.1.8', 'fastapi>=0.115.12', 'mcp>=1.8.0', 'mcp[cli]>=1.8.0', 'passlib[bcrypt]>=1.7.4', 'pydantic>=2.11.1', 'pyjwt[crypto]>=2.10.1', 'python-dotenv>=1.1.0', 'typer>=0.15.2', 'uvicorn>=0.34.0'],
    keywords=["mseep"] + [],
)
