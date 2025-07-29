
from setuptools import setup, find_packages

setup(
    name="mseep-mcp_server_bing",
    version="0.1.0",
    description="MCP server implementation for Bing Search API integration",
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
    install_requires=['python-dotenv>=1.0.1', 'httpx>=0.28.1', 'mcp[cli]>=1.4.1'],
    keywords=["mseep"] + [],
)
