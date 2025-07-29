
from setuptools import setup, find_packages

setup(
    name="mseep-tecton_mcp",
    version="0.1.0",
    description="Tecton MCP server",
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
    install_requires=['click>=8.1.8', 'cloudpickle>=3.1.1', 'httpx>=0.28.1', 'mcp>=1.3.0', 'tecton>=1.1.5'],
    keywords=["mseep"] + [],
)
