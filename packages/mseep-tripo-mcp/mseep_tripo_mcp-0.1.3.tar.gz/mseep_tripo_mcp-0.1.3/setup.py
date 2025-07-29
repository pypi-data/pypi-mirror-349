
from setuptools import setup, find_packages

setup(
    name="mseep-tripo-mcp",
    version="0.1.2",
    description="MCP (Model Control Protocol) integration for Tripo",
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
    install_requires=['tripo3d>=0.2.0', 'mcp[cli]>=1.4.1'],
    keywords=["mseep"] + ['mcp', 'blender', '3d', 'automation'],
)
