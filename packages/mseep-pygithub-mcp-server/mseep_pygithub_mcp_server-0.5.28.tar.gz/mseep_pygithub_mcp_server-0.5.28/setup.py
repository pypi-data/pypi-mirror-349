
from setuptools import setup, find_packages

setup(
    name="mseep-pygithub-mcp-server",
    version="0.5.27",
    description="GitHub MCP Server using PyGithub",
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
    install_requires=['PyGithub>=2.1.1', 'mcp>=1.1.3', 'pydantic>=2.9.2'],
    keywords=["mseep"] + [],
)
