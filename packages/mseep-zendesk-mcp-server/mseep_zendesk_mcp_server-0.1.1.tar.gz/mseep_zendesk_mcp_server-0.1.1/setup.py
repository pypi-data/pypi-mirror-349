
from setuptools import setup, find_packages

setup(
    name="mseep-zendesk-mcp-server",
    version="0.1.0",
    description="A simple Zendesk MCP server",
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
    install_requires=['mcp>=1.1.2', 'python-dotenv>=1.0.1', 'zenpy>=2.0.56'],
    keywords=["mseep"] + [],
)
