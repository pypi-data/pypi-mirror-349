
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-google-suite",
    version="0.1.1",
    description="MCP server for Google Workspace operations (Drive, Docs, and Sheets)",
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
    install_requires=['google-auth-oauthlib>=1.0.0', 'google-auth>=2.22.0', 'google-api-python-client>=2.95.0', 'mcp>=0.1.0', 'pydantic>=2.0.0', 'uvicorn>=0.23.0', 'starlette>=0.31.0', 'tabulate>=0.9.0'],
    keywords=["mseep"] + ['mcp', 'google-workspace', 'google-drive', 'google-docs', 'google-sheets', 'ai', 'cursor'],
)
