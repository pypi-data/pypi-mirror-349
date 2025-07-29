
from setuptools import setup, find_packages

setup(
    name="mseep-azure-agent-mcp-server",
    version="0.1.0",
    description="Azure AI Agent Service MCP Server",
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
    install_requires=['mcp[cli]~=1.4.1', 'azure-identity~=1.21.0', 'python-dotenv~=1.0.1', 'azure-ai-projects~=1.0.0b7', 'aiohttp>=3.11.14'],
    keywords=["mseep"] + [],
)
