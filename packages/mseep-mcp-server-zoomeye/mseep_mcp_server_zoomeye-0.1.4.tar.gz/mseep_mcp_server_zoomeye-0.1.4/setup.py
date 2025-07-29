
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-server-zoomeye",
    version="0.1.3",
    description="A Model Context Protocol server providing tools for ZoomEye queries for LLMs",
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
    install_requires=['mcp>=1.0.0', 'pydantic>=2.0.0', 'requests>=2.32.3', 'python-dotenv>=1.0.0'],
    keywords=["mseep"] + ['zoomeye', 'mcp', 'llm'],
)
