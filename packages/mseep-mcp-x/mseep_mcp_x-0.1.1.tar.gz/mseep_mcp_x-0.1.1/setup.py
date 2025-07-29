
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-x",
    version="0.1.0",
    description="This is MCP to fetch Tweets using RAPID API Client",
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
    install_requires=['httpx>=0.28.1', 'mcp[cli]>=1.4.1'],
    keywords=["mseep"] + [],
)
