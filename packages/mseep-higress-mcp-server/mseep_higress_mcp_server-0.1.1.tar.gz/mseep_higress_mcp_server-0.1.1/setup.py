
from setuptools import setup, find_packages

setup(
    name="mseep-higress-mcp-server",
    version="0.1.0",
    description="MCP Server for Higress",
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
    install_requires=['uvicorn>=0.24.0', 'starlette>=0.27.0', 'requests>=2.31.0', 'mcp[cli]>=1.2.1', 'openai>=1.61.0', 'langchain-mcp-adapters>=0.0.5', 'langgraph>=0.3.16', 'langchain-openai>=0.3.9', 'fastmcp>=0.4.1', 'python-dotenv>=1.0.1'],
    keywords=["mseep"] + [],
)
