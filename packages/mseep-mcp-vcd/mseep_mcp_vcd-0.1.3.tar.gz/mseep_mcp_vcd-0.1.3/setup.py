
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-vcd",
    version="0.1.1",
    description="A model context protocol (MCP) server for value change dump (VCD) waveforms.",
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
    install_requires=['httpx>=0.28.1', 'ipykernel>=6.29.5', 'mcp>=1.1.2'],
    keywords=["mseep"] + [],
)
