
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-mas-sequential-thinking",
    version="0.2.3",
    description="MCP Agent Implementation for Sequential Thinking",
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
    install_requires=['agno', 'asyncio', 'exa-py', 'python-dotenv', 'mcp', 'groq'],
    keywords=["mseep"] + [],
)
