
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-things3",
    version="0.1.0",
    description="A server implementation for interacting with Things3 app on macOS through Claude AI",
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
    install_requires=['flask'],
    keywords=["mseep"] + [],
)
