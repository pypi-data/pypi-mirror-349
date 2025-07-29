
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-python-interpreter",
    version="1.1",
    description="MCP server for Python code execution and environment management",
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
    install_requires=['mcp[cli]>=1.6.0'],
    keywords=["mseep"] + [],
)
