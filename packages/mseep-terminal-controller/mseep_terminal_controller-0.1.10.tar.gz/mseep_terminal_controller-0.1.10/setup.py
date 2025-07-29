
from setuptools import setup, find_packages

setup(
    name="mseep-terminal-controller",
    version="0.1.8",
    description="A Model Context Protocol (MCP) server for secure terminal command execution and file system operations",
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
    install_requires=['mcp[cli]>=1.3.0', 'httpx>=0.25.0'],
    keywords=["mseep"] + ['terminal', 'mcp', 'claude', 'command-line'],
)
