
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-pox",
    version="0.1.0",
    description="A sample POX MCP server",
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
    install_requires=['mcp[cli]>=1.5.0', 'requests>=2.32.3'],
    keywords=["mseep"] + [],
)
