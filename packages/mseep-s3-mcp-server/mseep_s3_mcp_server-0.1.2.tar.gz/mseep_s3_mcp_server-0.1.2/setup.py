
from setuptools import setup, find_packages

setup(
    name="mseep-s3-mcp-server",
    version="0.1.0",
    description="A MCP server project",
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
    install_requires=['aioboto3>=13.2.0', 'mcp>=1.0.0', 'python-dotenv>=1.0.1'],
    keywords=["mseep"] + [],
)
