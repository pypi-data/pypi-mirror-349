
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-ical",
    version="0.1.0",
    description="A Model Context Protocol server providing tools for CRUD operations for the mac-os calendar",
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
    install_requires=['loguru>=0.7.3', 'mcp[cli]>=1.2.1', 'pyobjc>=11.0'],
    keywords=["mseep"] + [],
)
