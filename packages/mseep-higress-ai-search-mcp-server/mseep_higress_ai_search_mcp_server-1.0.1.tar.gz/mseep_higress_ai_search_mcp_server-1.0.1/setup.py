
from setuptools import setup, find_packages

setup(
    name="mseep-higress-ai-search-mcp-server",
    version="1.0.0",
    description="Higress ai-search MCP Server",
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
    install_requires=['fastmcp>=0.4.1', 'httpx>=0.24.0', 'tomli>=2.2.1', 'tomli-w>=1.2.0'],
    keywords=["mseep"] + [],
)
