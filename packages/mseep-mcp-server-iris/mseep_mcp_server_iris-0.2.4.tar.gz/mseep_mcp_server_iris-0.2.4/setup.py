
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-iris",
    version="0.2.3",
    description="A Model Context Protocol server for InterSystems IRIS.",
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
    install_requires=['intersystems-irispython>=5.1.0', 'mcp[cli]>=1.2.0', 'starlette>=0.36.0', 'uvicorn>=0.27.0'],
    keywords=["mseep"] + ['iris', 'mcp', 'llm', 'automation'],
)
