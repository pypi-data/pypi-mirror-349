
from setuptools import setup, find_packages

setup(
    name="mseep-semgrep-mcp",
    version="0.2.0",
    description="MCP Server for using Semgrep to scan code",
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
    install_requires=['mcp>=1.6.0', 'semgrep>=1.117.0'],
    keywords=["mseep"] + ['security', 'static-analysis', 'code-scanning', 'semgrep', 'mcp'],
)
