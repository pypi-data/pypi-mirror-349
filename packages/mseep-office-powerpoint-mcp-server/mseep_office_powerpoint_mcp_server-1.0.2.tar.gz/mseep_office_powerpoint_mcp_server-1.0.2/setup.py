
from setuptools import setup, find_packages

setup(
    name="mseep-office-powerpoint-mcp-server",
    version="1.0.0",
    description="MCP Server for PowerPoint manipulation using python-pptx",
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
    install_requires=['python-pptx>=0.6.21', 'mcp[cli]>=1.3.0'],
    keywords=["mseep"] + [],
)
