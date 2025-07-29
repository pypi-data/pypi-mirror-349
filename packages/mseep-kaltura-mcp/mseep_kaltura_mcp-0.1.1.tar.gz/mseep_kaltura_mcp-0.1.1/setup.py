
from setuptools import setup, find_packages

setup(
    name="mseep-kaltura-mcp",
    version="0.1.0",
    description="Kaltura MCP Server for LLM integration",
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
    install_requires=['mcp>=1.4.1', 'KalturaApiClient>=18.0.0', 'pyyaml>=6.0', 'anyio[trio]>=3.6.2', 'trio>=0.29.0', 'aiohttp>=3.8.5', 'python-magic>=0.4.27', 'requests-toolbelt>=1.0.0', 'lxml>=5.0.0', 'uvicorn>=0.27.0', 'starlette>=0.36.0', 'requests>=2.31.0', 'sseclient>=0.0.27'],
    keywords=["mseep"] + [],
)
