
from setuptools import setup, find_packages

setup(
    name="mseep-playwright-server",
    version="0.1.0",
    description="\\A MCP server with playwright tools\\",
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
    install_requires=['mcp>=1.1.2', 'playwright'],
    keywords=["mseep"] + [],
)
