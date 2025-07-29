
from setuptools import setup, find_packages

setup(
    name="mseep-daytona-mcp-interpreter",
    version="0.1.1",
    description="A Daytona MCP server for Python code interpretation",
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
    install_requires=['mcp[cli]>=1.0.0', 'pydantic>=2.10.6', 'python-dotenv>=1.0.1', 'httpx>=0.24.0', 'daytona-sdk>=0.10.5'],
    keywords=["mseep"] + [],
)
