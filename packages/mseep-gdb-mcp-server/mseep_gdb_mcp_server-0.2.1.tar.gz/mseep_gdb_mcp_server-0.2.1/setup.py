
from setuptools import setup, find_packages

setup(
    name="mseep-gdb-mcp-server",
    version="0.2.0",
    description="GDB Model Context Protocol Server for AI-assisted debugging",
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
    install_requires=['fastmcp>=0.1.0', 'pexpect>=4.8.0'],
    keywords=["mseep"] + [],
)
