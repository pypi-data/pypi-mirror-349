
from setuptools import setup, find_packages

setup(
    name="mseep-fastapi-mcp-sse",
    version="0.1.0",
    description="A working example to create a FastAPI server with SSE-based MCP support",
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
    install_requires=['fastapi>=0.115.11', 'httpx>=0.28.1', 'mcp[cli]>=1.3.0', 'unicorn>=2.1.3'],
    keywords=["mseep"] + [],
)
