
from setuptools import setup, find_packages

setup(
    name="mseep-malaysia-prayer-time",
    version="0.2.0",
    description="Malaysia Prayer Time MCP Server for Claude Desktop",
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
    install_requires=['httpx>=0.27.0', 'pydantic>=2.0.0,<3.0.0', 'PyYAML>=6.0,<7.0', 'mcp>=1.2.0', 'mcp[cli]>=1.2.0'],
    keywords=["mseep"] + [],
)
