
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-florence2",
    version="0.3.2",
    description="An MCP server for processing images using Florence-2",
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
    install_requires=['dill>=0.3.9', 'einops>=0.8.1', 'mcp>=1.6', 'pillow>=11.1', 'pydantic>=2.10.6', 'pypdfium2>=4.30.1', 'requests>=2.32.3', 'rich-click>=1.8.8', 'timm>=1.0.15', 'torch>=2.6', 'transformers>=4.49'],
    keywords=["mseep"] + [],
)
