
from setuptools import setup, find_packages

setup(
    name="mseep-illumio-mcp",
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
    install_requires=['illumio>=1.1.3', 'logging>=0.4.9.6', 'mcp>=1.2.0', 'pandas>=2.2.3', 'python-dotenv>=1.0.1'],
    keywords=["mseep"] + [],
)
