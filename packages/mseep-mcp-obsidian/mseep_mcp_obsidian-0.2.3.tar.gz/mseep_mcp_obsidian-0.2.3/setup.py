
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-obsidian",
    version="0.2.1",
    description="MCP server to work with Obsidian via the remote REST plugin",
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
    install_requires=['mcp>=1.1.0', 'python-dotenv>=1.0.1', 'requests>=2.32.3'],
    keywords=["mseep"] + [],
)
