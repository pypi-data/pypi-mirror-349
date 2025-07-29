
from setuptools import setup, find_packages

setup(
    name="mseep-fastapi-mcp",
    version="0.3.4",
    description="Automatic MCP server generator for FastAPI applications - converts FastAPI endpoints to MCP tools for LLM integration",
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
    install_requires=['fastapi>=0.100.0', 'typer>=0.9.0', 'rich>=13.0.0', 'mcp>=1.8.1', 'pydantic>=2.0.0', 'pydantic-settings>=2.5.2', 'uvicorn>=0.20.0', 'httpx>=0.24.0', 'requests>=2.25.0', 'tomli>=2.2.1'],
    keywords=["mseep"] + ['fastapi', 'openapi', 'mcp', 'llm', 'claude', 'ai', 'tools', 'api', 'conversion', 'modelcontextprotocol'],
)
