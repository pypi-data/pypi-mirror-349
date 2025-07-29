
from setuptools import setup, find_packages

setup(
    name="mseep-cmd-line-mcp",
    version="0.5.0",
    description="Command-line MCP server for safe command execution",
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
    install_requires=['mcp>=1.6.0'],
    keywords=["mseep"] + [],
)
