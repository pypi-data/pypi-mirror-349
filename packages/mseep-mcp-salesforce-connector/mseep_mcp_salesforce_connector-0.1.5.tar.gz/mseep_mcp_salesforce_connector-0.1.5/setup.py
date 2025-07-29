
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-salesforce-connector",
    version="0.1.3",
    description="A Model Context Protocol (MCP) server implementation for Salesforce integration",
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
    install_requires=['mcp', 'simple-salesforce', 'python-dotenv'],
    keywords=["mseep"] + ['mcp', 'llm', 'salesforce'],
)
