
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-tinybird",
    version="1.0.2",
    description="An MCP server to interact with a Tinybird Workspace from any MCP client.",
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
    install_requires=['httpx>=0.27.2', 'mcp>=1.0.0', 'python-dotenv>=1.0.1', 'tinybird-python-sdk>=0.1.6', 'uvicorn>=0.27.0', 'starlette>=0.36.0'],
    keywords=["mseep"] + [],
)
