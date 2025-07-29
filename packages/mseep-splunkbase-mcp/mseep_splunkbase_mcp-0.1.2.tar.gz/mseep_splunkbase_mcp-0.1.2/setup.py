
from setuptools import setup, find_packages

setup(
    name="mseep-splunkbase-mcp",
    version="0.1.0",
    description="MCP server for Splunkbase",
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
    install_requires=['aiosplunkbase >= 0.1.3', 'mcp[cli]', 'aiofiles'],
    keywords=["mseep"] + [],
)
