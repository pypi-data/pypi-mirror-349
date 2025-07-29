
from setuptools import setup, find_packages

setup(
    name="mseep-fused-mcp",
    version="0.1.0",
    description="Fused MCP: Setting up MCP Servers for Data Scientists",
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
    install_requires=['anthropic>=0.49.0', 'fused[all]>=1.15.0', 'jupyterlab>=4.3.6', 'mcp[cli]>=1.4.1', 'python-dotenv>=1.0.1'],
    keywords=["mseep"] + [],
)
