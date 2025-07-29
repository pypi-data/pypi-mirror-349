
from setuptools import setup, find_packages

setup(
    name="mseep-mcps",
    version="0.1.0",
    description="Model Context Protocol server for continue.dev",
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
    install_requires=['fastmcp>=0.4.1'],
    keywords=["mseep"] + [],
)
